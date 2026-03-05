import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

# Load API key
api_key = os.getenv("PINECONE_API_KEY")

if not api_key:
    raise ValueError("PINECONE_API_KEY not found in .env file")

# Initialize Pinecone client
pc = Pinecone(api_key=api_key)

index_name = "support-policies"

# Check if index exists, create if not
if index_name not in [i["name"] for i in pc.list_indexes()]:
    print("Creating index...")
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(index_name)

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text):
    return embedding_model.encode(text).tolist()


def upload_policies():
    with open("support_policies.txt", "r") as f:
        policies = f.readlines()

    vectors = []
    for i, policy in enumerate(policies):
        vectors.append({
            "id": str(i),
            "values": embed_text(policy),
            "metadata": {"text": policy.strip()}
        })

    index.upsert(vectors=vectors)
    print("✅ Policies uploaded successfully!")


def retrieve_context(query):
    query_vector = embed_text(query)

    results = index.query(
        vector=query_vector,
        top_k=3,
        include_metadata=True
    )

    contexts = [match["metadata"]["text"] for match in results["matches"]]
    return "\n".join(contexts)


if __name__ == "__main__":
    print("Uploading policies...")
    upload_policies()

    print("\nTesting retrieval...\n")
    print(retrieve_context("Customer is angry and needs urgent help"))
