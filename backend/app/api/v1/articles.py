"""
医疗智能体系统 - 文章路由
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.content import Article, Category

router = APIRouter()


class ArticleResponse(BaseModel):
    """文章响应"""
    article_id: int
    title: str
    summary: str | None = None
    content: str
    content: str
    cover_image: str | None = None
    view_count: int
    like_count: int
    status: int
    published_at: datetime | None = None

    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    """分类响应"""
    category_id: int
    category_name: str
    parent_id: int | None = None

    class Config:
        from_attributes = True


@router.get("", response_model=List[ArticleResponse], summary="获取文章列表")
async def get_articles(
    category_id: int | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取文章列表"""
    query = db.query(Article).filter(Article.status == 2)  # 已发布
    if category_id:
        query = query.filter(Article.category_id == category_id)
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    return [ArticleResponse.model_validate(a) for a in articles]


@router.get("/", response_model=List[ArticleResponse], summary="获取文章列表(带斜杠)")
async def get_articles_with_slash(
    category_id: int | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取文章列表(带尾部斜杠)"""
    return await get_articles(category_id, skip, limit, db)


@router.get("/{article_id}", response_model=ArticleResponse, summary="获取文章详情")
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """获取文章详情"""
    article = db.query(Article).filter(
        Article.article_id == article_id,
        Article.status == 2
    ).first()
    if not article:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("文章", article_id)
    
    # 增加阅读量
    article.view_count += 1
    db.commit()
    
    return ArticleResponse.model_validate(article)


@router.get("/categories/", response_model=List[CategoryResponse], summary="获取分类列表")
async def get_categories(parent_id: int | None = None, db: Session = Depends(get_db)):
    """获取分类列表"""
    query = db.query(Category).filter(Category.status == 1)
    if parent_id is not None:
        query = query.filter(Category.parent_id == parent_id)
    categories = query.order_by(Category.sort_order).all()
    return [CategoryResponse.model_validate(c) for c in categories]
