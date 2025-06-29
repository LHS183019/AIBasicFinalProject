<div align="center">

# 🏀 GlideHoop — Your Basketball Companion 🐧
[![License][License-image]][License-url]
[![Latest Pre-release][Releases-image]][Releases-url]
[![Downloads][Installation-image]][Installation-url]
![Python 3.11][PythonVersion-image]

[![Page][page-image]][page-url]
[![Tech Report][report-image]][report-url]

🌐 **English** &nbsp;|&nbsp; [简体中文](README.md)
</div>

[page-image]: https://img.shields.io/badge/Page-know_more-black?style=flat-square
[License-image]: https://img.shields.io/github/license/LHS183019/AIBasicFinalProject?style=flat-square&color=brown
[Releases-image]: https://img.shields.io/github/v/release/LHS183019/AIBasicFinalProject?include_prereleases&sort=semver&color=orange&label=Latest%20Pre-release
[Installation-image]: https://img.shields.io/github/downloads/LHS183019/AIBasicFinalProject/total?style=flat-square&color=blue
[PythonVersion-image]: https://img.shields.io/badge/Python-3.11-yellow?style=flat-square&labelColor=blue
[report-image]: https://img.shields.io/badge/Tech_report-download-black?style=flat-square

[page-url]: https://lhs183019.github.io/AIBasicFinalProject/
[License-url]: https://github.com/LHS183019/AIBasicFinalProject/blob/main/COPYING
[Releases-url]: https://github.com/LHS183019/AIBasicFinalProject/releases
[Installation-url]: https://github.com/LHS183019/AIBasicFinalProject/releases
[PythonVersion-url]: https://github.com/LHS183019/AIBasicFinalProject/pulls
[report-url]: https://github.com/LHS183019/AIBasicFinalProject/blob/main/aibasis_report/main.pdf

---

## ✨ Latest Updates (v1.4.1 - 2025.06.29)
<div align="center">

| Type            | Description                                                                           |
| :-------------- | :------------------------------------------------------------------------------------ |
| 🐛 Bug Fix      | Fixed the issue where strategy generation was incomplete.                             |
| ⚡ Optimization | Optimized local library management and image generation features for better usability. |
| 📚 Docs Update  | Initial user guide is now live.<br>README updated with demonstrations, installation guide, and FAQs. |
| 🧹 Code Cleanup | Removed some redundant code.                                                        |

</div>

## 📖 Release History

<details>
  <summary><b>v1.4.0 (2025.06.27)</b></summary>
  
+ 🎉 Initial Public Release: Core functionalities are online.
</details>

<details>
  <summary><b>v1.0.0 - v1.3.0</b></summary>
  
  + Internal development phase, not publicly released.
</details>

## 💡 Coming Soon

<details>
  <summary><b>Personified Agent Assistant!</b></summary>
  
  + Will give your GlideHoop team engaging personality settings.
  + Fix inconsistent Agent response styles for an improved experience.
</details>

<details>
  <summary><b>WNBA, NBA Encyclopedia</b></summary>
  
  + Integrate the balldontlie API into our search browser for more professional player encyclopedias.
  + Update our search browser's web search functionality for sites like Basketball Reference, providing real-time player information.
</details>

<details>
  <summary><b>Basketball Shoe Shopping Guide 👟</b></summary>
  
  + Update the RAG corpus to provide professional purchasing advice.
</details>

---
## ✨ Feature Demonstrations

<details open>
  <summary><b>🤔 Hi~ I'm confused about a certain term.</b></summary>

  ![ask agent](asset/vshow1.gif)

  👨‍💻 Let's call a dedicated browser to look up information.

  ![agent draw pic](asset/vshow2.gif)

  👩‍🎨 And let the little coach draw an illustration for you.

</details>

<details>
  <summary><b>😵 Can you help me make a memo about everyone's playstyle on the team?</b></summary>

  ![agent manage database](asset/vshow3.gif)

  👨‍🏭 Yes, absolutely! We have a reliable player data manager!
</details>

<details>
  <summary><b>🏋️ Coach, I want to improve my skills.</b></summary>

  ![agent plan training](asset/vshow4.gif)

  🏃 Coming right up~

