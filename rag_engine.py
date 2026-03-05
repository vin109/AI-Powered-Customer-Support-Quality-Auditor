import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Create Chroma client
client = chromadb.Client()

collection = client.create_collection(name="support_policies")


# Load policies
with open("support_policies.txt", "r") as f:
    policies = f.readlines()

# Store embeddings
for i, policy in enumerate(policies):
    collection.add(
        documents=[policy],
        ids=[str(i)]
    )


def retrieve_context(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    return "\n".join(results['documents'][0])
