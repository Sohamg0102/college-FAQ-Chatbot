# 🎓 College FAQ Assistant – Department of Technology, SSPU

This is a user-friendly FAQ chatbot web app designed to assist students with queries related to college admission, courses, fees, campus, and placement for the **Department of Technology, SPPU**.

## 🚀 Features

- Semantic search using Sentence Transformers
- Search by domain (e.g., Fee Structure, Campus Overview, Courses, Placements)
- Intelligent chatbot interface for custom questions
- Clean UI built with Streamlit

## 🗂️ File Structure

```
📁 your_project/
├── app.py               ← Main Streamlit chatbot application
├── faq_data.csv         ← Dataset with FAQs (must contain `domain`, `question`, `answer` columns)
├── README.md            ← Project overview and instructions
├── requirements.txt     ← Python dependencies for the project
```

## 📦 Installation

1. **Clone this repo or download files manually**
2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the app**

```bash
streamlit run app.py
```

## 🧾 Format for `faq_data.csv`

Ensure your `faq_data.csv` contains the following columns:

| domain           | question                                | answer                                      |
|------------------|-----------------------------------------|---------------------------------------------|
| Fee Structure    | What is the fee for BSc Data Science?   | ₹85,000 per year                            |
| Campus Overview  | Is there Wi-Fi on campus?               | Yes, the campus is fully Wi-Fi enabled.     |

## 📌 Notes

- The model used is `all-MiniLM-L6-v2` from SentenceTransformers.
- If your question doesn't match with enough confidence, the bot will prompt you to rephrase.

## 👨‍💻 Author

Made with ❤️ by **Soham Gaikwad**  
*BSc Data Science & AI | Dept. of Technology, SSPU*