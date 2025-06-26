from google.adk.agents import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types as genai_types
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.function_tool import FunctionTool

from .asistant_agents.search import basketball_coach_browser,player_data_record,google_search_agent
from .asistant_agents.guardrail import safety_input_agent
from .asistant_agents.training import training_planner
from . import prompts as my_prompts
from .config import MODEl, ENABLE_THOUGHT

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
    ``:""
    ``:""


    Args:
        tool_name (str): see,summary
        
    Returns:
        str: handbook for the tool, return empty str if handbook doesn't exsit or incorrect param syntex
    """
    if(tool_name == "browser"):
        return my_prompts.browser_handbook
    
    return ""
    
    
root_agent = Agent(
    name="Basketball_Coach",
    model=MODEl,
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
        temperature=0.8,
        top_p=0.9
    ),
    include_contents="default",
    tools=[
           FunctionTool(repeat_instruction),
           FunctionTool(get_handbook_of),
           AgentTool(safety_input_agent),
           AgentTool(basketball_coach_browser),
           AgentTool(player_data_record),
           AgentTool(training_planner)
           ],
    # tools=[agent_tool.AgentTool(google_search_agent),
    #        agent_tool.AgentTool(safety_input_agent),
    #        agent_tool.AgentTool(basketball_coach_browser),
    #        agent_tool.AgentTool(player_data_record),
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