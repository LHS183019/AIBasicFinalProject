from openai import OpenAI
from pydantic import BaseModel
import keyboard
import colorama

"""
TODO:
1. safety issue
https://zhuanlan.zhihu.com/p/30480330292
https://www.promptingguide.ai/zh/risks/adversarial#%E5%8F%82%E6%95%B0%E5%8C%96%E6%8F%90%E7%A4%BA%E7%BB%84%E4%BB%B6
API key manage

2. CLI?
https://blog.csdn.net/sunshine_youngforyou/article/details/146162004

3. Agent
https://zhuanlan.zhihu.com/p/24432308656
https://zhuanlan.zhihu.com/p/657937696
大模型 Agent 是不是就是各种 Prompt 的堆叠？ - Tool的回答 - 知乎
https://www.zhihu.com/question/1894891236617332066/answer/1900585340592424543
https://zhuanlan.zhihu.com/p/32230066307

4. update requirements.txt
pip install pipreqs
pipreqs . --encoding=utf8
"""

client = OpenAI(api_key="sk-qseennfhdprismchczwnkzpohyjmuwgpiaywuclsisgugfvo", 
                base_url="https://api.siliconflow.cn/v1")

                
def ask_LLM(content):
    
    response = client.chat.completions.create(
        model='Pro/deepseek-ai/DeepSeek-R1',
        # model="Qwen/Qwen2.5-72B-Instruct",
        messages=[
            {'role': 'user', 
            'content': content}
        ],
        stream=True
    )

    print("输入'q'中止模型输出：")
    return process_response(response)

def process_response(response):
    reasoning = False
    for chunk in response:
        if not chunk.choices:
            continue
        
        # 检测Ctrl+Q按键事件
        if keyboard.is_pressed('q'):
            print("\n模型输出已中止")
            break
        
        if chunk.choices[0].delta.content:
            if reasoning:
                reasoning = False
                print("#"*30)
            print(chunk.choices[0].delta.content, end="", flush=True)
        if chunk.choices[0].delta.reasoning_content:
            if not reasoning:
                reasoning = True
                print(f"{'#'*10}思考过程{'#'*10}")
            print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
            
            
if __name__ == "__main__":

    print("欢迎来到语言大模型应用！在下方输入您想问大模型的问题。输入'Ctrl+Z'（Windows）或'Ctrl+D'（Unix/Linux/Mac）以退出应用。")
    
    while True:
        try:
            # 读取用户输入
            user_input = input(">>> ").strip()
            ask_LLM(user_input)
        
        except EOFError:
            # 捕获Ctrl+Z（或Ctrl+D）输入
            print("\n欢迎下次使用！")
            break
        
        except Exception as e:
            # 捕获并打印其他异常
            print(f"出现错误: {e}")
            break
