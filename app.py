# Save this file as app.py
import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="College FAQ Assistant",
    page_icon="🎓",
    layout="wide"
)

# --- 2. UI STYLING AND TITLES ---
st.markdown("<h1 style='text-align: center; color: #1f4e79;'>Department of Technology, SSPU</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #444;'>📘 College FAQ Assistant</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- 3. MODEL LOADING ---
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# --- 4. DATA AND EMBEDDING LOADING ---
@st.cache_data
def load_and_prepare_data(csv_path="faq_data.csv"):
    try:
        df = pd.read_csv(csv_path)
        required_columns = ["domain", "question", "answer"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"CSV must contain columns: {', '.join(required_columns)}")
            return None
        df['embeddings'] = df['question'].apply(lambda q: model.encode(q, convert_to_tensor=True))
        st.success("FAQ data loaded!")
        return df
    except FileNotFoundError:
        st.error(f"File '{csv_path}' not found.")
        return None
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

faq_df = load_and_prepare_data()

# --- 5. MAIN APPLICATION LOGIC ---
if faq_df is not None:
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📂 Choose a Domain")
        domains = sorted(faq_df["domain"].unique())
        selected_domain = st.selectbox("Select a domain:", domains, label_visibility="collapsed")
        domain_df = faq_df[faq_df["domain"] == selected_domain].copy()
        st.markdown("#### 🤔 Common Questions")
        with st.expander("Click to view"):
            for index, row in domain_df.iterrows():
                st.markdown(f"- *{row['question']}*")
    
    with col2:
        st.markdown("#### 💬 Ask Your Own Question")
        user_input = st.text_input("Type your question:", placeholder="e.g., What are the hostel facilities?")
        if user_input:
            user_embedding = model.encode(user_input, convert_to_tensor=True)
            domain_embeddings = torch.stack(domain_df['embeddings'].tolist())
            scores = util.cos_sim(user_embedding, domain_embeddings)[0]
            best_match_index = torch.argmax(scores).item()
            best_score = scores[best_match_index].item()

            st.markdown("---")
            st.markdown(f"**Your Question:** *{user_input}*")

            if best_score > 0.60:
                matched_question = domain_df.iloc[best_match_index]["question"]
                answer = domain_df.iloc[best_match_index]["answer"]
                st.markdown("##### ✅ Best Matched Answer:")
                st.info(answer)
                st.markdown(f"*(Matched question: "{matched_question}")*")
                st.progress(best_score, text=f"Confidence: {best_score:.2f}")
            else:
                st.warning("🤖 Bot: Sorry, no confident answer found. Try rephrasing or contact the department.")

else:
    st.info("Please ensure `faq_data.csv` is in the same directory with columns: domain, question, answer.")

# --- 6. FOOTER ---
st.markdown("---")
st.caption("Made with ❤️ by Soham Gaikwad | BSc Data Science & AI | Dept. of Technology, SSPU")