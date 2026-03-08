"""
医疗智能体系统 - 知识库路由
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models.knowledge import MedicalKnowledge, DrugInfo

router = APIRouter()


class KnowledgeResponse(BaseModel):
    """知识响应"""
    knowledge_id: int
    title: str
    summary: str | None = None
    keywords: str | None = None
    view_count: int
    status: int

    class Config:
        from_attributes = True


class DrugInfoResponse(BaseModel):
    """药品信息响应"""
    drug_id: int
    drug_name: str
    generic_name: str | None = None
    specification: str | None = None
    manufacturer: str | None = None
    usage: str | None = None
    indication: str | None = None

    class Config:
        from_attributes = True


@router.get("/search", response_model=List[KnowledgeResponse], summary="搜索知识")
async def search_knowledge(
    keyword: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """搜索医学知识"""
    knowledges = db.query(MedicalKnowledge).filter(
        MedicalKnowledge.status == 2,
        MedicalKnowledge.title.contains(keyword)
    ).offset(skip).limit(limit).all()
    return [KnowledgeResponse.model_validate(k) for k in knowledges]


@router.get("/drugs", response_model=List[DrugInfoResponse], summary="获取药品列表")
async def get_drugs(
    keyword: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取药品列表"""
    query = db.query(DrugInfo).filter(DrugInfo.status == 1)
    if keyword:
        query = query.filter(DrugInfo.drug_name.contains(keyword))
    drugs = query.offset(skip).limit(limit).all()
    return [DrugInfoResponse.model_validate(d) for d in drugs]


@router.get("/drugs/{drug_id}", response_model=DrugInfoResponse, summary="获取药品详情")
async def get_drug(drug_id: int, db: Session = Depends(get_db)):
    """获取药品详情"""
    drug = db.query(DrugInfo).filter(
        DrugInfo.drug_id == drug_id,
        DrugInfo.status == 1
    ).first()
    if not drug:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("药品", drug_id)
    return DrugInfoResponse.model_validate(drug)
