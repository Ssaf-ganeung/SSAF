from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


def get_posts(db: Session) -> list[Post]:
    """전체 게시글을 최신순(created_at 내림차순)으로 조회."""
    return db.query(Post).order_by(Post.created_at.desc()).all()


def get_post(db: Session, post_id: int) -> Post | None:
    """단건 조회. 없으면 None (404 처리는 라우터에서)."""
    return db.query(Post).filter(Post.id == post_id).first()


def create_post(db: Session, post: PostCreate) -> Post:
    db_post = Post(title=post.title, content=post.content, password=post.password)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, db_post: Post, post: PostUpdate) -> Post:
    """db_post는 라우터에서 조회·비밀번호 검증까지 끝낸 대상만 전달된다."""
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, db_post: Post) -> None:
    """db_post는 라우터에서 조회·비밀번호 검증까지 끝낸 대상만 전달된다."""
    db.delete(db_post)
    db.commit()
