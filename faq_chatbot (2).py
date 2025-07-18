import streamlit as st
import pandas as pd
import os
from sentence_transformers import SentenceTransformer, util
import datetime

st.set_page_config(page_title="College FAQ Chatbot Pro", page_icon="🤖")
st.title("🎓 College FAQ Chatbot – Pro Version")
st.write("Ask me anything about the college, and I'll try my best to help you!")

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

st.sidebar.header("📥 Upload FAQs")
uploaded_faq = st.sidebar.file_uploader("Upload a CSV file with 'question' and 'answer' columns", type=["csv"])

if uploaded_faq:
    faq_df = pd.read_csv(uploaded_faq)
else:
    faq_df = pd.DataFrame({
        "question": [
            "When are semester exams?",
            "What are the library hours?",
            "How to apply for admission?",
            "Hostel contact number?",
            "What is the college address?"
        ],
        "answer": [
            "Semester exams start on 15th November.",
            "Library is open from 8 AM to 8 PM, Monday to Saturday.",
            "Admissions are open through the official SSPU portal.",
            "Hostel office contact: +91-1234567890",
            "Department of Technology, SSPU, Pune - 411052."
        ]
    })

faq_embeddings = model.encode(faq_df['question'].tolist(), convert_to_tensor=True)

query = st.text_input("You:")

if query:
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, faq_embeddings)[0]
    best_idx = scores.argmax().item()
    best_score = scores[best_idx].item()

    if best_score > 0.6:
        matched_question = faq_df['question'].iloc[best_idx]
        matched_answer = faq_df['answer'].iloc[best_idx]
        st.markdown(f"**Bot:** {matched_answer}")
    else:
        matched_question = "No match"
        matched_answer = "Sorry, I couldn't find a good match. Please contact the admin."
        st.warning("Bot: Sorry, I couldn't find an answer for that.")

    log_file = "chatbot_log.csv"
    log_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "matched_question": matched_question,
        "answer": matched_answer,
    }

    if os.path.exists(log_file):
        pd.concat([pd.read_csv(log_file), pd.DataFrame([log_entry])]).to_csv(log_file, index=False)
    else:
        pd.DataFrame([log_entry]).to_csv(log_file, index=False)

    st.markdown("#### 📢 Was this helpful?")
    feedback = st.radio("Your feedback:", ["Yes", "No"], horizontal=True)
    if st.button("Submit Feedback"):
        feedback_data = pd.read_csv(log_file)
        feedback_data.at[len(feedback_data) - 1, "feedback"] = feedback
        feedback_data.to_csv(log_file, index=False)
        st.success("✅ Feedback recorded. Thank you!")

if st.sidebar.checkbox("📊 View Logs"):
    if os.path.exists("chatbot_log.csv"):
        st.sidebar.write(pd.read_csv("chatbot_log.csv"))
    else:
        st.sidebar.info("No logs yet.")