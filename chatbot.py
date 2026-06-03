from groq import Groq
from dotenv import load_dotenv
import os
import numpy as np
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# -----------------------------
# Load ENV
# -----------------------------
load_dotenv()

# -----------------------------
# LLM Client
# -----------------------------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------
# RAG CHATBOT CLASS
# -----------------------------
class RAGChatbot:
    def __init__(self):
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        print("Loading FAISS index...")
        self.index = faiss.read_index("faiss_index/index.faiss")

        print("Loading chunks...")
        with open("faiss_index/chunks.pkl", "rb") as f:
            self.chunks = pickle.load(f)

    # -------------------------
    # Retrieve Top K chunks
    # -------------------------
    def retrieve(self, question, k=3):
        query_vector = self.embedding_model.encode([question])
        query_vector = np.array(query_vector).astype("float32")

        distances, indices = self.index.search(query_vector, k)

        results = [self.chunks[i] for i in indices[0]]
        return results

    # -------------------------
    # Generate Answer using Groq
    # -------------------------
    def generate_answer(self, question, context_chunks):
        context = "\n\n".join(context_chunks)

        prompt = f"""
You are a helpful hotel assistant.

Use ONLY the context below to answer the question.
If answer is not in context, say "Information not available in hotel database."

Context:
{context}

Question:
{question}

Answer in a clear and helpful way:
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    # -------------------------
    # Chat Function
    # -------------------------
    def chat(self, question):
        chunks = self.retrieve(question)
        answer = self.generate_answer(question, chunks)
        return answer


# -----------------------------
# RUN CHATBOT
# -----------------------------
if __name__ == "__main__":
    bot = RAGChatbot()

    while True:
        q = input("\nAsk Question (type 'exit' to stop): ")

        if q.lower() == "exit":
            break

        answer = bot.chat(q)
        print("\n" + "=" * 50)
        print("ANSWER:")
        print("=" * 50)
        print(answer)
