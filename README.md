# 之前的内容搬到了开发者手册V3.md里面！请查收


## 应用简介（待完善）
三个场景
+ 知识咨询
+ 策略制定
+ 影片分析

三个应用优势
+ 个性化球员资料记录
+ 功能集成
+ 战术板呈现（如果能做出来的话）

三个......


## 目前的篮球Agent (6.25 update)
![safe guard](asset/showcase1.png)
![using google search as alternative](asset/showcase2.png)
![using google search as alternative](asset/showcase3.png)
![using rag search](asset/showcase4.png)
![safe guard in middle](asset/showcase5.png)


## 环境配置（6.25更新）

我电脑上的python版本为`3.11.13`, 建议使用`3.11.x`的python~。

建立python虚拟环境：
待完善

你需要在根目录配置一个命名为`.env`的文件，具体内容可以参考`.env.example`
```
SILICONFLOW_API_KEY=你的siliconflow_key
GOOGLE_API_KEY=你的GEMINI_key
GOOGLE_GENAI_USE_VERTEXAI=FALSE

GOOGLE_CLOUD_PROJECT="basketball-coach-rag"
GOOGLE_CLOUD_LOCATION="us-central1"
GOOGLE_GENAI_USE_VERTEXAI="True"
GOOGLE_APPLICATION_CREDENTIALS="basketball_coach//service_key.json"
RAG_CORPUS = "projects/basketball-coach-rag/locations/us-central1/ragCorpora/4532873024948404224"
```

（不确定）gcloud设定...

以及下载需要用到的一些依赖项，先把工作路径切换到根目录`AIBasicFinalProject`

然后在你的环境中运行：
```
pip install -r requirements.txt
```

## 运行我们的Agent！
在虚拟环境中，切换工作目录直到根目录`AIBasicFinalProject`，然后执行
```
adk web
```
等待adk设置本地伺服器，然后拷贝本地链路伺服器的url（形如http://127.0.0.1:8000/），在浏览器打开这个url。

在左上角选择"basketball_coach"作为对话agent。
![the left button](asset/readme_visual_aid1.png)


然后就可以开始使用啦。

[参考官方文档](https://adk.wiki/get-started/quickstart/#run-your-agent)
可以透过adk web右上角的export来储存对话结果

## 你可能遇到的问题（待完善）：
1. 缺少SSL认证
在命令行中运行
```
export SSL_CERT_FILE=$(python -m certifi)
```
你可能需要先pip install certifi

2. json codenc...decoding...
.env 的encoding make sure as utf-8，你可以用记事本打开然后修改编码然后再重命名为.env

3. adk web ui出现报错信息
重新提交你的问题