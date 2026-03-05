# GenAI-Powered Customer Support Quality Auditor

## OverviewThis project aims to build a GenAI-powered quality auditing platform that reviews customer
support chats and calls, assigns quality scores, detects compliance violations, and suggests
improvements in real time. By combining NLP, RAG pipelines, and speech-to-text
transcription, the platform leverages LLMs to evaluate tone, empathy, compliance with scripts,
and resolution effectiveness. Designed for enterprises, BPOs, and SaaS companies, the
solution enhances customer experience, ensures compliance, and reduces manual QA
workload.

## Features
- Text preprocessing and normalization
- Sentiment-based quality scoring
- Rule-based quality auditing
- Scalable architecture for GenAI and RAG integration

## Tech Stack
- Python
- Pandas
- Scikit-learn
- NLP

## Project Structure
- data/raw: Original dataset
- data/processed: Preprocessed data
- src: Source code for preprocessing and scoring

## How to Run
1. Clone the repository
2. Install dependencies using `pip install -r requirements.txt`
3. Run preprocessing script
4. Run quality scoring script

## Future Scope
- Audio transcription using Whisper
- LLM-based quality scoring
- RAG-powered compliance audits
