from sentence_transformers import SentenceTransformer
import re
import faiss
import pickle
import os


class RAGEngine:

    def __init__(self, data_path="data/hotel_kb.txt"):

        self.data_path = data_path

        self.raw_text = ""
        self.chunks = []
        self.embeddings = None

        print("Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load Knowledge Base
    def load_data(self):

        with open(self.data_path, "r", encoding="utf-8") as f:
            self.raw_text = f.read()

        return self.raw_text

    # Section-Based Chunking
    def chunk_text(self):

        pattern = r"={10,}"

        sections = re.split(pattern, self.raw_text)

        self.chunks = [
            section.strip()
            for section in sections
            if len(section.strip()) > 50
        ]

        return self.chunks

    # Create Embeddings
    def create_embeddings(self):

        print("Generating embeddings...")

        self.embeddings = self.model.encode(
            self.chunks,
            convert_to_numpy=True
        )

        return self.embeddings

    # Create and Save FAISS Index
    def create_faiss_index(self):

        print("Creating FAISS Index...")

        dimension = self.embeddings.shape[1]

        index = faiss.IndexFlatL2(dimension)

        index.add(self.embeddings)

        os.makedirs("faiss_index", exist_ok=True)

        faiss.write_index(
            index,
            "faiss_index/index.faiss"
        )

        with open(
            "faiss_index/chunks.pkl",
            "wb"
        ) as f:
            pickle.dump(self.chunks, f)

        print("FAISS Index Saved Successfully!")

        return index


if __name__ == "__main__":

    rag = RAGEngine()

    rag.load_data()

    chunks = rag.chunk_text()

    embeddings = rag.create_embeddings()

    rag.create_faiss_index()

    print(f"\nTotal Chunks: {len(chunks)}")
    print(f"Embedding Shape: {embeddings.shape}")

    print("\nFirst Chunk Preview:\n")
    print(chunks[0][:300])