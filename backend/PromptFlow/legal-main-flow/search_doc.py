from promptflow.core import tool
from promptflow.connections import CustomConnection
from backend.vector_db_client import VectorDBClient

@tool
def search_doc_tool(query: str, embedinginput: list, searchconnection: CustomConnection, filename: str, groups: str) -> object:
    # Connect to the configured vector database
    client = VectorDBClient()
    file_filter = {"filename": filename}
    response = client.query(query, vector=embedinginput, top_k=3, filters=file_filter, index="legal-documents")
    policy_list = []
    for result in response.get("results", []):
        policy_list.append({
            "title": result.get("title"),
            "paragraph": result.get("paragraph"),
            "keyphrases": result.get("keyphrases"),
            "summary": result.get("summary"),
        })

    return policy_list