</details>

<details>
  <summary><b>🎞️ Video Replay: Mark the highlights!</b></summary>

  ![agent whatching vid](asset/vshow5.gif)

  Let us pinpoint the key moments for you, so you can save time and watch a second video!

</details>

<details>
  <summary><b>🧠 Help me strategize!</b></summary>

  ![agent drawing strategy](asset/vshow6.gif)

  🧑🏻‍🏫 No problem! When your team faces the opposing team, what kind of tactical sparks will ignite? (Analysis will be combined with your local database.)

</details>

<details>
  <summary><b>More Features...</b></summary>
  And there's more...
  * [Full Feature Description](https://lhs183019.github.io/AIBasicFinalProject/)

  + Or, do you have any suggestions? Feel free to share them with us!
</details>

## 🆓 Request a Free Trial!

Currently, some core functionalities of GlideHoop rely on our corpus and cloud services deployed on Google Cloud. Therefore, we temporarily need to provide you with authorized access.

If you are interested in GlideHoop and wish to get early access, please feel free to contact us via the email below to request a trial. We will respond as soon as possible:

* 📧 **lhs183019@gmail.com**

Thank you for your support! We understand the importance of local deployment and will soon provide a solution that allows GlideHoop to run **entirely locally**. Stay tuned! 💡

## 🔥 Get Started on Your Computer

Follow these steps to easily set up GlideHoop🐧

#### Environment Configuration

**Step 1: Download our source code to your computer.**

[Download the latest trial version](https://github.com/LHS183019/AIBasicFinalProject/releases/download/v1.4.1/v1.4.1-release.zip) and extract it.

Then, navigate to our root directory via the command line:

```yaml
GlideHoop/   # You should be in this directory
├── basketball_coach/
│   ├── __init__.py
│   └── agent.py
├── requirements.txt
└── .env
```

<br>

**Step 2: Create and Activate a Python Virtual Environment (Recommended)**

Currently, GlideHoop's compatibility with other Python versions is not confirmed. It's best to stick with **Python 3.11**.

<details open>
<summary><b>Using <code>venv</code></b></summary>
<br>

**⚠️ Prerequisite:** Ensure **Python 3.11** is installed on your system. If not, you can download and install it from the [Official Python Website](https://www.python.org/downloads/release/python-3110/).

```bash
# This will create a folder named '.venv' in the current project root directory.
# Make sure you are in the project root directory (e.g., GlideHoop/).
python3.11 -m venv .venv

# Activate the virtual environment
# After activation, your terminal prompt will show '(.venv)', indicating you've successfully entered the virtual environment.
# **Important: You need to reactivate the virtual environment every time you open a new terminal window.**

# For macOS / Linux users:
source .venv/bin/activate

# For Windows CMD users:
.venv\Scripts\activate.bat

# For Windows PowerShell users:
.venv\Scripts\Activate.ps1
```

After activation, your terminal prompt will display `(.venv)`, indicating that you have successfully entered the virtual environment!

</details>

<details>
<summary><b>Using <code>conda</code></b></summary>

```bash
# This will create a new environment named 'glidehoop' (name is customizable) and install Python 3.11.
conda create -n glidehoop python=3.11

conda activate glidehoop
```

After activation, your terminal prompt will display `(glidehoop)`, indicating that you have successfully entered the virtual environment!

</details>

<br>

**Step 3: Install Project Dependencies**

Regardless of whether you chose `venv` or `conda`, run the following command after activating your virtual environment:

```bash
pip install -r requirements.txt # Make sure you are in the root directory mentioned above.
```

Pip will automatically download all dependencies; this may take some time.

<br>

**Final Step: Configure `.env` file**

You need to configure a file named `.env` in the root directory:

```yaml
GlideHoop/
├── basketball_coach/
│   ├── __init__.py
│   └── agent.py
├── requirements.txt
└── .env                   # <-- This needs to be configured
```

You can refer to `.env.example` for its content:

```
SILICONFLOW_API_KEY=your_siliconflow_key (Optional, not strictly necessary)

GOOGLE_CLOUD_PROJECT="basketball-coach-rag"
GOOGLE_CLOUD_LOCATION="us-central1"
GOOGLE_GENAI_USE_VERTEXAI="True"
GOOGLE_APPLICATION_CREDENTIALS="basketball_coach//service_key.json"
RAG_CORPUS = "projects/basketball-coach-rag/locations/us-central1/ragCorpora/4532873024948404224"
```

Then, replace the content of `service_key.json` with the key you obtained earlier.

```yaml
GlideHoop/
├── basketball_coach/
│   ├── __init__.py
│   ├── agent.py
│   └── service_key.json    # <-- Paste your key here
├── requirements.txt
└── .env
```

#### Start the Conversation!

```yaml
GlideHoop/   # In this directory
├── basketball_coach/
│   ├── __init__.py
│   └── agent.py
├── requirements.txt
└── .env
```

Run the following command:

```bash
adk web
```

ADK will set up a local server, and finally print setup information, including the local server's URL (e.g., `http://127.0.0.1:8000/`).

Copy this URL and open it in your browser.

In the top-left dropdown menu, select "basketball_coach" as the conversation agent.

Now you can start debugging and using it!

  - For usage of this interface, please refer to our [Guide](https://lhs183019.github.io/AIBasicFinalProject/)
  - For the design of this interface, you can [refer to the official introduction](https://github.com/google/adk-web?tab=readme-ov-file)

You can also run our Agent in the CLI by changing `adk web` to:

```bash
adk run multi_tool_agent
```

  - **Note:** Running in CLI mode is not recommended as we have not yet fully ensured functional compatibility for this mode.

## 🛠️ Troubleshooting

### 🚨 Configuration Issues

  * **Problem: Missing SSL Certificate**

      * **Solution:** Please run the following command in your terminal to ensure the SSL certificate path is correctly configured.
        ```bash
        # macOS / Linux / Git Bash users:
        export SSL_CERT_FILE=$(python -m certifi)
        # CMD users:
        for /f "del delims=" %i in ('python -m certifi') do set SSL_CERT_FILE=%i
        # PowerShell users:
        $env:SSL_CERT_FILE = python -m certifi
        ```
      * **Tip:** If the `certifi` module is not installed, you may need to run `pip install certifi` first.

  * **Problem: JSON Decoding Error**

      * **Solution:** Please ensure your `.env` file's encoding is **UTF-8**. You can open `.env` with a text editor (like Notepad), manually change its encoding to UTF-8, and then save it.

  * **Problem: JWT Invalid**

      * **Solution:**
        1.  First, please carefully check if you have configured your `service_key.json` file correctly according to the project guidelines.
        2.  If the configuration is correct, it's possible that the key assigned to you has been disabled due to security risks. Please contact us to resend the key 👆.

### 🚧 Functional Bugs

  * **Streaming Response Error: JSON Encoding Error (when using ADK Web)**

      * **Symptom:** When using the streaming response feature in ADK Web, you might occasionally encounter a JSON encoding error.
      * **Temporary Solution:**
          * You can try submitting your query multiple times.
          * Start a new conversation.
          * Temporarily disable streaming response.
          * If you must experience the full streaming response, you can switch to CLI mode.
      * **Additional Info:** This error is likely due to ADK web's handling of long text streams. [See issue here](https://github.com/google/adk-web/issues/74).

  * **Excessive Wait Time for Dialogue Generation**

      * **Symptom:** The dialogue or task generation process takes excessively long, far exceeding expectations.
      * **Temporary Solution:**
          * This is usually caused by momentary errors. Please try resubmitting the current task (even if the Agent tells you the result is being generated).
          * If the issue persists, try starting a new conversation.
      * **Additional Info:** Only **tactical visualization generation** tasks tend to be time-consuming; most other tasks should yield results within 1 minute. You can also monitor the conversation between Agents through the running command line.

  * **Voice Generation Failed**

      * **Symptom:** You are informed that the voice service was unsuccessful.
      * **Cause:**
          * The Gemini-2.5 preview voice service is currently not available or applicable.

We will address the issues above as soon as possible to provide a more stable user experience!
