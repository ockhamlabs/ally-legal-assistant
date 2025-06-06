
from promptflow.core import tool
from promptflow.connections import CustomConnection
from backend.vector_db_client import VectorDBClient

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def list_policy_tool(searchconnection: CustomConnection) -> object:
    client = VectorDBClient()
    results = client.query("*", index="legal-instructions", top_k=1000).get("results", [])
    policy_list = []
    for result in results:
        policy_list.append({"title": result.get("title"), "instruction": result.get("instruction")})
        
    return policy_list

