
# Ally - AI Contract Assistant

### Solution Overview 

__Ally – AI Contract Assistant__ is a contract analysis and review tool featuring a Word plugin that uses Azure OpenAI Service for analyzing contracts, real-time Q&A, and auto-markup based on legal policies. It helps legal professionals converse naturally, verify clauses, identify risks, and ensure consistency in reviews, saving time and boosting efficiency. 

__Ally – AI Contract Assistant__  is an innovative solution meticulously crafted to transform the landscape of contract analysis and review for legal professionals. This sophisticated tool harnesses the power of advanced artificial intelligence to streamline the intricate processes of document summarization, comprehensive contract analysis and review, legal policy compliance verification, and the application of corrections and redlining. By integrating seamlessly with Microsoft Word within the Office 365 suite, the plugin provides a native and intuitive user experience. 

At the heart of this plugin is the robust infrastructure of Azure, coupled with Azure AI’s cutting-edge capabilities, delivering an unparalleled end-to-end contract analysis and review solution. This integration not only enhances the speed and accuracy of contract processing but also ensures that legal professionals can focus on more strategic aspects of their work. 

__Ally – AI Contract Assistant__  is designed with flexibility and scalability in mind. Its open-source code base allows organizations to tailor the solution to their unique requirements, offering a customizable platform that can evolve alongside changing business needs. Whether deployed in a local environment or within a larger cloud-based infrastructure using Docker and Azure Kubernetes Service (AKS), this plugin adapts to diverse IT architectures, ensuring optimal performance and reliability. 

By leveraging this plugin, legal professionals can significantly reduce the time spent on manual tasks, thereby increasing overall productivity and enabling a sharper focus on delivering value to clients. Embrace the future of legal technology with a solution that combines Microsoft’s best-of-breed offerings to redefine efficiency and efficacy in legal contract analysis and review. 

## Demo

[![IMAGE ALT TEXT HERE](./files/youtube.png)](https://www.youtube.com/watch?v=-powTAGvKu0)

### Key Features 

- Efficient Contract Analysis & Review: Streamline the process of contract review with AI-driven summarization and analysis. 
- Policy and Compliance Checks: Ensure compliance with company legal policies through integrated policy checks. 
- Customizable Solution: Modify and extend functionalities with access to the open-source code. 

### Business Impact: 

Legal professionals spend about 50% of their time reviewing repetitive contracts, which is a major source of frustration and reduces their ability to focus on strategic tasks. This manual workload negatively impacts employee morale, leading to burnout, high turnover rates and inefficiencies in the contract review process. ​ 

Enabled by the Azure OpenAI Service, Ally – AI Contract Assistant offers significant business impact through contract analysis and review, saving time, and enhancing the delivery of legal services.  

### Industry​

 - Legal / Professional Services​ 

### Personas​ 

- Legal counsel​ 
- Contract management​ 
- Legal operations​ 
- Procurement​ 
- Risk management and compliance​ 
- Regulators​ 
- Professional Services Firms​ 
  
## Key Features  
  
- **Efficient Contract Review:** Streamline the process of contract review with AI-driven summarization and analysis.  
- **Policy and Compliance Checks:** Ensure compliance with company policies through integrated policy checks.  
- **Customizable Solution:** Modify and extend functionalities with access to the open-source code.  
  
## Architecture  
  
  
![High-Level Design](./files/ally-hld.png)

## Prerequisites  
  
To install and run the plugin locally, ensure you have the following:  
  
- Office 365  
- Node.js and NPM  
- Python  
- Visual Studio Code  
- Azure OpenAI with GPT-4o model and Ada-002 for embedding  
- Azure AI Search (Basic tier)  

> [!NOTE]  
> Use Azure OpenAi GPT4o with the `2024-08-06` model version

## Installation
  
**Local Installation:**  
  
1. Ensure all prerequisites are installed.  
2. Clone the repository to your local machine. 
3. Navigate to the solution directory.  
4. Run `npm install` to install dependencies.  
5. Start the plugin with `npm start`.  
6. Start the backend API server:
   ```bash
   pip install -r backend/requirements.txt
   uvicorn backend.api.server:app --reload --port 8000
   ```

    
## Intellectual Property and Licensing  
  
This plugin is free to use and modify by anyone. The GitHub repository is also free to use and change.  
### Vector API Requests

The add-in communicates with the backend configured by `vector-api-endpoint` using JSON payloads. Each request contains a `query_type` field and the backend must return a JSON object with an `answer` property.
  

#### Ask a question (`query_type: 3`)
```json
{
  "query_type": 3,
  "question": "Can we terminate the agreement early?",
  "language": "en",
  "groups": ["<groupId>"]
}
```
Response
```json
{
  "answer": {
    "Answer": "Yes. The contract allows early termination with 30 days notice.",
    "SearchResults": [
      {"title": "Termination clause", "summary": "Clause 12 covers early termination...", "keyphrases": ["early termination", "notice period"]}
    ]
  }
}
```

#### Review selected text (`query_type: 2`)
```json
{
  "query_type": 2,
  "question": "<selected text from Word>",
  "language": "en",
  "group": ["<groupId>"]
}
```
Response
```json
{
  "answer": {
    "PolicyItems": [
      {"title": "Non\u2011compete policy", "summary": "Contract language conflicts with policy...", "relevant_policy_item": "1.2", "suggested_correction": "Replace with ...", "key_phrases": ["non-compete"], "iscompliant": false}
    ],
    "warning": ""
  }
}
```

#### Summarize entire document (`query_type: 1`)
```json
{ "query_type": 1, "filename": "mydoc.docx" }
```
Response
```json
{
  "answer": [
    {"title": "Section 1", "summary": "Overview of the agreement...", "isCompliant": true, "CompliantCollection": ["NDA Policy"], "NonCompliantCollection": [], "keyphrases": ["overview"]}
  ]
}
```

#### Check document index (`query_type: 99`)
```json
{
  "query_type": 99,
  "filename": "mydoc.docx",
  "groups": ["<groupId>"]
}
```
Response
```json
{ "answer": { "Found": true } }
```
The add-in reads `answer.Found` to determine whether the document is already indexed. If `Found` is `false`, users are prompted to upload the document.

## License

This project is released under the MIT license.

## Team

- **Esther Dediashvili** – Senior Solution Specialist – AI Global Black Belt, EMEA
- **Lior Armiev** – Senior Technical Specialist – AI Global Black Belt, EMEA
- **Andrew Mackay** – AI Director – Global Black Belts, CEMA
