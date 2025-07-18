# 🎓 College FAQ Chatbot – Pro Version

A smart, Streamlit-based FAQ chatbot powered by sentence embeddings for accurate semantic search.

## ✅ Features

- 💬 Ask questions about the college
- 🔍 Semantic matching using Sentence Transformers
- 📤 Upload your own FAQ CSVs
- 🧠 Default fallback FAQ
- 📝 Logging of interactions and user feedback
- 📊 View feedback log in sidebar

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## 🚀 Run the App

```bash
streamlit run pro_faq_chatbot.py
```

---

## 📄 FAQ CSV Format

```csv
question,answer
What are the library hours?,Library is open from 8 AM to 8 PM.
How to apply for admission?,Visit the SSPU admission portal.
```

---

## 📁 Files Included

- `pro_faq_chatbot.py` – Main app
- `requirements.txt` – Python dependencies
- `sample_faq.csv` – Example FAQ
- `chatbot_log.csv` – Auto-generated log file

---

## 📌 Notes

- Default questions will load if no file is uploaded.
- GPT fallback can be added later if needed.