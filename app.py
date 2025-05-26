import os
import json
import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Setup Streamlit
st.set_page_config(page_title="Interview Prep Bot", page_icon="🧠", layout="centered")
st.title("🎓 Interview Preparation Chatbot")

# Token check
if not hf_token:
    st.error("Token not found. Check your .env file.")
    st.stop()

model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
try:
    client = InferenceClient(model=model_id, token=hf_token)
    st.success("🔗 Connected to Hugging Face Inference API.")
except Exception as e:
    st.error(f"Failed to initialize InferenceClient: {e}")
    st.stop()

# Debug reset button (useful once to fix corrupted state)
if st.button("🔄 Reset App"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Sidebar topic & stats
topics = [
    "Machine Learning",
    "Data Structures",
    "Python",
    "Generative AI",
    "Computer Vision",
    "Deep Learning"
]
st.sidebar.header("🔍 Select Topic")
topic = st.sidebar.selectbox("Topic:", topics)

# Safely initialize session state
if "questions" not in st.session_state or not isinstance(st.session_state.questions, list):
    st.session_state.questions = []

if "score" not in st.session_state or not isinstance(st.session_state.score, int):
    st.session_state.score = 0

if "correct_count" not in st.session_state or not isinstance(st.session_state.correct_count, int):
    st.session_state.correct_count = 0

if "incorrect_count" not in st.session_state or not isinstance(st.session_state.incorrect_count, int):
    st.session_state.incorrect_count = 0

if "active_question" not in st.session_state:
    st.session_state.active_question = None

if "last_action" not in st.session_state:
    st.session_state.last_action = ""

st.sidebar.markdown("---")
st.sidebar.header("📊 Your Score")
st.sidebar.markdown(f"**Questions:** {len(st.session_state.questions)}")
st.sidebar.markdown(f"**Correct:** {st.session_state.correct_count}")
st.sidebar.markdown(f"**Incorrect:** {st.session_state.incorrect_count}")
st.sidebar.markdown(f"**Points:** {st.session_state.score}")

# Fetch unique MCQ
def fetch_mcq(topic, past_questions=None, max_retries=3):
    if past_questions is None:
        past_questions = set(q["question"] for q in st.session_state.questions)

    prompt_template = (
        f"Generate a multiple-choice question about {topic}. "
        "Return only JSON with keys: question (string), options (4 strings), correct_index (0-based integer). "
        "Make the question unique and different from this list:\n" +
        json.dumps(list(past_questions))
    )

    for _ in range(max_retries):
        try:
            response = client.chat_completion(
                model=model_id,
                messages=[
                    {"role": "system", "content": "You are a helpful MCQ bot that returns JSON only."},
                    {"role": "user", "content": prompt_template}
                ]
            )
            content = response.choices[0].message.get("content", "").strip()
            data = json.loads(content)

            new_question = data.get("question", "").strip()
            if new_question in past_questions:
                continue

            return {
                "question": new_question,
                "options": data["options"],
                "correct_index": data["correct_index"],
                "selected": None,
                "submitted": False
            }

        except Exception as e:
            st.error("❌ Error fetching MCQ")
            st.text(traceback.format_exc())
            return None

    st.warning("⚠️ Couldn't generate a unique question after several tries.")
    return None

# Handle logic based on last action
if st.session_state.last_action == "submit":
    new_q = fetch_mcq(topic)
    if new_q:
        st.session_state.active_question = new_q
    st.session_state.last_action = ""

# Render active question or show start button
q = st.session_state.active_question

if not q:
    if st.button("🧠 Start Interview"):
        new_q = fetch_mcq(topic)
        if new_q:
            st.session_state.active_question = new_q
else:
    st.markdown(f"### ❓ {q['question']}")
    choice = st.radio(
        "Choose your answer:",
        range(4),
        format_func=lambda i: q["options"][i],
        index=q.get("selected", 0),
        key="answer",
        disabled=q["submitted"]
    )
    st.session_state.active_question["selected"] = choice

    if not q["submitted"]:
        if st.button("✅ Submit Answer"):
            q["submitted"] = True
            if choice == q["correct_index"]:
                st.success("✅ Correct! +10 points")
                st.session_state.score += 10
                st.session_state.correct_count += 1
            else:
                correct_ans = q["options"][q["correct_index"]]
                st.error(f"❌ Incorrect. Correct answer: {correct_ans} (-10 points)")
                st.session_state.score -= 10
                st.session_state.incorrect_count += 1

            st.session_state.questions.append(q)
            st.session_state.last_action = "submit"
            st.rerun()  # <== Force rerun after submission
