# CraftFlow Pattern Explainer

CraftFlow is an early-stage, AI-assisted crochet learning tool. It helps crocheters make sense of abbreviated written patterns by expanding common crochet terms and generating a short, beginner-friendly explanation.

The project is being developed in connection with Crocheters' Association Uganda. Crocheters have tried the working prototype. Their experience and feedback can help guide its next steps.

## What it does

- Accepts a crochet pattern pasted by the user.
- Expands a small set of common crochet abbreviations.
- Uses the Phi-3 model through Ollama to produce a concise explanation of the supplied instructions.
- Lets users submit optional helpfulness feedback and comments.

CraftFlow is a learning aid, not a substitute for checking the original pattern. AI-generated explanations may be incomplete or incorrect; compare them with the source instructions.

## How it works

The app is built with Streamlit. Before calling the model, it expands abbreviations using a crochet terminology map in `app.py`. It then asks Phi-3 to explain only the supplied pattern, with limits on response length and scope.

The current user-type selector is recorded with feedback but does not yet tailor the generated explanation. Adapting explanations to different skill levels is an area for future development.

## Run locally

You will need Python, [Ollama](https://ollama.com/download), and the Phi-3 model.

In Windows PowerShell, from the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull phi3
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Ollama must be running on the same machine as the app. Open the local URL printed by Streamlit, usually `http://localhost:8501`.

On macOS or Linux, use `python3` if needed and replace `.\.venv\Scripts\python.exe` with `./.venv/bin/python`.

## Feedback and data

When a user clicks **Submit Feedback**, the app appends a row to `feedback.csv` in its working directory. The row includes the timestamp, selected user type, helpfulness rating, original pattern, expanded pattern, generated explanation, and optional comments.

Do not submit patterns or comments that you are not comfortable sharing with the person operating the app. The CSV may contain users' work and feedback; keep it private, restrict access, and do not commit real user submissions to GitHub. Local CSV storage is not a durable or multi-user database.

## Sharing a demo

The current prototype is designed to run locally. A temporary tunnel can make the Streamlit page reachable by people outside your network, but anyone with the link may be able to use it, and the link stops working when the tunnel or host computer stops. Expose only the Streamlit page; do not expose Ollama's port directly to the internet.

A hosted deployment needs a deliberate model-hosting and data-storage setup. Installing the Ollama Python package alone does not provide a running Ollama server or model.

## Current status and future direction

CraftFlow is a working prototype, not a mature or continuously available service. Current work is focused on improving explanation quality, learning from crocheters' feedback, making data handling clearer, and finding reliable resources for ongoing development and hosting.

The longer-term vision is a CraftFlow ecosystem of focused tools for crochet workflows. Possible future modules include yarn estimation, design support, and workflow tools. These are possibilities, not current features or committed delivery dates; community needs and available resources will guide priorities.

## Working in the open

The project plans to share educational materials, public presentations or workshops, and other public-facing updates. User-submitted patterns and comments will not be published as raw data; any shared findings should be aggregated, de-identified, and shared only when appropriate consent has been obtained.

No open-source license has been selected for this repository yet. Public visibility on GitHub does not by itself grant permission to reuse or redistribute the code.
