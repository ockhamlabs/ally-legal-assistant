
from promptflow.core import tool
from promptflow.connections import CustomConnection
from backend.vector_db_client import VectorDBClient

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def list_policy_tool(filename:str, searchconnection: CustomConnection) -> object:
    client = VectorDBClient()
    response = client.query(
        filename,
        index="legal-documents",
        top_k=1,
        filters={"filename": filename},
    )
    count = len(response.get("results", []))
    if count == 0:
        return 0  # not indexed
    else:
        return 1  # indexed
