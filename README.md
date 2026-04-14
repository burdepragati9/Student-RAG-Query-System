# 🎓 Student RAG Query System

This project is a simple **Retrieval-Augmented Generation (RAG)** based system that allows users to query student data stored in a CSV file using natural language.

---

## 🚀 Features

- Load CSV data using DocumentLoader
- Generate embeddings using SentenceTransformers
- Store embeddings in ChromaDB (Vector Database)
- Retrieve relevant student data using semantic search
- Supports smart queries like:
  - Top students
  - Students above/below marks
  - Course-wise filtering
  - Count queries

---

## 📂 Project Structure
RAG_NEW/
│── data/
│   ├── students.csv
│   ├── vector_store/
│
│── loaders/
│   └── data_loader.py
│
│── embeddings/
│   └── embedding.py
│
│── vectordb/
│   └── vector_store.py
│
│── retriever/
│   └── retriever.py
│
│── main.py
---## ⚙️ Technologies Used- Python- LangChain DocumentLoader- SentenceTransformers- ChromaDB (Vector Database)---

## 💻 How to Run```bashpip install -r requirements.txtpython main.py

🧠 Example Queries
how many studentshow many coursesstudents in cs above 70students in it below 60top studentbest student in cs

📌 Output Example
Top Student: Aarti (IT) - 90 marks

🎯 Purpose
This project demonstrates how to build a basic RAG pipeline using structured CSV data for intelligent querying.
