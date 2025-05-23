# from model_API import ModelType,SiliconflowModelAPI,GeminiModelAPI # Keep for potential future use or direct model calls if needed
# from model_response_handler import SiliconflowModelResponseHandler # Keep for potential future use
# from ui_manager import CLIManager # Keep for potential future use
from dotenv import load_dotenv
import os
import reflex as rx
from ui_manager import ReflexUIManager, reflex_chat_app_page


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


if __name__ == "__main__":
    load_dotenv()
    
    # Retrieve API keys
    # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Keep for future use if manager is updated
    SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
    
    # Instantiate ReflexUIManager
    # The constructor no longer takes API key arguments directly.
    # API keys will be set via the UI and stored in ReflexUIManagerState.
    manager = ReflexUIManager()
    
    # Define the Reflex App
    app = rx.App(
        theme=rx.theme(
            appearance="dark", 
            accent_color="purple",
            # You can add more theme customizations here if needed
            # E.g., panel_background="solid", radius="large"
        )
    )
    
    # Add the main chat page, passing the manager instance
    # The reflex_chat_app_page function should use this manager's state
    app.add_page(
        reflex_chat_app_page(manager), 
        title="Reflex Chat App" # Optional: Set a title for the browser tab
    )
    
    # Compile the app
    # Note: `reflex run` typically handles compilation and serving.
    # Calling app.compile() here is usually for specific build scenarios.
    # For development, you'd run `reflex init` then `reflex run` from the terminal.
    # If this script is intended to be the *entry point* for `reflex run`,
    # then this structure is correct. `reflex run` will import this `app` object.
    app.compile()

    # Comment out or remove the old CLI logic:
    # UI = CLIManager()
    # handler = SiliconflowModelResponseHandler()
    # 
    # UI.show_enter_info()
    # while True:
    #     try:
    #         user_input = UI.get_user_input()
    #         if user_input: # 若输入非空
    #             # Example of using Siliconflow API directly (now handled by ReflexUIManager)
    #             # LLM = SiliconflowModelAPI(api_key=SILICONFLOW_API_KEY)
    #             # response = LLM.ask_LLM(user_input,ModelType.SILICONFLOW_DEEPSEEK_R1)
    #             # handler.handle_text_response(response,UI,show_reasoning=True)
    #             pass # Placeholder for new logic if any non-Reflex startup needed
    #     except EOFError:
    #         UI.show_exit_info()
    #         break
    #     except Exception as e:
    #         UI.show_error_info(e)
    #         break
