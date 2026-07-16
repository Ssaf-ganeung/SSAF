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


def search_posts(query: str, limit: int = 5, db: Session | None = None) -> list[dict]:
    """제목·내용·카테고리에서 질문 토큰이 걸리는 게시글을 최신순으로 반환한다.

    데이터가 소규모라 LIKE 검색으로 충분하다. 토큰이 하나도 안 남으면
    (예: "게시글 뭐 있어?") 최신 글을 보여준다.
    """
    own_session = db is None
    session = db or SessionLocal()
    try:
        statement = session.query(Post)
        tokens = _tokenize(query)

        if tokens:
            conditions = []
            for token in tokens:
                pattern = f"%{token}%"
                conditions.append(Post.title.ilike(pattern))
                conditions.append(Post.content.ilike(pattern))
            statement = statement.filter(or_(*conditions))

        posts = statement.order_by(Post.created_at.desc()).limit(limit).all()
        return [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "category": post.category.value if post.category else "",
                "created_at": post.created_at.strftime("%Y-%m-%d") if post.created_at else "",
            }
            for post in posts
        ]
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
