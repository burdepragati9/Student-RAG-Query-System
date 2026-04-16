import os
from dotenv import load_dotenv

from loaders.data_loader import load_data
from embeddings.embedding import EmbeddingModel
from vectordb.vector_store import VectorStore
from retriever.retriever import Retriever

from google import genai

# ---------------------------
# LOAD ENV FILE
# ---------------------------
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise Exception("API key not found. Check .env file")

# ---------------------------
# GEMINI CLIENT (NEW SDK)
# ---------------------------
client = genai.Client(api_key=API_KEY)

# ---------------------------
# LOAD DATA
# ---------------------------
documents = load_data()

# ---------------------------
# EMBEDDINGS
# ---------------------------
embed_model = EmbeddingModel()
texts = [doc.page_content for doc in documents]
embeddings = embed_model.get_embeddings(texts)

# ---------------------------
# VECTOR STORE
# ---------------------------
vector_db = VectorStore()
vector_db.add_documents(documents, embeddings)

# ---------------------------
# RETRIEVER
# ---------------------------
retriever = Retriever(vector_db.collection, embed_model)

# ---------------------------
# FINAL ANSWER FUNCTION
# ---------------------------
def final_answer(query):

    results = retriever.query(query)

    if not results["documents"] or not results["documents"][0]:
        return "No data found"

    context = "\n".join(results["documents"][0])

    prompt = f"""
You are a helpful AI assistant.

Context:
{context}

Question:
{query}

Rules:
- Use only given data
- Do calculations if needed (average, count, max, min)
- Give short answer
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"Error: {e}"

# ---------------------------
# CHAT LOOP
# ---------------------------
while True:
    query = input("\nAsk question (type exit): ")

    if query.lower() == "exit":
        print("Goodbye 👋")
        break

    print("\nAnswer:\n", final_answer(query))
