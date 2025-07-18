
import streamlit as st
from difflib import get_close_matches

st.set_page_config(page_title="College FAQ Chatbot", page_icon="🎓")
st.image("https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Savitribai_Phule_Pune_University_Logo.png/250px-Savitribai_Phule_Pune_University_Logo.png", width=100)
st.title("🎓 College FAQ Chatbot")
st.write("Ask me your questions about the college. I’ll try my best to help!")

# Session state for context memory
if 'last_topic' not in st.session_state:
    st.session_state.last_topic = None

# FAQ database with tags
faq_data = [
    {
        "tags": ["exam", "date", "schedule", "test"],
        "answer": "Semester exams start on 15th November."
    },
    {
        "tags": ["exam timetable", "exam time table"],
        "answer": "The exam timetable is usually released a week before exams."
    },
    {
        "tags": ["library", "timing", "open", "hours"],
        "answer": "Library is open from 8 AM to 8 PM, Monday to Saturday."
    },
    {
        "tags": ["admission", "how to apply", "enroll", "apply"],
        "answer": "Admissions are open through the official SSPU portal."
    },
    {
        "tags": ["hostel", "contact", "warden"],
        "answer": "Hostel office contact: +91-1234567890"
    },
    {
        "tags": ["college", "location", "address"],
        "answer": "Department of Technology, SSPU, Pune - 411052."
    }
]

# Text input from user
user_input = st.text_input("You:").lower()

# Dropdown to explore FAQs manually
with st.expander("📚 Browse FAQs"):
    options = [', '.join(faq['tags']) for faq in faq_data]
    browse = st.selectbox("Select a topic:", options)
    if browse:
        for faq in faq_data:
            if browse.split(',')[0] in faq['tags']:
                st.markdown(f"**Bot:** {faq['answer']}")

# Core logic
if user_input:
    found = False
    for faq in faq_data:
        for tag in faq['tags']:
            if tag in user_input:
                st.write("**Bot:**", faq['answer'])
                st.session_state.last_topic = tag
                found = True
                break
        if found:
            break

    # Contextual fallback
    if not found and "timetable" in user_input and st.session_state.last_topic == "exam":
        st.write("**Bot:**", "Do you mean the exam timetable? It's usually released a week before exams.")
        found = True

    # Fuzzy matching fallback
    if not found:
        all_tags = [tag for faq in faq_data for tag in faq['tags']]
        matches = get_close_matches(user_input, all_tags, n=1, cutoff=0.6)
        if matches:
            for faq in faq_data:
                if matches[0] in faq['tags']:
                    st.write("**Bot:**", faq['answer'])
                    found = True
                    break

    if not found:
        st.warning("Bot: Sorry, I couldn't find an answer for that. Please contact the admin.")

# Feedback system
st.markdown("---")
st.subheader("📢 Feedback")
feedback = st.radio("Was this helpful?", ("Yes", "No"))
if st.button("Submit Feedback") and feedback:
    st.success("Thank you for your feedback!")
