import streamlit as st

#  College FAQ Chatbot - Soham Gaikwad

# FAQ dictionary
faqs = {
    "exam dates": "Semester exams start on 15th November.",
    "library hours": "Library is open from 8 AM to 8 PM, Monday to Saturday.",
    "admission process": "Admissions are open through the official SSPU portal.",
    "hostel contact": "Hostel office: +91-1234567890",
    "college address": "Department of Technology, SSPU, Pune - 411052."
}

faqs = {k.lower(): v for k, v in faqs.items()}

st.title("College FAQ Chatbot")
st.write("Ask me your questions about the college.")

user_input = st.text_input("You:")

if user_input:
    user_input = user_input.lower()
    matched = False
    for key in faqs.keys():
        if key in user_input:
            st.write("Bot:", faqs[key])
            matched = True
            break
    if not matched:
        st.write("Bot: Sorry, I don't know that. Please contact the admin.")
