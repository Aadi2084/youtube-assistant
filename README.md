# 🎥 youtube-assistant

YouTube Assistant is a Streamlit-powered web app that allows users to ask questions about YouTube videos based on their transcripts. It utilizes **LangChain**, **FAISS**, and **Sentence Transformers** to retrieve and process relevant video content.

## 🚀 Getting Started  
Clone the repository:  
`git clone https://github.com/your-username/youtube-assistant.git && cd youtube-assistant`  

Install dependencies:  
`pip install -r requirements.txt`  

Set up API keys in a `.env` file:  
OPENAI_API_KEY=your_openai_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

Run the app:  
`streamlit run main.py`  

## 📌 Deployment on Streamlit Cloud  
```
Push your code to GitHub:  
git add .
git commit -m "Initial commit"
git push origin main
```
Then, deploy via [Streamlit Community Cloud](https://share.streamlit.io/) by linking your GitHub repository.

## 🛠 Technologies Used  
- **Python** (Backend)  
- **Streamlit** (UI Framework)  
- **LangChain** (LLM Integration)  
- **FAISS** (Vector Database)  
- **Sentence Transformers** (Embeddings)  
- **Mistral-7B via OpenRouter API** (LLM)  
- **YouTubeLoader** (Extracts video transcripts)  
