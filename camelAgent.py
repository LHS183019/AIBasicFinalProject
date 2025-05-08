from camel.agents import ChatAgent
from camel.configs import GeminiConfig,SiliconFlowConfig
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.types import ModelType
from camel.toolkits import FunctionTool
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")

SILICONFLOW_DEEPSEEK_R1 = "deepseek-ai/DeepSeek-R1"
SILICONFLOW_QWEN_3_235B_A22B = "Qwen/Qwen3-235B-A22B"
SILICONFLOW_QWEN_3_32B = "Qwen/Qwen3-32B"

gemini_model = ModelFactory.create(
    model_platform=ModelPlatformType.GEMINI,
    model_type=ModelType.GEMINI_1_5_FLASH,
    model_config_dict=GeminiConfig().as_dict(),
    api_key=GEMINI_API_KEY
)

siliconflow_deepseek_model = ModelFactory.create(
    model_platform=ModelPlatformType.SILICONFLOW,
    model_type=SILICONFLOW_DEEPSEEK_R1,
    model_config_dict=SiliconFlowConfig(stream=True).as_dict(),
    api_key=SILICONFLOW_API_KEY
)

siliconflow_qwen_model = ModelFactory.create(
    model_platform=ModelPlatformType.SILICONFLOW,
    model_type=SILICONFLOW_QWEN_3_32B,
    model_config_dict=SiliconFlowConfig(stream=True).as_dict(),
    api_key=SILICONFLOW_API_KEY
)

# Define system message
sys_msg = "You are a helpful assistant."

# Set agent
camel_agent = ChatAgent(system_message=sys_msg, model=siliconflow_qwen_model)

user_msg = """what is a apple"""

# Get response information
response = camel_agent.step(user_msg)
# camel_agent._handle_stream_response(response,response.info[""])
print(response.msgs[0].content,flush=True)
