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
```

## 🧠 Topics Supported

- Machine Learning  
- Data Structures  
- Python  
- Generative AI  
- Computer Vision  
- Deep Learning  

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd interview-prep-chatbot
   ```

2. **Create a virtual environment (optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file**

   Create a `.env` file in the project root with:
   ```
   HUGGINGFACEHUB_API_TOKEN=your_token_here
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

## 🛠 Dependencies

- `streamlit`
- `huggingface_hub`
- `python-dotenv`

Install them via:
```bash
pip install streamlit huggingface_hub python-dotenv
```

## 📝 Notes

- You must have access to the Hugging Face Inference API.
- Use your Hugging Face token responsibly to avoid rate limits.

## 📄 License

MIT License
