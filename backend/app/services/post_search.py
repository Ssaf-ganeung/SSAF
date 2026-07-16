"""커뮤니티 게시글 검색. 챗봇이 "게시글 찾아줘" 류 질문에 답하기 위한 근거를 만든다.

장소 데이터(place_data)는 JSON 파일을 메모리에 캐시하지만, 게시글은 사용자가 계속
쓰는 값이라 캐시하지 않고 매번 DB를 조회한다.
"""
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.post import Post

# 이 단어들이 있으면 커뮤니티 게시글을 찾는 질문으로 본다.
POST_INTENT_WORDS = (
    "게시글", "게시물", "게시판", "커뮤니티", "글", "posts",
    "후기", "리뷰", "추천글", "얘기", "이야기", "썼", "올라온", "올린",
)

# 점수를 매길 후보 수. 전부 가져와도 되지만 글이 늘어날 때를 대비해 상한을 둔다.
CANDIDATE_LIMIT = 200

# 질문에서 빼도 되는 흔한 말 (검색어로 쓰면 아무 글이나 다 걸린다)
STOPWORDS = {
    "게시글", "게시물", "게시판", "커뮤니티", "후기", "리뷰", "추천글",
    "검색", "찾아줘", "찾아", "알려줘", "알려", "보여줘", "보여", "있어", "있나",
    "뭐", "무슨", "어떤", "관련", "대한", "대해", "좀", "요즘", "최근",
}


def has_post_intent(query: str) -> bool:
    """게시글을 찾는 질문인지 판단한다."""
    return any(word in query for word in POST_INTENT_WORDS)



def _tokenize(query: str) -> list[str]:
    """검색에 쓸 만한 토큰만 남긴다. 2글자 미만과 불용어는 버린다."""
    tokens = []
    for raw in query.split():
        token = raw.strip(",.?!·'\"()[]")
        if len(token) >= 2 and token not in STOPWORDS:
            tokens.append(token)
    return tokens


def _to_dict(post: Post) -> dict:
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "category": post.category.value if post.category else "",
        "created_at": post.created_at.strftime("%Y-%m-%d") if post.created_at else "",
    }


def _score(post: Post, tokens: list[str]) -> int:
    """토큰이 몇 개나 걸리는지로 관련도를 매긴다. 제목에 걸리면 더 쳐준다.

    토큰을 OR로 걸면 "대전 맛집"에서 '대전'만 스친 글도 다 통과하므로,
    걸린 토큰 수로 다시 줄을 세워야 맛집 글이 위로 온다.
    """
    category = post.category.value if post.category else ""
    haystack = f"{post.title} {post.content} {category}"
    score = 0
    for token in tokens:
        if token in post.title or token in category:
            score += 3  # 제목·카테고리 일치가 본문 언급보다 강한 신호
        elif token in haystack:
            score += 1
    return score


def search_posts(query: str, limit: int = 5, db: Session | None = None) -> list[dict]:
    """질문과 관련도가 높은 게시글을 반환한다.

    데이터가 소규모라 LIKE로 후보를 추린 뒤 파이썬에서 점수를 매긴다.
    토큰이 하나도 안 남으면(예: "게시글 뭐 있어?") 최신 글을 보여준다.
    """
    own_session = db is None
    session = db or SessionLocal()
    try:
        tokens = _tokenize(query)

        if not tokens:
            posts = session.query(Post).order_by(Post.created_at.desc()).limit(limit).all()
            return [_to_dict(post) for post in posts]

        conditions = []
        for token in tokens:
            pattern = f"%{token}%"
            conditions.append(Post.title.ilike(pattern))
            conditions.append(Post.content.ilike(pattern))

        candidates = (
            session.query(Post)
            .filter(or_(*conditions))
            .order_by(Post.created_at.desc())
            .limit(CANDIDATE_LIMIT)
            .all()
        )

        # 점수 내림차순, 같으면 최신순(후보를 이미 최신순으로 받았으므로 안정 정렬이면 유지된다)
        ranked = sorted(candidates, key=lambda post: _score(post, tokens), reverse=True)
        return [_to_dict(post) for post in ranked[:limit]]
    finally:
        if own_session:
            session.close()


def format_post_context(posts: list[dict]) -> str:
    """검색된 게시글을 프롬프트에 넣을 텍스트로 변환한다."""
    if not posts:
        return ""
    lines = []
    for post in posts:
        # 본문이 길면 프롬프트가 비대해지므로 앞부분만 근거로 준다.
        snippet = " ".join(post["content"].split())[:80]
        lines.append(
            f"- [{post['id']}] {post['title']} ({post['category']}, {post['created_at']}) — {snippet}"
        )
    return "\n".join(lines)
