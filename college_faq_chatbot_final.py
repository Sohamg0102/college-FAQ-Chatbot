
import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Page configuration
st.set_page_config(page_title="SSPU College FAQ Chatbot", page_icon="🎓")

# College branding
st.markdown("<h1 style='text-align: center; color: #1f4e79;'>Department of Technology, SSPU</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #444;'>College FAQ Chatbot</h3>", unsafe_allow_html=True)
st.markdown("---")
st.write("📚 Ask a question about academics, admissions, campus life, or departments.")

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

faq_df = pd.DataFrame({
    "question": [
        "What is the annual fee for BSc in Data Science?",
        "Is there any scholarship available for students?",
        "What facilities are available on campus?",
        "Is there Wi-Fi on the campus?",
        "What are the hostel facilities like?",
        "What are the subjects in 3rd year for Computer Science?",
        "What are the subjects in 3rd year for Data Science?",
        "What is the placement rate for Data Science?",
        "What companies visit for campus recruitment?",
        "Which departments are available in the college?",
        "Does the college offer Artificial Intelligence courses?",
        "Is there a separate department for Cybersecurity?",
        "How do I apply for an internship through the college?",
        "How do I register for elective subjects?",
        "What is the process to submit a mini-project proposal?",
        "Where can I access previous years' question papers?",
        "How is attendance calculated and what is the minimum requirement?",
        "What software/tools are we expected to learn in 3rd year?",
        "Where do I submit my mini project or final project files?",
        "Can I apply for semester exchange programs abroad?"
    ],
    "answer": [
        "The annual fee for BSc in Data Science is approximately ₹85,000 per year.",
        "Yes, merit-based and government scholarships are available for eligible students.",
        "Campus has labs, library, auditorium, canteen, and student innovation hub.",
        "Yes, the campus is Wi-Fi enabled for all registered students.",
        "Hostels are equipped with Wi-Fi, study rooms, mess, and 24/7 security.",
        "Subjects include Operating Systems, Algorithms, DBMS, Software Engineering.",
        "Subjects include ML, Big Data, Data Visualization, Deep Learning, Python, R.",
        "The placement rate for Data Science is around 90% with an average package of 6 LPA.",
        "Companies include Infosys, TCS, Wipro, Zensar, Capgemini, and startups in AI.",
        "Departments include Computer Science, Data Science, AI & ML, Cybersecurity, E&TC, and Mechanical.",
        "Yes, AI is offered as a major specialization under the Data Science department.",
        "Yes, the Cybersecurity department offers both electives and full-time specializations.",
        "Apply through the Training & Placement cell and fill out the internship request form.",
        "Login to your student portal and select electives under the 'Course Registration' tab.",
        "Fill the mini-project proposal form and get approval from your subject guide.",
        "Previous years’ papers are available in the library repository and student dashboard.",
        "A minimum of 75% attendance is mandatory in each course to appear for exams.",
        "You will learn Python, R, SQL, TensorFlow, Scikit-Learn, and Power BI in 3rd year.",
        "Upload your project files to the university LMS under the designated course section.",
        "Yes, you can apply through the International Relations Cell with a minimum 8.0 CGPA."
    ]
})

faq_embeddings = model.encode(faq_df['question'].tolist(), convert_to_tensor=True)

query = st.text_input("You:")

if query:
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, faq_embeddings)[0]
    best_idx = scores.argmax().item()
    best_score = scores[best_idx].item()

    st.markdown("💬 **You:** " + query)

    if best_score > 0.6:
        matched_answer = faq_df['answer'].iloc[best_idx]
        st.markdown("🤖 **Bot:** " + matched_answer)
    else:
        st.warning("🤖 Bot: Sorry, I couldn't find an answer. Please contact the department.")

st.markdown("---")
st.caption("Project by Soham Gaikwad | BSc Data Science & AI | Dept. of Technology, SSPU")
