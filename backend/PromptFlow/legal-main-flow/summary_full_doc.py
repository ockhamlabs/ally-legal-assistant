from promptflow.core import tool
from promptflow.connections import AzureOpenAIConnection, CustomConnection
from pydantic import BaseModel 
from openai import AzureOpenAI
from backend.vector_db_client import VectorDBClient
from typing import List  
import json
import time
import logging

class SummaryResponse(BaseModel):  
    class Item(BaseModel):  
        title: str
        summary: str
        notes: str
        original_text: str
        keyItems: List[str]
    Summary: str
    KeyPoints: List[str]
    Items: list[Item]


@tool
def python_tool(input_text: str, ally:CustomConnection) -> object:
    
    client = VectorDBClient()
    results = client.query("*", index="legal-documents", top_k=1000).get("results", [])
    list = []
    for result in results:
        #title,paragraph,keyphrases,summary,isCompliant,CompliantCollection,NonCompliantCollection
        # if is compliant false read the NonCompliantCollection list and run the get_policyinfo function
        if result["isCompliant"] == False:
            policylist = []
            for policyid in result["NonCompliantCollection"]:
                # log into promptflow a warning                
                policy = get_policyinfo(policyid,ally)
                policylist.append(policy)
            list.append({"title": result["title"], "summary": result["summary"], "keyphrases": result["keyphrases"], "summary": result["summary"], "isCompliant": result["isCompliant"], "CompliantCollection": result["CompliantCollection"], "NonCompliantCollection": result["NonCompliantCollection"], "NonCompliantPolicies": policylist})           
        else:    
            list.append({"title": result["title"], "summary": result["summary"], "keyphrases": result["keyphrases"], "summary": result["summary"], "isCompliant": result["isCompliant"], "CompliantCollection": result["CompliantCollection"], "NonCompliantCollection": result["NonCompliantCollection"]})
    print(list)
    return list


def get_policyinfo(policyid: int, ally: CustomConnection):
    client = VectorDBClient()
    response = client.query(
        "*",
        filters={"PolicyId": policyid},
        index="legal-instructions",
        top_k=1,
    )
    results_list = response.get("results", [])
    return results_list[0] if results_list else None
     
