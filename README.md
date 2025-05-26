# 🎓 Interview Preparation Chatbot

An interactive Streamlit-based application that helps users prepare for interviews through topic-wise multiple-choice questions (MCQs). The app connects to Hugging Face's inference API to dynamically generate MCQs using the `mistralai/Mixtral-8x7B-Instruct-v0.1` model.

## 🚀 Features

- Topic-wise quiz generation with MCQs
- Real-time scoring system with correct/incorrect tracking
- Clean, interactive Streamlit interface
- Uses Hugging Face Inference API for dynamic content
- Reset functionality to start fresh anytime

## 📁 Project Structure

```bash
.
├── app.py              # Main Streamlit app
├── .env                # Contains Hugging Face API token
├── requirements.txt    # List of Python dependencies
└── README.md           # Project documentation
