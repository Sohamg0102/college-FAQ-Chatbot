import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="College FAQ Assistant", page_icon="🎓")
st.markdown("<h1 style='text-align: center; color: #1f4e79;'>Department of Technology, SSPU</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #444;'>📘 College FAQ Assistant</h3>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

@st.cache_data
def load_faq_csv():
    try:
        df = pd.read_csv("faq_data.csv")
        if "domain" not in df or "question" not in df or "answer" not in df:
            st.error("CSV must have columns: domain, question, answer")
            return None
        return df
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")
        return None

df = load_faq_csv()

if df is not None:
    domains = sorted(df["domain"].unique())
    selected_domain = st.selectbox("Choose a domain:", domains)

    domain_df = df[df["domain"] == selected_domain]
    questions = domain_df["question"].tolist()
    answers = domain_df["answer"].tolist()

    selected_question = st.selectbox("Select a question:", questions)
    selected_answer = domain_df[domain_df["question"] == selected_question]["answer"].values[0]
    st.markdown("#### 🧾 Answer:")
    st.write(selected_answer)

    st.markdown("---")
    st.markdown("### 💬 Or Ask Your Own Question")

    embeddings = model.encode(df["question"].tolist(), convert_to_tensor=True)
    user_input = st.text_input("Type your question:")

    if user_input:
        user_embedding = model.encode(user_input, convert_to_tensor=True)
        scores = util.cos_sim(user_embedding, embeddings)[0]
        best_idx = scores.argmax().item()
        best_score = scores[best_idx].item()
        matched_question = df.iloc[best_idx]["question"]

        st.markdown("💬 **You:** " + user_input)

        if best_score > 0.6:
            st.markdown("🤖 **Bot:** " + df.iloc[best_idx]["answer"])
            st.markdown(f'*(Matched question: "{matched_question}")*')
        else:
            st.warning("🤖 Bot: Sorry, I couldn't find an answer. Please contact the department.")

    st.markdown("---")
    st.caption("Made with ❤️ by Soham Gaikwad | BSc Data Science & AI | Dept. of Technology, SSPU")
else:
    st.info("Please upload a properly formatted CSV with columns: domain, question, answer.")