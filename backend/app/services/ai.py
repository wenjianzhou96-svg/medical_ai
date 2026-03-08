"""
医疗智能体系统 - AI服务层

提供通义千问LLM调用、RAG检索增强、提示词管理等AI能力
"""

import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

import httpx

from app.core.config import settings
from app.core.exceptions import BadRequestException, ServiceUnavailableException

# 配置日志
logger = logging.getLogger(__name__)


class AIService:
    """AI服务类 - 通义千问调用封装"""

    def __init__(self):
        """初始化AI服务"""
        self.api_key = settings.qianwen_api_key
        self.model = settings.qianwen_model
        self.base_url = settings.qianwen_base_url
        self._init_client()

    def _init_client(self):
        """初始化HTTP客户端"""
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=60.0,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()

    async def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        通义千问对话接口

        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            system_prompt: 系统提示词
            temperature: 温度参数 (0-2)
            max_tokens: 最大生成token数

        Returns:
            AI响应结果 {"content": "...", "usage": {...}}
        """
        # 构建请求体 - 使用 OpenAI 兼容格式（compatible-mode）
        messages_list = []
        
        # 添加系统提示词
        if system_prompt:
            messages_list.append({
                "role": "system",
                "content": system_prompt
            })
        
        # 添加用户消息
        messages_list.extend(messages)
        
        request_body = {
            "model": self.model,
            "messages": messages_list,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = await self.client.post(
                "/chat/completions",
                json=request_body
            )
            
            # 打印详细日志用于排查
            logger.info(f"AI API 请求体: {json.dumps(request_body)[:200]}...")
            logger.info(f"AI API 响应状态码: {response.status_code}")
            logger.info(f"AI API 响应内容: {response.text[:500] if response.text else '空'}")

            if response.status_code != 200:
                logger.error(f"AI API调用失败: {response.status_code} - {response.text}")
                raise ServiceUnavailableException(f"AI服务暂不可用: {response.status_code}")

            result = response.json()

            # 解析响应 - OpenAI 兼容格式
            if "choices" in result and result["choices"]:
                message = result["choices"][0].get("message", {})
                content = message.get("content", "")
                usage = result.get("usage", {})

                return {
                    "content": content,
                    "usage": {
                        "prompt_tokens": usage.get("prompt_tokens", 0),
                        "completion_tokens": usage.get("completion_tokens", 0),
                        "total_tokens": usage.get("total_tokens", 0)
                    }
                }

            raise ServiceUnavailableException("AI服务响应格式异常")

        except httpx.TimeoutException:
            logger.error("AI API调用超时")
            raise ServiceUnavailableException("AI服务响应超时")
        except httpx.RequestError as e:
            logger.error(f"AI API请求错误: {str(e)}")
            raise ServiceUnavailableException("AI服务请求失败")

    async def consultation_chat(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        问诊对话接口

        Args:
            user_message: 用户消息
            conversation_history: 对话历史
            user_info: 用户健康档案信息

        Returns:
            AI响应 {"reply": "...", "suggestion": "...", "is_emergency": False}
        """
        # 构建系统提示词
        system_prompt = self._build_consultation_prompt(user_info)

        # 构建消息列表
        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})

        # 调用AI
        result = await self.chat(
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=1000
        )

        # 解析AI回复
        ai_content = result["content"]

        # 检查是否包含紧急症状
        is_emergency = self._check_emergency(ai_content)

        # 尝试解析结构化回复
        try:
            # 尝试JSON格式解析
            parsed = json.loads(ai_content)
            return {
                "reply": parsed.get("reply", ai_content),
                "suggestion": parsed.get("suggestion", ""),
                "is_emergency": is_emergency,
                "follow_up_questions": parsed.get("follow_up_questions", [])
            }
        except json.JSONDecodeError:
            # 非JSON格式，直接返回文本
            return {
                "reply": ai_content,
                "suggestion": "",
                "is_emergency": is_emergency,
                "follow_up_questions": []
            }

    async def generate_diagnosis_suggestion(
        self,
        symptoms: str,
        conversation_history: List[Dict[str, str]],
        user_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        生成诊断建议

        Args:
            symptoms: 症状描述
            conversation_history: 对话历史
            user_info: 用户健康档案信息

        Returns:
            诊断建议 {"diagnosis": "...", "suggestions": [...], "severity": "low"}
        """
        system_prompt = """你是一位专业的医疗AI助手，请根据用户的症状描述和对话历史，提供诊断建议。

请按以下JSON格式返回：
{
    "diagnosis": "可能的诊断",
    "possible_conditions": ["可能的疾病1", "可能的疾病2"],
    "suggestions": ["建议1", "建议2"],
    "severity": "low/medium/high/critical",
    "recommendations": "详细建议"
}

注意：
1. 这是AI辅助诊断，仅供参考，不能替代专业医生诊断
2. 如果发现紧急症状，请将severity设为"critical"
3. 建议用户尽快就医的情况请明确指出"""

        # 构建消息
        messages = []
        if conversation_history:
            messages.extend(conversation_history)

        # 添加用户症状总结
        messages.append({
            "role": "user",
            "content": f"根据以上问诊信息，请给出诊断建议。\n\n症状总结：{symptoms}"
        })

        result = await self.chat(
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=1500
        )

        ai_content = result["content"]

        # 解析诊断建议
        try:
            parsed = json.loads(ai_content)
            return parsed
        except json.JSONDecodeError:
            return {
                "diagnosis": "无法生成诊断建议",
                "possible_conditions": [],
                "suggestions": ["请咨询专业医生"],
                "severity": "unknown",
                "recommendations": ai_content
            }

    async def generate_consultation_report(
        self,
        consultation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成问诊报告

        Args:
            consultation_data: 问诊数据

        Returns:
            问诊报告 {"title": "...", "sections": [...], "summary": "..."}
        """
        system_prompt = """你是一位专业的医疗AI助手，请根据问诊记录生成详细的问诊报告。

请按以下JSON格式返回：
{
    "title": "问诊报告标题",
    "patient_info": {"name": "...", "age": "...", "gender": "..."},
    "chief_complaint": "主诉",
    "history_of_present_illness": "现病史",
    "ai_diagnosis": "AI诊断",
    "doctor_review": "医生审核",
    "suggestions": ["建议1", "建议2"],
    "summary": "总结"
}"""

        messages = [
            {"role": "user", "content": f"请生成问诊报告：\n{json.dumps(consultation_data, ensure_ascii=False)}"}
        ]

        result = await self.chat(
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=2000
        )

        ai_content = result["content"]

        # 解析报告
        try:
            parsed = json.loads(ai_content)
            return parsed
        except json.JSONDecodeError:
            return {
                "title": "问诊报告",
                "content": ai_content,
                "summary": "报告生成完成"
            }

    def _build_consultation_prompt(self, user_info: Optional[Dict[str, Any]] = None) -> str:
        """构建问诊系统提示词"""
        prompt = """你是一位专业、亲切的医疗AI问诊助手。你的目标是：
1. 通过友好的对话方式了解用户的症状
2. 收集足够的症状信息以便做出初步判断
3. 适当进行追问，获取更多关键信息
4. 提供有价值的健康建议

问诊原则：
1. 始终保持专业、耐心、友善的态度
2. 询问症状的位置、持续时间、严重程度、诱因等
3. 关注伴随症状
4. 了解用户的既往病史、过敏史等信息
5. 根据症状判断是否需要紧急就医
6. 提供初步建议，但明确说明这是AI辅助建议，不能替代医生诊断

紧急症状识别：
- 胸痛、胸闷、呼吸困难
- 严重头痛、意识模糊
- 大量出血
- 高热不退
- 剧烈腹痛
等危急情况应立即提示用户就医

请用中文回复，语言要通顺自然，不要机械地罗列问题。"""

        # 添加用户健康信息
        if user_info:
            prompt += f"\n\n用户健康档案信息："
            if user_info.get("blood_type"):
                prompt += f"\n血型：{user_info['blood_type']}"
            if user_info.get("medical_history"):
                prompt += f"\n既往病史：{user_info['medical_history']}"
            if user_info.get("allergy_history"):
                prompt += f"\n过敏史：{user_info['allergy_history']}"
            if user_info.get("medications"):
                prompt += f"\n当前用药：{user_info['medications']}"

        return prompt

    def _check_emergency(self, content: str) -> bool:
        """检查内容是否包含紧急症状"""
        emergency_keywords = [
            "紧急", "立即就医", "尽快就医", "急诊",
            "胸痛", "呼吸困难", "大量出血", "意识丧失",
            "剧烈疼痛", "高热不退", "休克"
        ]

        content_lower = content.lower()
        for keyword in emergency_keywords:
            if keyword in content_lower:
                return True

        return False


class RAGService:
    """RAG检索增强服务"""

    def __init__(self):
        """初始化RAG服务"""
        self.ai_service = AIService()
        # 知识库存储（后续可接入向量数据库）
        self.knowledge_base = self._init_knowledge_base()

    def _init_knowledge_base(self) -> List[Dict[str, str]]:
        """初始化基础知识库"""
        return [
            {
                "category": "常见症状",
                "keywords": "头痛,头晕,头昏",
                "content": "头痛常见原因：紧张性头痛、偏头痛、血压升高、颈椎病、睡眠不足等。建议：注意休息、规律作息、必要时就医检查。"
            },
            {
                "category": "常见症状",
                "keywords": "发热,发烧,高温",
                "content": "发热常见原因：感染、炎症、肿瘤等。处理建议：多喝水、物理降温、必要时使用退烧药、持续发热需就医。"
            },
            {
                "category": "常见症状",
                "keywords": "咳嗽,咳痰,喉咙痛",
                "content": "咳嗽常见原因：感冒、支气管炎、肺炎、过敏等。建议：多喝水、避免刺激性食物、持续咳嗽需就医。"
            },
            {
                "category": "常见症状",
                "keywords": "胸痛,胸闷,呼吸困难",
                "content": "胸痛可能涉及心血管、呼吸系统疾病，属于危急症状。建议：立即就医，尤其是伴随呼吸困难、出汗等症状时。"
            },
            {
                "category": "常见症状",
                "keywords": "腹痛,胃痛,肚子痛",
                "content": "腹痛原因多样，如消化不良、胃炎、阑尾炎等。建议：注意饮食、观察疼痛性质、持续疼痛需就医。"
            },
            {
                "category": "健康建议",
                "keywords": "预防,保健,养生",
                "content": "健康建议：均衡饮食、适量运动、充足睡眠、定期体检、保持心情愉悦。"
            }
        ]

    async def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        """
        检索知识库

        Args:
            query: 查询内容
            top_k: 返回结果数量

        Returns:
            知识条目列表
        """
        # 简单关键词匹配（后续可接入向量检索）
        results = []
        query_lower = query.lower()

        for item in self.knowledge_base:
            keywords = item["keywords"].lower()
            # 简单的关键词匹配
            if any(kw in query_lower for kw in keywords.split(",")):
                results.append(item)

        return results[:top_k]

    async def augment_prompt(self, query: str, user_message: str) -> str:
        """
        增强提示词

        Args:
            query: 用户查询
            user_message: 用户消息

        Returns:
            增强后的提示词
        """
        # 检索相关知识
        knowledge = await self.retrieve(query)

        if not knowledge:
            return user_message

        # 构建增强提示词
        context = "\n\n".join([
            f"【{item['category']}】{item['content']}"
            for item in knowledge
        ])

        enhanced_prompt = f"""参考以下医学知识回答用户问题：

{context}

用户问题：{user_message}

请结合以上知识给出专业、准确的回答。"""

        return enhanced_prompt


# 创建全局AI服务实例（延迟初始化）
_ai_service = None
_rag_service = None

def get_ai_service() -> 'AIService':
    """获取AI服务实例（延迟初始化）"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service

def get_rag_service() -> 'RAGService':
    """获取RAG服务实例（延迟初始化）"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service

# 保持向后兼容
ai_service = AIService()
rag_service = RAGService()
