# ========================子agent的结构化输出格式控制============================
from pydantic import BaseModel, Field
from typing import List, Dict

class KnowledgeCollectOutput(BaseModel):
    """回答问题结构化输出"""
    explanation: str = Field(description="知识简介")
    essence: str = Field("具体要点")
    metrics: str = Field("相关战术")

class TrainingPlanOutput(BaseModel):
    """训练计划结构化输出"""
    phase: str = Field(description="训练阶段: 基础/进阶/实战")
    objectives: List[str] = Field(description="本阶段训练目标")
    drills: Dict[str, List[str]] = Field(
        description="训练项目: {周数: [训练项目1, 训练项目2]}"
    )
    success_metrics: Dict[str, str] = Field(
        description="成功标准: {指标: 目标值}"
    )

class VideoAnalysisOutput(BaseModel):
    """视频分析结构化输出"""
    strengths: List[str] = Field(description="技术强项")
    weaknesses: List[str] = Field(description="需改进的技术弱点")
    recommendations: List[str] = Field(description="具体改进建议")
    related_drills: List[str] = Field(description="相关训练项目")