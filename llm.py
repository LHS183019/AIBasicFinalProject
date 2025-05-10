from openai import OpenAI
from pydantic import BaseModel
from typing_extensions import Iterable,Union
from enum import Enum
from typing import Sequence

"""
!TODO 拓展ask_LLM功能
1. 完善对不同model的访问的支持(注意测试 确保运行结果如预期)
2. 参数调试(temperature)
3. 拓展至支持多模态输入(如图片、语音)
4. 拓展至支持多模态输出(如图片、语音)
5. 拓展至支持结构化输入输出(
    建议用pydantic的方法而不是json mode，除非模型不支持
    https://ai.google.dev/gemini-api/docs/openai?hl=zh-cn#structured-output
    https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses#introduction
    )
6. 输入输出预处理(敏感信息 防prompt注入 etc.)
适当重构代码 按需增加函数
"""

class ModelType(Enum):
    SILICONFLOW_DEEPSEEK_R1 = 'Pro/deepseek-ai/DeepSeek-R1'
    SILICONFLOW_QWEN3_30B_A3B = 'Qwen/Qwen3-30B-A3B'
    
    # NOTE: all GEMINI API not supporting reasoning output
    GEMINI_FLASH_2_0 = "gemini-2.0-flash"            
    # GEMINI_FLASH_2_5 = "gemini-2.5-flash-preview-04-17"            
    # GEMINI_PRO_2_5 = "gemini-2.5-pro-exp-03-25"
    
                
def ask_LLM(content:str,model_type:ModelType,api_key:str) -> Union[Iterable,None]:
    """
    This function sends a request to the LLM server and returns the response.
    If the model_type is not llm.ModelType, the function Raise ValueError.
    """
    
    client = None
    response = None
    message = [
                {"role": "system", "content": "You are a helpful assistant."},
                {'role': 'user', 
                'content': content}
            ]
    if not isinstance(model_type, ModelType):
        raise ValueError(f"Unknown model type {model_type}.")
    
    try:
        if model_type == ModelType.SILICONFLOW_DEEPSEEK_R1:
            client = OpenAI(api_key=api_key, 
                            base_url="https://api.siliconflow.cn/v1")
            response = client.chat.completions.create(
                model='Pro/deepseek-ai/DeepSeek-R1',
                messages=message,
                stream = True,
                max_tokens=16384
            )
        elif model_type == ModelType.SILICONFLOW_QWEN3_30B_A3B:
            client = OpenAI(api_key=api_key, 
                            base_url="https://api.siliconflow.cn/v1")
            response = client.chat.completions.create(
                model='Qwen/Qwen3-30B-A3B',
                messages=message,
                stream = True,
                max_tokens=8192,
            )
        elif model_type == ModelType.GEMINI_FLASH_2_0:
                client = OpenAI(api_key=api_key, 
                            base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
                response = client.chat.completions.create(
                model = 'gemini-2.5-flash-preview-04-17',
                messages=message,
                stream=True,
                
                # reasoning_effort="none"
            )
        return response
    except Exception as e:
        raise RuntimeError(f"Error during connecting the LLM server: {str(e)}")
