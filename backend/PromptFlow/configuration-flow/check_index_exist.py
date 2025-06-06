
from promptflow import tool
from promptflow.connections import CustomConnection
from backend.vector_db_client import VectorDBClient

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(filename: str, user_config: object, searchconnection:CustomConnection) -> str:
    client = VectorDBClient()
    filter_data = {"filename": filename}
    response = client.query("*", filters=filter_data, index="legal-documents")
    count = response.get("count", 0)
    return count > 0
