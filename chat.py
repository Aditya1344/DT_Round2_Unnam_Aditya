import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# --- Load API key ---
load_dotenv()
SAMBA_API_KEY = os.getenv("SAMBA_API_KEY")

# --- Setup OpenAI client with SambaNova endpoint ---
client = OpenAI(
    api_key=SAMBA_API_KEY,
    base_url="https://api.sambanova.ai/v1"
)

# --- Quiz generation function ---
def generate_quiz(topic, format="short answer", difficulty="easy"):
    prompt = f"""
    You are a helpful AI tutor. Generate 3 {format} quiz questions on the topic '{topic}'.
    All 3 questions should match this difficulty level: {difficulty}.
    After each question, provide the correct answer in markdown as well.

    Use this format exactly:
    **Question 1:** ...
    **Answer 1:** ...
    **Question 2:** ...
    **Answer 2:** ...
    **Question 3:** ...
    **Answer 3:** ...

    Keep the explanations clear and use markdown formatting.
    """

    response = client.chat.completions.create(
        model="Meta-Llama-3.1-405B-Instruct",
        messages=[
            {"role": "system", "content": "You are a friendly quiz generator for students."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# --- Streamlit UI ---
st.set_page_config(page_title="AI Quizbot", layout="centered")
st.title("🧠 AI Study Coach")

with st.form("quiz_form"):
    topic = st.text_input("Enter a topic:", value="")
    format = st.selectbox("Question format:", ["short answer", "MCQ"])
    difficulty = st.selectbox("Difficulty level:", ["easy", "medium", "mixed"])
    submit = st.form_submit_button("Generate Quiz")

if submit and topic.strip():
    with st.spinner("Contacting SambaNova..."):
        result = generate_quiz(topic, format, difficulty)
        st.markdown(result)
elif submit:
    st.error("Please enter a topic first.")
