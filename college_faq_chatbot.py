
import streamlit as st
import pandas as pd
import datetime
from sentence_transformers import SentenceTransformer, util

# Title and setup
st.set_page_config(page_title="College FAQ Chatbot", page_icon="🎓")
st.title("🎓 College FAQ Chatbot")
st.write("Ask a question related to your course, academics, or college services.")

# Load model once
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Load hardcoded FAQs
faq_df = pd.DataFrame({
    "question": [
        "What are the eligibility criteria for BSc in Data Science and AI?",
        "How can I apply for a re-evaluation of my exam papers?",
        "Where can I access previous years' question papers?",
        "How many credits are required to pass each semester?",
        "Who is the academic advisor for 3rd year DS & AI students?",
        "How do I apply for an internship through the college?",
        "Where can I find the placement calendar for this year?",
        "What is the process to submit a mini-project proposal?",
        "Are there any funding opportunities for research projects?",
        "How do I get my transcripts issued from the university?",
        "Can I apply for semester exchange programs abroad?",
        "Where do I report technical issues with online exams?",
        "How is attendance calculated and what is the minimum requirement?",
        "How do I register for elective subjects?",
        "What are the rules regarding backlogs and re-examinations?",
        "Where can I find information on clubs and student organizations?",
        "How do I update my personal details in university records?",
        "How to request a bonafide certificate from the college?",
        "What software/tools are we expected to learn in 3rd year?",
        "Where do I submit my mini project or final project files?"
    ],
    "answer": [
        "You need to have passed 12th grade with Mathematics and at least 60% aggregate marks.",
        "Submit a re-evaluation form through the exam portal within 7 days of result declaration.",
        "Previous years’ papers are available in the library repository and student dashboard.",
        "You must complete a minimum of 24 credits per semester to be promoted.",
        "Dr. A. K. Sharma is the academic advisor for 3rd year Data Science and AI students.",
        "Apply through the Training & Placement cell and fill out the internship request form.",
        "The placement calendar is available on the college website under the T&P section.",
        "Fill the mini-project proposal form and get approval from your subject guide.",
        "Yes, students can apply for research funding through the Innovation Cell.",
        "Apply at the university transcript section with an application and ID proof.",
        "Yes, you can apply through the International Relations Cell with a minimum 8.0 CGPA.",
        "Contact the IT Helpdesk at ithelp@college.edu or visit the Digital Support Lab.",
        "A minimum of 75% attendance is mandatory in each course to appear for exams.",
        "Login to your student portal and select electives under the 'Course Registration' tab.",
        "Backlogs can be cleared in supplementary exams held after regular semesters.",
        "Visit the Student Affairs page on the college website for all club-related info.",
        "Submit a request via the admin office or through the student service portal.",
        "Bonafide certificates can be requested online and are issued within 3 working days.",
        "You will learn Python, R, SQL, TensorFlow, Scikit-Learn, and Power BI in 3rd year.",
        "Upload your project files to the university LMS under the designated course section."
    ]
})

# Encode FAQs
faq_embeddings = model.encode(faq_df['question'].tolist(), convert_to_tensor=True)

# Chat input
query = st.text_input("You:")

if query:
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, faq_embeddings)[0]
    best_idx = scores.argmax().item()
    best_score = scores[best_idx].item()

    if best_score > 0.6:
        matched_answer = faq_df['answer'].iloc[best_idx]
        st.markdown(f"**Bot:** {matched_answer}")
    else:
        st.warning("Bot: Sorry, I couldn't find an answer. Please contact the department.")

# Footer
st.markdown("---")
st.caption("Developed by Soham Gaikwad • Dept. of Technology, SSPU")
