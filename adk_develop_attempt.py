from dotenv import load_dotenv
import os
from google_adk import Agent, Gemini

# 加载环境变量
load_dotenv()
ADK_API_KEY = os.getenv("GEMINI_API_KEY")

# 初始化ADK代理（基于Gemini模型）
agent = Agent(llm=Gemini(api_key=ADK_API_KEY))

# 定义基础聊天功能
def chat_with_agent(user_input):
    response = agent.run(user_input)
    return response

if __name__ == "__main__":
    if not ADK_API_KEY:
        raise ValueError("请在.env文件中配置ADK_API_KEY（参考https://google.github.io/adk-docs/获取密钥）")
    print("简易ADK聊天机器人启动！输入任意内容开始对话，输入'退出'结束")
    while True:
        user_msg = input("用户：")
        if user_msg.strip().lower() == "退出":
            break
        bot_response = chat_with_agent(user_msg)
        print(f"机器人：{bot_response}")

