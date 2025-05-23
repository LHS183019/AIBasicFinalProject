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
    def ask_LLM(self, messages: List[Dict[str, str]], model_type: ModelType, response_format:Union[BaseModel,None], api_key: str = None, enable_reasoning:bool=True):
        """
        Sends a list of messages to the language model and returns the response.
        Accepts an optional api_key to use for this specific call.
        If the model_type is not supported, raises a ValueError.
        """
        pass
    


class SiliconflowModelAPI(ModelAPIInterface):
    def __init__(self, api_key: str = None):
        super().__init__()
        self._api_key = api_key # Store the initial API key
        self._client = None
        if api_key:
            self._client = OpenAI(api_key=api_key, base_url="https://api.siliconflow.cn/v1")
        
    @property
    def client(self):
        """
        Returns the client object for Siliconflow API.
        Initializes client on first access if an API key is available.
        """
        if self._client is None and self._api_key:
            self._client = OpenAI(api_key=self._api_key, base_url="https://api.siliconflow.cn/v1")
        return self._client

    def _get_client_with_key(self, api_key_override: str = None) -> OpenAI:
        """
        Gets an OpenAI client instance. Uses api_key_override if provided,
        otherwise uses self._api_key. Initializes client if necessary.
        Raises ValueError if no API key is available.
        """
        key_to_use = api_key_override or self._api_key
        if not key_to_use:
            raise ValueError("SiliconFlow API key not provided for ask_LLM call and not set during initialization.")
        
        # If overriding key, or if client not initialized with the instance key
        if api_key_override and api_key_override != self._api_key:
            return OpenAI(api_key=api_key_override, base_url="https://api.siliconflow.cn/v1")
        
        if self.client: # Access via property to ensure it's initialized if self._api_key was present
             return self.client
        
        # This case should ideally be caught by the key_to_use check, but as a fallback:
        raise ValueError("Client could not be initialized.")


    def ask_LLM(self, messages: List[Dict[str, str]], model_type: ModelType, response_format: Union[BaseModel, None] = None, api_key: str = None, enable_reasoning: bool = True) -> Union[Iterable, None]:
        """
        Sends a list of messages to the specified Siliconflow language model and returns the response.
        Uses the provided api_key for this call, or the one set during initialization.
        If the model_type is not supported, raises a ValueError.
        """
        client_to_use = self._get_client_with_key(api_key_override=api_key)
        if not client_to_use:
             raise ValueError("SiliconFlow API client not available.")

        # The 'messages' parameter is now passed directly
        # Ensure it's a list of dicts with "role" and "content" keys
        if not isinstance(messages, list) or not all(isinstance(m, dict) and "role" in m and "content" in m for m in messages):
            raise ValueError("The 'messages' argument must be a list of dictionaries, each with 'role' and 'content'.")

        response = None
        try:
            # Add a system prompt if not already present and if it's standard practice for this model
            # For now, assuming messages list is complete as prepared by ReflexUIManagerState
            
            if model_type == ModelType.SILICONFLOW_DEEPSEEK_R1:
                response = client_to_use.chat.completions.create(
                    model='Pro/deepseek-ai/DeepSeek-R1',
                    messages=messages, # Use the passed messages list
                    stream=True,
                    max_tokens=16384
                )
            elif model_type == ModelType.SILICONFLOW_QWEN3_30B_A3B:
                response = client_to_use.chat.completions.create(
                    model='Qwen/Qwen3-30B-A3B',
                    messages=messages, # Use the passed messages list
                    stream=True,
                    max_tokens=8192,
                )
            else:
                # Check if it's any other SiliconFlow model, e.g. VLM, though this method is ask_LLM
                if "SILICONFLOW" in model_type.name:
                     raise ValueError(f"Unsupported SiliconFlow LLM model type: {model_type.value}")
                else:
                     raise ValueError(f"Model type {model_type.value} is not a SiliconFlow model.")
            return response
        except Exception as e:
            raise RuntimeError(f"Error during requesting the SiliconFlow LLM server: {str(e)}")
    
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
    def __init__(self, api_key: str = None):
        super().__init__()
        self._api_key = api_key # Store the initial API key
        self._client = None
        if api_key:
            self._client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

    @property
    def client(self):
        """
        Returns the client object for Gemini API.
        Initializes client on first access if an API key is available.
        """
        if self._client is None and self._api_key:
            self._client = OpenAI(api_key=self._api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        return self._client

    def _get_client_with_key(self, api_key_override: str = None) -> OpenAI:
        """
        Gets an OpenAI client instance for Gemini. Uses api_key_override if provided,
        otherwise uses self._api_key. Initializes client if necessary.
        Raises ValueError if no API key is available.
        """
        key_to_use = api_key_override or self._api_key
        if not key_to_use:
            raise ValueError("Gemini API key not provided for ask_LLM call and not set during initialization.")

        if api_key_override and api_key_override != self._api_key:
            return OpenAI(api_key=api_key_override, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        
        if self.client: # Access via property
            return self.client
            
        raise ValueError("Gemini client could not be initialized.")

    def ask_LLM(self, messages: List[Dict[str, str]], model_type: ModelType, response_format: Union[BaseModel, None] = None, api_key: str = None, enable_reasoning: bool = True) -> Union[Iterable, None]:
        """
        Sends a list of messages to the specified Gemini language model and returns the response.
        Uses the provided api_key for this call, or the one set during initialization.
        If the model_type is not supported, raises a ValueError.
        """
        client_to_use = self._get_client_with_key(api_key_override=api_key)
        if not client_to_use:
            raise ValueError("Gemini API client not available.")

        if not isinstance(messages, list) or not all(isinstance(m, dict) and "role" in m and "content" in m for m in messages):
            raise ValueError("The 'messages' argument must be a list of dictionaries, each with 'role' and 'content'.")

        response = None
        try:
            # Add a system prompt if not already present and if it's standard practice for this model
            # For now, assuming messages list is complete as prepared by ReflexUIManagerState

            if model_type == ModelType.GEMINI_FLASH_2_0:
                response = client_to_use.chat.completions.create(
                    model=model_type.value, # Use the enum's value directly for consistency
                    messages=messages, # Use the passed messages list
                    stream=True,
                    # NOTE: Gemini API via OpenAI proxy might not support 'reasoning_effort'
                    # This seems to be a Google AI Studio specific parameter.
                    # For OpenAI API compatibility, such custom params are usually not available.
                )
            else:
                if "GEMINI" in model_type.name:
                    raise ValueError(f"Unsupported Gemini LLM model type: {model_type.value}")
                else:
                    raise ValueError(f"Model type {model_type.value} is not a Gemini model.")
            return response
        except Exception as e:
            raise RuntimeError(f"Error during requesting the Gemini LLM server: {str(e)}")


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
