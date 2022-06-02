from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[schemas.PostOut])
# @router.get("/")
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 1,
    skip: int = 1,
    search: Optional[str] = "",
):
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
    ).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_post(payload: dict = Body(...)):
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """
    #         insert into posts (title, content, published)
    #         values (%s, %s, %s)
    #         returning *
    #     """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """
    #         select * from posts where id = %s
    #     """,
    #     (str(id)),
    # )
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """
    #         delete from posts where id = %s returning *
    #     """,
    #     (str(id)),
    # )
    # deleted_post = cursor.fetchone()
    # conn.commit()

    delete_post_query = db.query(models.Post).filter(models.Post.id == id)
    delete_post = delete_post_query.first()

    if not delete_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found"
        )

    if delete_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )

    delete_post_query.delete(synchronize_session=False)
    db.commit()

    # if status_code = 204 -> do not send the data back!
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """
    #         update posts set title = %s, content = %s, published = %s
    #         where id = %s
    #         returning *
    #     """,
    #     (post.title, post.content, post.published, id),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    if not updated_post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found"
        )
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return updated_post_query.first()
