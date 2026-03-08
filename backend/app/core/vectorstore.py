"""
医疗智能体系统 - Chroma向量数据库模块

提供向量存储和检索功能，基于Chroma实现
"""

import os
from typing import List, Optional, Dict, Any
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

from app.core.config import settings
from app.core.logging import logger


class VectorStoreManager:
    """向量存储管理器"""

    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self._initialize()

    def _initialize(self):
        """初始化嵌入模型和向量存储"""
        try:
            # 使用HuggingFace嵌入模型
            # 可以根据需要更换为其他嵌入模型
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )

            # 确保持久化目录存在
            persist_dir = settings.chroma_persist_dir
            os.makedirs(persist_dir, exist_ok=True)

            logger.info(f"初始化Chroma向量数据库，持久化目录: {persist_dir}")
        except Exception as e:
            logger.error(f"初始化Chroma向量数据库失败: {e}")
            raise

    def get_vectorstore(self, collection_name: str = "medical_knowledge") -> Chroma:
        """获取指定集合的向量存储"""
        try:
            vectorstore = Chroma(
                client=None,
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=settings.chroma_persist_dir
            )
            return vectorstore
        except Exception as e:
            logger.error(f"获取向量存储失败: {e}")
            raise

    def add_documents(
        self,
        documents: List[Document],
        collection_name: str = "medical_knowledge"
    ) -> List[str]:
        """添加文档到向量存储"""
        try:
            vectorstore = self.get_vectorstore(collection_name)
            ids = vectorstore.add_documents(documents)
            vectorstore.persist()
            logger.info(f"成功添加 {len(documents)} 个文档到集合 {collection_name}")
            return ids
        except Exception as e:
            logger.error(f"添加文档失败: {e}")
            raise

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        collection_name: str = "medical_knowledge",
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """相似度搜索"""
        try:
            vectorstore = self.get_vectorstore(collection_name)
            docs = vectorstore.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
            return docs
        except Exception as e:
            logger.error(f"相似度搜索失败: {e}")
            raise

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        collection_name: str = "medical_knowledge",
        filter: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """带分数的相似度搜索"""
        try:
            vectorstore = self.get_vectorstore(collection_name)
            docs_with_scores = vectorstore.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter
            )
            return docs_with_scores
        except Exception as e:
            logger.error(f"带分数的相似度搜索失败: {e}")
            raise

    def delete_collection(self, collection_name: str):
        """删除指定集合"""
        try:
            vectorstore = self.get_vectorstore(collection_name)
            vectorstore.delete_collection()
            logger.info(f"成功删除集合: {collection_name}")
        except Exception as e:
            logger.error(f"删除集合失败: {e}")
            raise

    def get_collection_info(self, collection_name: str = "medical_knowledge") -> Dict[str, Any]:
        """获取集合信息"""
        try:
            vectorstore = self.get_vectorstore(collection_name)
            return {
                "collection_name": collection_name,
                "count": vectorstore._collection.count(),
                "persist_directory": settings.chroma_persist_dir
            }
        except Exception as e:
            logger.error(f"获取集合信息失败: {e}")
            return {"error": str(e)}


# 全局向量存储管理器实例
vector_store_manager = VectorStoreManager()


def get_vector_store() -> Chroma:
    """获取默认向量存储的依赖函数"""
    return vector_store_manager.get_vectorstore()
