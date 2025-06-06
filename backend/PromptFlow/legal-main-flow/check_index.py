
from promptflow import tool
from promptflow.connections import CustomConnection
from backend.vector_db_client import VectorDBClient
@tool
def my_python_tool(filename: str, groups: str, searchconnection:CustomConnection) -> str:
    client = VectorDBClient()
    filter_data = {"filename": filename}
    response = client.query("*", filters=filter_data, index="legal-documents")
    count = response.get("count", 0)
    return count > 0
