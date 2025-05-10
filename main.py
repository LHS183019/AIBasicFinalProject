import keyboard
import colorama
import getpass
import os
from llm import ask_LLM,ModelType
from response_handler import process_response
from dotenv import load_dotenv
import os


"""
NOTE:
每次更新之后都建议update requirements.txt,在工作路径下面执行:
pipreqs . --encoding=utf8 --force
你可能需要在当前环境中安装pipreqs这个库:
pip install pipreqs

TODO:
1. 让用户选择模型
2. 让用户设置自己的API key并缓存到本地
3. 让用户选择是否启用长思考功能(切换到没有思考能力的模型?)、输出长思考过程
4. 让用户可以进行多模态输入，接受多模态输出
5. 结构化输入输出
"""


# HACK: 只是一个临时的CLI，UI有待完善
if __name__ == "__main__":
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")

    
    print("欢迎来到语言大模型应用！在下方输入您想问大模型的问题。输入'Ctrl+Z'（Windows）或'Ctrl+D'（Unix/Linux/Mac）以退出应用。")
    
    while True:
        try:
            user_input = input(">>> ").strip()
            if user_input: # 若输入非空
                response = ask_LLM(user_input,ModelType.SILICONFLOW_DEEPSEEK_R1,SILICONFLOW_API_KEY)
                print("输入'q'中止模型输出：")
                process_response(response,hotkey='q')
        except EOFError:
            # 捕获Ctrl+Z（或Ctrl+D）输入
            print("\n欢迎下次使用！")
            break
        
        except Exception as e:
            print(f"{str(e)}")
            print(f"自动退出程序！")
            break
