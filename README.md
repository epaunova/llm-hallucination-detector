# 🤖 LLM Hallucination & Robustness Detector (Single & Batch Mode)

[![Streamlit](https://img.shields.io/badge/Streamlit-App-green)](https://share.streamlit.io/epaunova/llm-hallucination-detector/main/hallucination_app.py)


  # 🤖 LLM Hallucination & Robustness Detector

Welcome! This is a lightweight yet powerful **Streamlit** app designed to help you detect when large language models (LLMs) like GPT, Claude, or Mistral start “hallucinating” — that is, generating uncertain or false information.

---

## What’s it all about?

Working with LLMs means dealing with outputs that aren’t always reliable. This app helps you:

- Highlight common phrases that signal hallucinations  
- Manually rate the factual accuracy of any output  
- Run an automatic (simulated) LLM check for quick diagnostics  
- Detect toxic or offensive language to keep things clean  
- Visualize hallucination triggers frequency in an intuitive bar chart  
- Analyze multiple outputs at once in batch mode, with aggregated stats and distributions  

---

## How to use

There are two modes:

### 1. Single output mode

Paste a single LLM output and instantly see all analyses — perfect for quick checks.

### 2. Batch mode

Paste multiple outputs separated by `---`. Get batch-level summaries: how many outputs have hallucinations, toxicity, average factuality, and trigger distributions.

---

## Why use this app?

Because no LLM is perfect. As a product manager, researcher, or developer, you need to know when your model is trustworthy and when it’s not. This is your handy sidekick for spotting hallucinations and toxicity before they cause trouble.

---

## Installation

```bash
pip install streamlit pandas
Running locally
bash
Copy
streamlit run hallucination_app.py
Sample text to test hallucination detection
pgsql
Copy
As far as I know, there is no evidence for this. Some sources claim it is fictional.
Author
Eva Paunova — AI Enthusiast & Product Architect
GitHub | LinkedIn

License
MIT License
