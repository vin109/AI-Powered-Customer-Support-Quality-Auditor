<div align="center">
  <h1>📞 AI Customer Support Quality Auditor</h1>
  <p><i>An Enterprise-Grade, GenAI-powered platform for auditing customer support calls in real-time.</i></p>

  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![Pinecone](https://img.shields.io/badge/Pinecone-Vector_Database-000000?logo=pinecone)](https://www.pinecone.io/)
  [![Ollama](https://img.shields.io/badge/Ollama-Llama_3-black)](https://ollama.ai/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
</div>

---

## 📖 Overview
The **AI Customer Support Quality Auditor** is a GenAI-powered platform that reviews customer support chats and transcripts, assigns quality scores, detects compliance violations, and suggests improvements in real-time. 

By combining a **Cloud RAG pipeline (Pinecone)** with **Local LLMs (Llama 3 via Ollama)**, this platform evaluates tone, empathy, and adherence to company policies, completely automating QA for enterprise support teams.

## ✨ Key Features
- **🤖 GenAI Quality Auditing:** Sentiment-based and rule-based quality scoring for empathy, professionalism, and resolution quality.
- **📚 RAG-Powered Compliance:** Uses Pinecone Vector DB to retrieve and enforce company support policies.
- **🔒 Local LLM Execution:** Powered by local Llama models via Ollama to ensure data privacy and zero API costs.
- **🖥️ Interactive Dashboard:** Beautiful Streamlit UI for uploading transcripts and visualizing performance metrics.
- **📄 Automated Reports:** One-click generation of PDF audit reports complete with scores and AI recommendations.
- **📧 Email Integration:** Instantly distribute generated reports to managers via SMTP.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **AI/LLM:** Llama 3 (via Ollama)
- **Vector DB:** Pinecone (for RAG)
- **Data Engineering:** Pandas, Scikit-learn
- **Reporting:** ReportLab (PDF Generation)
- **Other:** Python `smtplib`

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai/) installed locally with the `llama3` model.
- A [Pinecone](https://www.pinecone.io/) API Key.

### 2. Installation
Clone the repository:
```bash
git clone https://github.com/vinit-your-username/AI-Powered-Customer-Support-Quality-Auditor.git
cd AI-Powered-Customer-Support-Quality-Auditor
```

*(Note: Replace `vinit-your-username` with your actual GitHub username)*

Install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add the following:
```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
EMAIL_ADDRESS=your_sender_email@example.com
EMAIL_PASSWORD=your_app_password
```

### 4. Running the Application
Ensure the Ollama service is running in the background with the model you want to use:
```bash
ollama serve
```

Start the Streamlit dashboard:
```bash
streamlit run dashboard.py
```

## 📸 Screenshots
> **Note:** Add screenshots of your Streamlit Dashboard, Score Visualization, and generated PDF reports here to make your project stand out!
> 
> *Example:* `![Dashboard Screenshot](link_to_your_image)`

## 📁 Project Structure
```text
.
├── dashboard.py               # Main Streamlit application
├── rag_llama_auditor.py       # Core LLM auditing logic 
├── pinecone_rag_engine.py     # Vector DB index/retrieval integration
├── attribute_scoring.py       # Rule-based NLP metrics
├── data/                      # Raw and processed transcript definitions
└── requirements.txt           # Python dependencies
```

## 🔮 Future Scope
- **Audio Transcription:** Direct integration with OpenAI Whisper to process live call audio.
- **Multi-Agent Evaluation:** Specialized AI agents for different departments (Sales, Tech Support, Billing).
- **Batch Processing:** Evaluate hundreds of historical calls asynchronously.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
