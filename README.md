# 🤖 Gemini-README-Gen: AI-Powered Documentation

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub Actions workflow status](https://img.shields.io/badge/GitHub_Actions-In_Progress-orange)](https://github.com/SuranjithNK/Gemini-README-Gen/actions)

## ✨ Overview

**Gemini-README-Gen** is an AI-powered GitHub Action that automates the creation of high-quality, comprehensive `README.md` files for any repository. By leveraging the **Gemini API's** deep understanding of code, this tool scans your project structure and existing files to generate documentation that is both accurate and engaging.

Saves developers countless hours of manual documentation work, ensuring every project on your profile is professionally presented.

## 🚀 Key Features

* **Intelligent Analysis:** Scans the repository's files (`package.json`, `.py` files, etc.) to infer the technology stack and purpose.
* **Gemini API Integration:** Uses a powerful large language model to generate detailed sections like Installation, Usage, and Project Structure.
* **GitHub Action:** Seamlessly integrates into your CI/CD workflow to run automatically or on-demand.
* **Professional Output:** Generates clean Markdown with clear headings and formatting.

## ⚙️ Installation & Setup

To use this action in your repository, follow these steps:

### Step 1: Get Your Gemini API Key

1.  Get an API key from [Google AI Studio or your preferred platform].
2.  In your GitHub repository, go to **Settings** -> **Secrets and variables** -> **Actions**.
3.  Click **New repository secret**.
4.  Set the **Name** to `GEMINI_API_KEY`.
5.  Paste your API key into the **Value** field and click **Add secret**.

### Step 2: Create the Workflow File

Create a new file in your repository at the path: `.github/workflows/generate_readme.yml`.

### Step 3: Add Action Usage

Paste the following YAML content into your new workflow file (we will create this file in the next section).

```yaml
name: 'Generate README'

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install google-genai
      - name: Run README Generator Script
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python src/generator.py
      - name: Commit and Push Changes
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: 'docs: Automated README update via Gemini-README-Gen'
          file_pattern: 'README.md'
