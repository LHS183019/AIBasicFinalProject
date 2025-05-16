## Notes
### Document Link
开发过程中你可能会用到的documentation:
+ OpenAI API [doc](https://platform.openai.com/docs/overview) 
需要翻到内地、港澳之外的地方才能访问
+ Gemini API [doc](https://ai.google.dev/gemini-api/docs/openai?hl=zh-cn)
需要翻墙
+ Siliconflow API [doc](https://docs.siliconflow.com/cn/userguide/introduction)
+ openAI Agent SDK [doc](https://openai.github.io/openai-agents-python/)
+ Google ADK [doc](https://google.github.io/adk-docs/)

### Available Model
+ All model provided by Siliconflow
+ Free Gemini model

### Reason to drop Camel
1. Seems like siliconflow is not compatible with camel so well. 
The `camel.types.enums` don't provide the token limit about the siliconflow type.
2. Camel Agent don't support **streaming output**
3. Lack tutorial and guidance

### The Tech Stack
#### Chat Bot
Currently use the OpenAI API.
An alternative way is to use [gemini-api](https://ai.google.dev/gemini-api/docs) (support gemini only)
Another alternative approach is to init an Chat Agent.


#### User Interface
Below listed the corresponding python package for different UI implement: 
1. CLI
    + colorama
2. TUI
    + rich
3. GUI
    + Reflex
    + streamlit

#### Agent system
I'm still figuring what's the best way to build up the agent system. Currently we are using the very crude OpenAI SDK approach.
Here's some promising approaches to build up agent / agentic workflow / multi-agent system:
1. OpenAI agent SDK
https://platform.openai.com/docs/guides/agents
2. google agent SDK with gemini
https://google.github.io/adk-docs/
3. Non-code purpose(e.g. n8n)(not sure if allowed)
4. Other multi-agent framework:
    + camel [no streaming support]
    + langchain and langgraph[too complicated]
    + crewai
    ...

Most importantly, we have no idea what application we gonna build with agent / workflow / multi-agent. Making it harder to decide.

### Learn Basic Concept
Some article and video tutorial Listed Below:

#### How to Protect your LLM
https://www.promptingguide.ai/zh/risks/adversarial#%E5%8F%82%E6%95%B0%E5%8C%96%E6%8F%90%E7%A4%BA%E7%BB%84%E4%BB%B6
https://www.youtube.com/watch?v=6bYGhY9HB8k
https://www.youtube.com/watch?v=jrHRe9lSqqA
https://zhuanlan.zhihu.com/p/30480330292

#### What is structured output:
https://www.youtube.com/watch?v=xpvFinvqRCA

##### What is an Agent:
https://openai.github.io/openai-agents-python/
https://zhuanlan.zhihu.com/p/24432308656
https://zhuanlan.zhihu.com/p/657937696
https://www.zhihu.com/question/1894891236617332066/answer/1900585340592424543
https://zhuanlan.zhihu.com/p/32230066307

##### What is agentic workflow:
https://www.anthropic.com/engineering/building-effective-agents


#### Other Resouces
[一个社媒爬虫repo: 小红书、知乎.......](https://github.com/NanmiCoder/MediaCrawler)

[Reflex](https://youtu.be/ITOZkzjtjUA)
[streamlit](https://www.youtube.com/watch?v=kNgx0AifVo0)
[rich/textual](https://youtu.be/NIyljVEcJKw?si=J6sSi1BgPOIqCO24)
[colorama](https://blog.csdn.net/sunshine_youngforyou/article/details/146162004
)


###### TODO
+ Github action(https://www.youtube.com/watch?v=0aEJBygCn5Q)