# 開發手冊

## 开发约定Git
接下来的一周需要完成基本功能的实现！
分工就是:
+ UI工程师 - hbc
    + reflex web app的基本实现
        + 实现文字交互功能（文字键入、流式输出、中断输出）
        + 管理chat（新增和删除chat、记住chat的上下文）
        + 模型自选（用户可以切换使用到不同的语言模型）
        + 输出控制（用户选择是否显示长思考、是否使用长思考）
        + API管理（用户储存自己的API）
+ AI工程师 - dyt
    + 多模态模型请求、回应处理
        + 支持VLM（视觉语言模型）(siliconflow和gemini都有)
        + 支持生图模型 (siliconflow和gemini都有)(实现一个就行，多个也可以)
        + 支持听觉语言模型 (only gemini)
        + 支持TTS(文字转语音) (siliconflow)

**预期交付日期：5.24(下周六)**

在我们的repo上面有一个`development`的branch，这里是一个保险作用，以后我们的**开发阶段都在development上进行**，development上还有两个子branch`feature:ui`、`feature:ai`，工程师们pull、push、commit的时候选择自己的子分支！（后面我会把features们merge回development！）

~~交付日期后我会确保一下功能整合没问题再merge到main！

push之前记得更新requiements.txt！（详见下面注意事项）

## 环境配置

我电脑上的python版本为`3.10.16`, 注意，必须需要使用`3.10+`的python（reflex支持原因）。

你需要在工作目录根目录配置.env文件
```
SILICONFLOW_API_KEY=你的siliconflow_key
GEMINI_API_KEY=你的GEMINI_key
OPENAI_AGENTS_DISABLE_TRACING=1
```

以及下载需要用到的一些依赖，在你的环境中运行：
```
pip install -r requirements.txt
```
`requirements.txt`在工作目录中

## 模块说明

### `main.py` 主程序

这个模块由UI工程师负责。

当前的`main.py`只是一个纯例子，你完全可以摒弃这个代码，它只是用来展示各个模块的调用和配合。
最终，你需要根据整个应用的用户交互需求，来实现这个应用的主程序。
更具体的实现方式应该查看**文档链接**里面的reflex部分。


### `ui_manager.py`

这个模块由UI工程师负责。AI工程师也需要了解。

这个模块负责**连接**用户交互界面（UI）和大模型交互的所有方面的沟通。
UI工程师需要实现UIManager的接口功能，而AI工程师开发`model_response_handler.py`时注意调用这些接口来进行对UI的update。

提供的接口包括界面的初始化、更新、展示模型输出等。具体功能有：

- 显示进入和退出应用的信息。
- 显示错误信息。
- 获取用户输入。
- 显示文本、图片和音频输出。
- 处理各种**信号**，如开始显示、结束显示等。

这里的**信号**是一个为增加可扩展性而加入的小机制。
具体来说，UI工程师可以根据UI的具体实践需求 而新增一些客制化的signal的handling:
```python
def handle_signal(self, signal:str):
    if signal == "display_ends":
        print()
        if self.temp_hotkey:
            self.reasoning_style_ouput = False
            keyboard.clear_hotkey(self.temp_hotkey)
    elif signal == "display_starts":
        print(f"输入'{self.hotkey_char}'中止模型输出：")
        self.paused_response_output = False
        self.temp_hotkey = keyboard.add_hotkey(self.hotkey_char,self.termintate_llm_output,suppress=True)
```
然后如果有需要的话，只需和AI工程师沟通，约定signal的发放时机就可以。
```python
def handle_text_response(self, response, UI:UIManager, show_reasoning:bool = True) -> None:
    UI.handle_signal("display_starts")
    for chunk in response:
        if not hasattr(chunk.choices[0].delta,"reasoning_content"):
            show_reasoning = False
        if not chunk.choices:
            continue
        if UI.paused_response_output:
            break
        if chunk.choices[0].delta.content:
            UI.display_text_output(chunk.choices[0].delta.content, reasoning=False)
        if show_reasoning and chunk.choices[0].delta.reasoning_content:
            UI.display_text_output(chunk.choices[0].delta.reasoning_content, reasoning=True)
    UI.handle_signal("display_ends")
```

反过来的，AI工程师也可以向UI工程师表示有什么样的signal需求。(如此一来透过signal就可以保持一些接口上的统一，不用频繁改动原始代码...)

提供了`CLIManager`这一实现案例参考。

