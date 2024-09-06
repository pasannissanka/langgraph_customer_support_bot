from langchain_core.tools import tool
from data.vector_store import VectorStore


@tool
def lookup_policy(query: str) -> str:
    """Consult the company policies to check whether certain options are permitted.
    Use this before making any flight changes performing other 'write' events."""
    vector_store = VectorStore()
    docs = vector_store.retriever.query(query, k=2)
    return "\n\n".join([doc["page_content"] for doc in docs])
