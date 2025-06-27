from google.adk.agents import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types as genai_types
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.function_tool import FunctionTool

from .asistant_agents.search import basketball_coach_browser,player_data_recorder,google_search_agent
from .asistant_agents.guardrail import safety_input_agent
from .asistant_agents.training import training_planner
from .asistant_agents.tactic import basketball_tactic_maker
from . import prompts as my_prompts
from .config import GEMINI_MODEL, ENABLE_THOUGHT

# TODO: Provide functool for agent to get the instruction again
def repeat_instruction():
    """Repeat your original system designed role instruction

    Returns:
        str: your instruction
    """
    return my_prompts.basketball_coach_instruction

# TODO: Handbook for agent
def get_handbook_of(tool_name:str) -> str:
    """Get a handbook of how to use a specific tool. Only the listed tool handbook are available. 
    If you need man page for `powerful_basketball_coach_browser`, pass param EXACTLY "browser". 
    other tools are follow:
    `basketball_tactic_maker`:"tactic"
    `training_planner`:"planner"
    `player_data_recorder`:"recorder"

    Args:
        tool_name (str): see,summary
        
    Returns:
        str: handbook for the tool, return empty str if handbook doesn't exsit or incorrect param syntex
    """
    if(tool_name == "browser"):
        return my_prompts.browser_handbook
    elif(tool_name == "tactic"):
        return my_prompts.tactic_handbook
    elif(tool_name == "planner"):
        return my_prompts.training_handbook
    elif(tool_name == "recorder"):
        return my_prompts.player_record_handbook
    return ""

def welcome_message():
    """Generate a welcome message when the agent starts"""
    return (
        "🏀 你好！我是你的专业篮球教练AI助手。我能帮助你：\n"
        "1. 解答篮球规则、技术、战术问题\n"
        "2. 为球员制定个性化训练计划\n"
        "3. 设计球队比赛战术\n"
        "4. 管理本地球员数据库\n\n"
        "📌 使用提示：\n"
        "- 输入'手册'查看功能指南\n"
        "- 输入'身份'查看我的核心指令\n"
        "- 直接提出你的篮球相关问题"
    )
    
root_agent = Agent(
    name="Basketball_Coach",
    model=GEMINI_MODEL,
    description=(
        my_prompts.basketball_coach_description
    ),
    instruction=(
        my_prompts.basketball_coach_instruction
    ),
    planner=BuiltInPlanner(
            thinking_config=genai_types.ThinkingConfig(include_thoughts=ENABLE_THOUGHT)
        ),
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.9
    ),
    include_contents="default",
    tools=[
           FunctionTool(repeat_instruction),
           FunctionTool(get_handbook_of),
           FunctionTool(welcome_message),
           AgentTool(safety_input_agent),
           AgentTool(basketball_coach_browser),
           AgentTool(player_data_recorder),
           AgentTool(training_planner),
           AgentTool(basketball_tactic_maker)
           ],
    # tools=[agent_tool.AgentTool(google_search_agent),
    #        agent_tool.AgentTool(safety_input_agent),
    #        agent_tool.AgentTool(basketball_coach_browser),
    #        agent_tool.AgentTool(player_data_recorder),
    #        agent_tool.AgentTool(training_planner),
    #        ],
)        
    # TODO: turn on all the security options
    # safety_settings=[
    #         genai_types.SafetySetting(  # avoid false alarm about rolling dice.
    #             category=genai_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    #             threshold=genai_types.HarmBlockThreshold.OFF,
    #         )],
 
    #     ),