# 🌱 EnergyInsightGPT

An **AI-powered sustainability intelligence platform** that combines **energy analytics, carbon footprint estimation, document intelligence, and RAG-based conversational AI** into a single interactive application.

Built with **Streamlit + LangChain + FAISS + LLMs**, this project demonstrates real-world **AI + Automation + Sustainability use cases**.

---

## 🚀 Key Features

### 📊 1. Energy Analytics Dashboard

* Upload CSV datasets with energy usage
* Auto-enrichment with emission factors
* Visualizations:

  * Bar charts (Energy & CO₂)
  * Pie chart (Usage distribution)
* AI-generated insights on:

  * High consumption zones
  * Usage anomalies
  * Optimization opportunities

---

### 🌱 2. Carbon Footprint Estimator

* Calculates **monthly & yearly emissions**
* Inputs:

  * Electricity consumption
  * Appliance usage
  * Transport distance
* Uses real emission factors dataset
* Provides **intelligent recommendations** based on emission levels

---

### 🤖 3. AI Chatbot (RAG-enabled)

Supports **3 intelligent modes**:

* **General Mode**

  * Sustainability advice
  * Practical recommendations

* **Data Mode (RAG)**

  * Ask questions on uploaded CSV/report
  * Context-aware answers using FAISS vector search

* **Policy Mode**

  * ESG, carbon tax, government policies
  * Structured expert-level responses

---

### 📄 4. Report Summarizer

* Upload **PDF or TXT reports**
* Extracts and summarizes:

  * Energy inefficiencies
  * Abnormal usage patterns
  * Optimization insights
* Outputs clean bullet-point summaries

---

## 🧠 Architecture Overview

```
                ┌────────────────────────┐
                │     Streamlit UI       │
                └──────────┬─────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
 Energy Engine     Carbon Engine        Summarizer
 (Pandas + AI)     (Emission Logic)     (LLM + PDF)

        ▼
   RAG Pipeline
   ├── Document Loader (CSV/PDF)
   ├── Text Splitter
   ├── Embeddings (MiniLM)
   ├── Vector DB (FAISS)
   └── LLM (Groq / Gemini)

```

---

## 🛠️ Tech Stack

| Layer           | Technology                     |
| --------------- | ------------------------------ |
| UI              | Streamlit                      |
| Data Processing | Pandas                         |
| LLM Framework   | LangChain                      |
| Vector Database | FAISS                          |
| Embeddings      | Sentence Transformers          |
| LLM Providers   | Groq (LLaMA 3) / Google Gemini |
| PDF Processing  | PyPDF                          |
| Visualization   | Matplotlib                     |

---

## 📂 Project Structure

```
EnergyInsightGPT/
│
├── app.py                  # Main Streamlit app 
├── chatbot_module.py      # RAG + chatbot logic 
├── summarizer.py          # Document summarization 
├── carbon_calc.py         # Carbon calculations & insights 
├── llm_provider.py        # LLM configuration (Groq/Gemini) 
├── requirements.txt       # Dependencies 
│
├── energy_data/
│   ├── usage/             # Uploaded CSV files
│   ├── reports/           # Uploaded reports
│   └── carbon_factors_reference/
│
└── README.md              # Documentation :contentReference[oaicite:6]{index=6}
```

---

## ⚙️ Installation

```bash
git clone https://github.com/shubham2k15/EnergyInsightGPT.git
cd EnergyInsightGPT
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
# OR
GOOGLE_API_KEY=your_google_api_key
```

> ⚠️ At least one API key is required for LLM functionality

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📊 How It Works

### Energy Dashboard

* Upload CSV → processed via Pandas → enriched with emission factors → visualized + AI insights

### RAG Chatbot

1. Upload data (CSV or report)
2. Text is chunked & embedded
3. Stored in FAISS vector DB
4. Query → similarity search → LLM generates answer

### Carbon Estimation

* Uses:

  * Energy consumption × emission factors
  * Appliance usage
  * Transport emissions

---

## 🎯 Use Cases

* 🏭 Industrial energy optimization
* 🏢 Building energy analysis
* 🌍 Sustainability consulting
* 📊 ESG reporting support
* 🤖 AI-powered data assistants
* 📄 Automated report intelligence

---

## 🔥 Highlights

* End-to-end **RAG pipeline implementation**
* Real-world **AI + sustainability integration**
* Clean **session-based document handling**
* Multi-mode intelligent chatbot
* Production-ready modular architecture

---

## 🚧 Future Enhancements

* Multi-file RAG support
* Real-time IoT energy integration
* Advanced forecasting (ML models)
* Dashboard export (PDF/Excel)
* Role-based enterprise version

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork, improve, and raise a PR.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Shubham Bhattacharya**
Senior RPA Developer | AI & Automation Enthusiast

* Passionate about **Hyperautomation + Generative AI**
* Building real-world AI-driven solutions

---

## ⭐ If you like this project

Give it a ⭐ on GitHub — it helps others discover it!
