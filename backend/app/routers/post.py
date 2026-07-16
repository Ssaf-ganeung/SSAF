from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import post as crud
from app.db.database import get_db
from app.models.post import PostCategory
from app.schemas.post import PostCreate, PostDelete, PostResponse, PostUpdate

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("", response_model=list[PostResponse])
def list_posts(
    category: PostCategory | None = Query(
        default=None,
        description="카테고리 단일 필터. 지정하지 않으면 전체 목록을 반환한다.",
    ),
    limit: int | None = Query(
        default=None,
        gt=0,
        description="반환할 최대 게시글 수. 지정하지 않으면 전체 반환. 예: 최근 5개 -> limit=5",
    ),
    db: Session = Depends(get_db),
):
    """게시글 목록 조회. category/limit 쿼리 파라미터로 필터링·개수 제한 가능."""
    return crud.get_posts(db, category, limit)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """게시글 상세 조회. 없으면 404."""
    db_post = crud.get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return db_post


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """게시글 작성. 인증 없이 누구나 작성 가능, password는 수정/삭제 권한 확인용."""
    return crud.create_post(db, post)


@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    """게시글 수정. 없으면 404, password가 저장된 값과 다르면 403."""
    db_post = crud.get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if db_post.password != post.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password mismatch")
    return crud.update_post(db, db_post, post)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, post: PostDelete, db: Session = Depends(get_db)):
    """게시글 삭제. 없으면 404, password가 저장된 값과 다르면 403."""
    db_post = crud.get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if db_post.password != post.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password mismatch")
    crud.delete_post(db, db_post)
