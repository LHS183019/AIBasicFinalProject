from model_API import ModelType,SiliconflowModelAPI,GeminiModelAPI
from model_response_handler import SiliconflowModelResponseHandler
from ui_manager import CLIManager,ReflexUIManager
from dotenv import load_dotenv
import os


"""
TODO:
1. 让用户选择模型
2. 让用户设置自己的API key并缓存到本地
3. 让用户选择是否启用长思考功能(切换到没有思考能力的模型?)、输出长思考过程
5. 支持markdown格式显示?

TODO: 未来
1. 让用户可以进行多模态输入
1. 处理多模态输出
2. Agent
3. 内置prompt
"""


# HACK: 只是一个临时的CLI，UI有待完善
if __name__ == "__main__":
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
    
    UI = CLIManager()
    handler = SiliconflowModelResponseHandler()
    
    UI.show_enter_info()
    while True:
        try:
            user_input = UI.get_user_input()
            if user_input: # 若输入非空
                LLM = SiliconflowModelAPI(api_key=SILICONFLOW_API_KEY)
                response = LLM.ask_LLM(user_input,ModelType.SILICONFLOW_DEEPSEEK_R1)
                handler.handle_text_response(response,UI,show_reasoning=True)
        except EOFError:
            # 捕获Ctrl+Z（或Ctrl+D）输入
            UI.show_exit_info()
            break
        except Exception as e:
            UI.show_error_info(e)
            break
