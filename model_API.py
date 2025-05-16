from openai import OpenAI
from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing_extensions import Iterable,Union
from enum import Enum
from typing import Sequence,List,Dict


"""
This module provides an interface to interact with various AI models.
It includes an abstract base class for model APIs, an enumeration of supported model types,
and specific implementations for Siliconflow and Gemini models.
"""

# !TODO 拓展ask_LLM功能
# 1. 处理不启用长思考(enable_reasoning=False)的情况
# 2. 参数调试(temperature,frequency_penalty etc)
# 3. 拓展至支持多模态输入(如图片、语音)
# 4. 拓展至支持多模态输出(如图片、语音)
# # 注意API是否支持模态

# TODO 未来
# 5. 拓展至支持结构化输入输出(
#     建议用pydantic的方法而不是json mode，除非模型不支持
#     https://ai.google.dev/gemini-api/docs/openai?hl=zh-cn#structured-output
#     https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses#introduction
#     )
# 6. 输入输出预处理(敏感信息 防prompt注入 etc.)
#         # 注意检查image格式、大小等的合法性


class ModelType(Enum):
    """
    Enumeration of supported model types.
    """
    
    # siliconflow LLM
    SILICONFLOW_DEEPSEEK_R1 = 'Pro/deepseek-ai/DeepSeek-R1'
    SILICONFLOW_QWEN3_30B_A3B = 'Qwen/Qwen3-30B-A3B'
    
    # siliconflow VLM
    SILICONFLOW_DEEPSEEK_V12 = "deepseek-ai/deepseek-vl2"
    
    # NOTE: all GEMINI API not support reasoning output(you can't get the reasoning process at all)
    # NOTE: Gemini flash support MultiMedia input and image generatation
    GEMINI_FLASH_2_0 = "gemini-2.0-flash"  
    # GEMINI_FLASH_2_5 = "gemini-2.5-flash-preview-04-17"            
    # GEMINI_PRO_2_5 = "gemini-2.5-pro-exp-03-25"




class ModelAPIInterface(ABC):
    """
    Abstract base class for model APIs.
    Subclasses should implement the 'client' and 'ask_LLM' methods.
    """
    
    @property
    @abstractmethod
    def client(self):
        """
        Returns the client object used to interact with the model API.
        """
        pass
    
    @abstractmethod
    def ask_LLM(self, query: str, model_type: ModelType, response_format:Union[BaseModel,None], enable_reasoning:bool=True):
        """
        Sends a query to the language model and returns the response.
        If the model_type is not supported, raises a ValueError.
        """
        pass
    


class SiliconflowModelAPI(ModelAPIInterface):
    def __init__(self,api_key):
        super().__init__()
        self._client = OpenAI(api_key=api_key, base_url="https://api.siliconflow.cn/v1")
        
        """
        Initializes the SiliconflowModelAPI with the provided API key.
        """
    @property
    def client(self):
        """
        Returns the client object for Siliconflow API.
        """
        return self._client
    
    def ask_LLM(self,query:str,model_type:ModelType,response_format:Union[BaseModel,None]=None) -> Union[Iterable,None]:
        """
        Sends a query to the specified Siliconflow language model and returns the response.
        If the model_type is not supported, raises a ValueError.
        """
        response = None
        message = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {'role': 'user', 
                    'content': query}
                ]
        try:
            if model_type == ModelType.SILICONFLOW_DEEPSEEK_R1:
                response = self.client.chat.completions.create(
                    model='Pro/deepseek-ai/DeepSeek-R1',
                    messages=message,
                    stream = True,
                    max_tokens=16384
                )
            elif model_type == ModelType.SILICONFLOW_QWEN3_30B_A3B:
                response = self.client.chat.completions.create(
                    model='Qwen/Qwen3-30B-A3B',
                    messages=message,
                    stream = True,
                    max_tokens=8192,
                )
            else:
                raise ValueError(f"Unknown model type {model_type}.")
            return response
        except Exception as e:
            raise RuntimeError(f"Error during requesting the LLM server: {str(e)}")
    
    def ask_VLM(self,query:str,image_ref:List[Dict[str,str]],model_type:ModelType) -> Union[Iterable,None]:
        """
        Sends a query to the specified Siliconflow visual language model and returns the response.
        """
        # 注意检查image格式、大小等的合法性
        pass
    
    def gen_image(self)->str:
        """
        Generates an image using the Siliconflow API and returns the URL or file path.
        """
        # you should return an url or file path or something
        # I'm not sure if it support Open AI API, maybe u need to use the request lib method
        pass

class GeminiModelAPI(ModelAPIInterface):
    """
    NOTE: Pay attention that gemini is not available for several regions like China.

    Args:
        ModelAPIInterface (_type_): _description_
    """
    def __init__(self,api_key):
        super().__init__()
        self._client = OpenAI(api_key=api_key, 
                                base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

    @property
    def client(self):
        """
        Returns the client object for Gemini API.
        """
        return self._client
                    

    def ask_LLM(self,query:str,model_type:ModelType,response_format:Union[BaseModel,None]=None) -> Union[Iterable,None]:
        """
        Sends a query to the specified Gemini language model and returns the response.
        If the model_type is not supported, raises a ValueError.
        """
        response = None
        message = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {'role': 'user', 
                    'content': query}
                ]
        try:
            if model_type == ModelType.GEMINI_FLASH_2_0:
                    response = self.client.chat.completions.create(
                    model = 'gemini-2.5-flash-preview-04-17',
                    messages=message,
                    stream=True,
                    # NOTE: adding attribute 'reasoning_effort="none"' to prohibit reasoning 
                )
            else:
                raise ValueError(f"Unknown model type {model_type}.")
            return response
        except Exception as e:
            raise RuntimeError(f"Error during requesting the LLM server: {str(e)}")


    def ask_VALM(self,query:str,image_ref:List[Dict[str,str]],audio_ref:List[Dict[str,str]],model_type:ModelType) -> Union[Iterable,None]:
        """
        Sends a query to the specified Gemini visual-audio language model and returns the response.
        """
        pass

    
    def gen_image(self)->str:
        """
        Generates an image using the Gemini API and returns the URL or file path.
        """
        # you should return an url or file path or something
        # not sure if support the OpenAI API, may need to turn to gemini API(may leads to Environment compatibility issue)
        pass