### `model_response_handler.py`

这个模块由AI工程师负责。UI工程师也需要了解。

这个模块负责处理大模型返回的响应数据，负责解析模型输出并告知UI的更新时机。
具体功能有：
- 处理文本响应：解析和展示由模型生成的流式文本响应。
- 处理多媒体响应：目前未实现，但未来可以扩展以处理图片、音频等多媒体数据。

处理多媒体响应的一些思路：配置一个专门的路径储存多媒体数据，返回该路径/路径列表。

需要实现对`model_API.py`中不同modelAPI的调用结果的handle。

提供了`SiliconflowModelResponseHandler`的部分实现作为案例参考。


### `model_API.py`

这个模块由AI工程师负责。

这个模块负责与模型API进行交互。它包括发送请求、接收响应以及处理API相关的错误。具体功能有：

- 向模型API发送请求并接收响应。
- 支持不同类型的模型，如文本模型和视觉语言模型（VLM）(未实现)。
- 生成图片：目前未实现，但未来可以扩展以支持图片生成。返回值应该包含生成档案所处的路径。

需要注意的是，不同的API平台支持的模型类型和调用方式不一样，我们尽量统一使用openai的API，但也可能必须使用不一样的库或实现方法。

提供了`SiliconflowModelAPI`和`GeminiModelAPI`的部分实现作为案例参考。

## 注意事项

### 保持沟通
拿不定主意的时候在群里发消息！

### 更新requiements.txt
你在开发过程中可能新增了对一些第三方库的使用，导致需求的更新。如果发生这种情况，建议在push之前在工作路径下面执行:
pipreqs . --encoding=utf8 --force

你可能需要先在当前环境中安装pipreqs这个库:
pip install pipreqs

### 异常处理
你在开发过程中应保证代码的健壮性，做好必要的异常处理（利用try-except语句和raise语句），并多运行和测试自己的代码，以确保实现的所有的类、函数等都是正确的。

```python
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
```
（p.s. V1的原始代码并没有做好充足的异常处理，需要你的改善）

### 代码即文档
注意类、方法、函数、变量命名的可读性。
不要忘记留下必要的docstring和comment。
+ python内置的`typing`可以提供很好用的类型提示（用来生成对 参数、返回值 的类型提示）
+ comment中可以使用特殊标志提高可维护性和可读性
    1. **TODO**:
    - 用于标记需要完成的功能或需要改进的代码部分。通常包含一个简短的描述，说明需要完成的任务。
    
    2. **XXX**:
    - 用于标记危险或需要特别注意的代码部分。它通常用于代码中存在潜在问题或不确定的部分，需要进一步检查或处理。

    3. **HACK**:
    - 用于标记使用了一些临时或不规范的解决方案的代码部分。它通常用于代码中使用了临时或不规范的解决方案的部分，需要在未来进行改进或重构。

    4. **NOTE**:
    - 用于标记需要特别注意或记录的代码部分。它通常用于代码中存在需要特别注意或记录的部分，如重要的逻辑或算法。

    5. **FIXME**:
    - 用于标记需要修复的问题或错误。它通常用于代码中存在明显错误或问题的部分，需要立即修复。

    6. **BUG**:
    - 用于标记已知的bug或问题。它通常用于代码中存在已知的bug或问题的部分，需要在未来进行修复。


### 大模型帮助

在`notes.md`里有一些学习链接可以参考。

积极和编程模型配合，他们可以帮助你：
+ 重构代码
+ 提供代码灵感
+ fix bug
+ 撰写docstring和comment

我用的是CodeGeeX，vscode上可以下载extension
关于代码重构，你可以使用prompt：
```我应该如何重构这部分的代码，使它更符合DRY原则 并且 令代码框架符合SOLID原则```
不过要小心不要让它随便改动原有的类的接口，除非能确保不影响整个应用的协同开发。

## 文档链接
开发过程中你可能会用到的documentation:
+ OpenAI API [doc](https://platform.openai.com/docs/overview) 
需要翻到内地、港澳之外的地方才能访问
+ Gemini API [doc](https://ai.google.dev/gemini-api/docs/openai?hl=zh-cn)
需要翻墙
+ Siliconflow API [doc](https://docs.siliconflow.com/cn/userguide/introduction)
+ Reflex [doc](https://reflex.dev/docs/getting-started/introduction/)
+ Reflex chat template[doc](https://reflex.dev/templates/reflex-chat/)