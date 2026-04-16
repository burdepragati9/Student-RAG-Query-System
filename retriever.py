class Retriever:

    def __init__(self, collection, model):
        self.collection = collection
        self.model = model

    def query(self, query):

        query_embedding = self.model.get_embeddings([query]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=50
        )

        return results
