
import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Page configuration
st.set_page_config(page_title="SSPU FAQ Assistant", page_icon="🎓")

st.markdown("<h1 style='text-align: center; color: #1f4e79;'>Department of Technology, SSPU</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #444;'>📘 College FAQ Assistant</h3>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("### 🔎 Explore by Category")

# Load model
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Define categories and questions
faq_data = {
    "Fee Structure": {
        "What is the annual fee for BSc in Data Science?": "The annual fee for BSc in Data Science is approximately ₹85,000 per year.",
        "Is there any scholarship available for students?": "Yes, merit-based and government scholarships are available for eligible students."
    },
    "Campus Overview": {
        "What facilities are available on campus?": "Campus has labs, library, auditorium, canteen, and student innovation hub.",
        "Is there Wi-Fi on the campus?": "Yes, the campus is Wi-Fi enabled for all registered students.",
        "What are the hostel facilities like?": "Hostels are equipped with Wi-Fi, study rooms, mess, and 24/7 security."
    },
    "Academics": {
        "What are the subjects in 3rd year for Computer Science?": "Subjects include Operating Systems, Algorithms, DBMS, Software Engineering.",
        "What are the subjects in 3rd year for Data Science?": "Subjects include ML, Big Data, Data Visualization, Deep Learning, Python, R.",
        "What is the placement rate for Data Science?": "The placement rate for Data Science is around 90% with an average package of 6 LPA.",
        "What companies visit for campus recruitment?": "Companies include Infosys, TCS, Wipro, Zensar, Capgemini, and startups in AI.",
        "How do I apply for an internship through the college?": "Apply through the Training & Placement cell and fill out the internship request form.",
        "What software/tools are we expected to learn in 3rd year?": "You will learn Python, R, SQL, TensorFlow, Scikit-Learn, and Power BI in 3rd year.",
        "Where do I submit my mini project or final project files?": "Upload your project files to the university LMS under the designated course section."
    },
    "Departments": {
        "Which departments are available in the college?": "Departments include Computer Science, Data Science, AI & ML, Cybersecurity, E&TC, and Mechanical.",
        "Does the college offer Artificial Intelligence courses?": "Yes, AI is offered as a major specialization under the Data Science department.",
        "Is there a separate department for Cybersecurity?": "Yes, the Cybersecurity department offers both electives and full-time specializations."
    }
}

# Category and question selection
category = st.selectbox("Choose a category:", list(faq_data.keys()))
question = st.selectbox("Select a question:", list(faq_data[category].keys()))
st.markdown(f"#### 🧾 Answer:
{faq_data[category][question]}")

st.markdown("---")
st.markdown("### 💬 Or Ask Your Own Question Below")

# Flatten all questions and answers for embedding
flat_questions = []
flat_answers = []
for domain in faq_data.values():
    for q, a in domain.items():
        flat_questions.append(q)
        flat_answers.append(a)

embeddings = model.encode(flat_questions, convert_to_tensor=True)

# Chat input
user_query = st.text_input("Type your question:")

if user_query:
    user_embedding = model.encode(user_query, convert_to_tensor=True)
    scores = util.cos_sim(user_embedding, embeddings)[0]
    best_idx = scores.argmax().item()
    best_score = scores[best_idx].item()

    st.markdown("💬 **You:** " + user_query)

    if best_score > 0.6:
        st.markdown("🤖 **Bot:** " + flat_answers[best_idx])
    else:
        st.warning("🤖 Bot: Sorry, I couldn't find an answer. Please contact the department.")

st.markdown("---")
st.caption("Made with ❤️ by Soham Gaikwad | BSc Data Science & AI | Dept. of Technology, SSPU")
