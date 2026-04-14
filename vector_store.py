import chromadb
import os
import uuid

class VectorStore:

    def __init__(self):
        os.makedirs("./data/vector_store", exist_ok=True)
        self.client = chromadb.PersistentClient(path="./data/vector_store")
        self.collection = self.client.get_or_create_collection(name="students")

    def add_documents(self, documents, embeddings):

        # ✅ avoid duplicate insert
        if self.collection.count() == 0:

            ids = [f"id_{uuid.uuid4().hex[:8]}" for _ in documents]
            texts = [doc.page_content for doc in documents]

            self.collection.add(
                ids=ids,
                embeddings=embeddings.tolist(),
                documents=texts
            )