from promptflow.core import tool
from promptflow.connections import CustomConnection
from backend.vector_db_client import VectorDBClient

@tool
def list_policy_tool(query: str, embeding:list, searchconnection: CustomConnection, groups: list) -> object:
    client = VectorDBClient()
    print(type(groups))
    groupssplit = ','.join(groups)
    filter_data = {"groups": groupssplit}
    response = client.query(query, vector=embeding, top_k=1, filters=filter_data, index="legal-instructions")
    policy_list = []
    for result in response.get("results", []):
        policy_list.append({"title": result.get("title"), "instruction": result.get("instruction")})
        
    return policy_list

