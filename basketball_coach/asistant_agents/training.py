from google.adk.agents import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types as genai_types
from google.adk.tools import agent_tool

# 导入RAG搜索代理和球员数据库代理
from .search import basketball_rag_search_agent, player_data_record 
from ..prompts import training_planner_description, training_planner_instruction
from ..schema import TrainingPlanOutput
from ..config import MODEl, ENABLE_THOUGHT

# 自定义策略制定代理的指令
# 这里我们将结合 prompts.py 中已有的 instruction 并进行扩展

# HACK: turn off了output_schema，但这样设置prompt也能达到理想的输出效果
custom_strategy_instruction = f"""
{training_planner_instruction}

你现在可以访问以下工具来制定更精准的策略：
1. 使用 `your_players_data_recorder` 获取特定球员的详细信息。在制定策略前，你必须先了解涉及球员的能力、位置、风格等。
2. 使用 `basketball_rag_search_agent` 从专业的篮球资料库中检索最新的战术、训练方法和篮球理论。

综合球员数据和专业知识，为用户提供一个个性化、可执行的篮球战术或训练计划。
请始终以中文回应，并严格按照 {TrainingPlanOutput.__name__} 的格式输出内容。
如果用户要求制定战术，而你认为`TrainingPlanOutput`的字段不足以完全表达战术，请将战术描述在`objectives`或`drills`中，并根据战术类型进行调整。
如果用户没有提供具体球员信息，你需要主动询问他们希望为哪些球员制定战术。
"""

training_planner = Agent(
    name="training_planner",
    model=MODEl, # 使用config.py中定义的模型
    description=training_planner_description, # 从prompts.py导入
    instruction=custom_strategy_instruction,
    planner=BuiltInPlanner(
        thinking_config=genai_types.ThinkingConfig(include_thoughts=ENABLE_THOUGHT)
    ),
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.7, # 适当的温度以鼓励创造性但仍保持逻辑性
        top_p=0.8
    ),
    tools=[
        agent_tool.AgentTool(player_data_record),#球员数据库工具agent 
        agent_tool.AgentTool(basketball_rag_search_agent)# RAG搜索工具
    ]
    # BUG: output_schema指定之后无法调用tool
    # output_schema=TrainingPlanOutput 
)
