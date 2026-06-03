from sentence_transformers import SentenceTransformer
import faiss
import pickle


class Retriever:

    def __init__(self):

        print("Loading Embedding Model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        print("Loading FAISS Index...")
        self.index = faiss.read_index(
            "faiss_index/index.faiss"
        )

        print("Loading Chunks...")
        with open(
            "faiss_index/chunks.pkl",
            "rb"
        ) as f:
            self.chunks = pickle.load(f)

    def search(self, query, top_k=3):

        query_embedding = self.model.encode(
            [query]
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx in indices[0]:
            results.append(
                self.chunks[idx]
            )

        return results


if __name__ == "__main__":

    retriever = Retriever()

    query = input("\nAsk Question: ")

    results = retriever.search(
        query=query,
        top_k=3
    )

    print("\n" + "=" * 60)
    print("TOP RETRIEVED CHUNKS")
    print("=" * 60)

    for i, chunk in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("-" * 50)

        print(chunk[:500])