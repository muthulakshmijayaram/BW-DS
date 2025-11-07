import os, re, json, pandas as pd
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
load_dotenv()
# Load all environment variables from .env file
client_id = os.getenv("AICORE_CLIENT_ID")
auth_url = os.getenv("AICORE_AUTH_URL")
client_secret = os.getenv("AICORE_CLIENT_SECRET")
resource_group = os.getenv("AICORE_RESOURCE_GROUP")
base_url = os.getenv("AICORE_BASE_URL")
deployment_id = os.getenv("DEPLOYMENT_ID")
os.environ.update({
    "AICORE_CLIENT_ID": client_id,
    "AICORE_AUTH_URL": auth_url,
    "AICORE_CLIENT_SECRET": client_secret,
    "AICORE_RESOURCE_GROUP": resource_group,
    "AICORE_BASE_URL": base_url
})

llm = ChatOpenAI(deployment_id=os.getenv("DEPLOYMENT_ID"), temperature=0, max_tokens=4000)


csv_path = "C:\Users\Muthulakshmi Jayaram\Desktop\bw_code\Sample_Text_u.csv"
df = pd.read_csv(csv_path)
csv_data = df.to_string(index=False)


prompt_template = PromptTemplate(
    input_variables=["csv_data"],
    template="""
You are an SAP Datasphere CDS JSON Expert.

Your task:
1. Infer the most appropriate **entity name** from the CSV schema provided.
   - specfied without any column names and values
   - 

2. Convert the CSV schema into a valid **SAP CDS JSON definition** using this entity name.

STRICT RULES:
- Output must be **pure JSON** (no explanations, no markdown, no code fences).
- Follow SAP CDS structure exactly.

FORMAT TO FOLLOW:

{{
  "definitions": {{
    "text_demo": {{
      "kind": "entity",
      "@EndUserText.label": "text_demo",
      "@ObjectModel.modelingPattern": {{
        "#": "LANGUAGE_DEPENDENT_TEXT"
      }},
      "@ObjectModel.supportedCapabilities": [
        {{
          "#": "LANGUAGE_DEPENDENT_TEXT"
        }}
      ],
      "elements": {{
        "data_1": {{
          "@EndUserText.label": "Data 1",
          "type": "cds.String",
          "length": 100,
          "@Semantics.text": true
        }},
        "data1": {{
          "@EndUserText.label": "Data1",
          "type": "cds.String",
          "length": 100,
          "@Semantics.text": true
        }}
      }},
      "_meta": {{
        "dependencies": {{
          "folderAssignment": "Folder_UOVCXMFT"
        }}
      }}
    }}
  }},
  "version": {{
    "csn": "1.0"
  }},
  "meta": {{
    "creator": "CDS Compiler v1.19.2"
  }},
  "$version": "1.0"
}}
CSV SCHEMA:
{csv_data}


Rules:
- If "Key" = X → "key": true, "notNull": true
- Use “Business Name” as @EndUserText.label
- Convert:
  - String(50) → "type": "cds.String", "length": 50
  - Decimal(10,2) → "type": "cds.Decimal", "precision": 10, "scale": 2
  - Integer → "type": "cds.Integer"
  - Date → "type": "cds.Date"
- Semantics:
  - “Text” → "@Semantics.text": true
  - “Language” → "@Semantics.language": true
- Entity Name:
  - Derive from CSV filename (default "entity_demo")
- Always include:
  - "version": {{"csn": "1.0"}}
  - "meta": {{"creator": "CDS Compiler v1.19.2"}}
  - "$version": "1.0"
  - "_meta.dependencies.folderAssignment" with a folder name
  - get entity name from csv only

Output only valid JSON (no explanations).
"""
)


chain = LLMChain(llm=llm, prompt=prompt_template)
response = chain.invoke({"csv_data": csv_data})
text = response.get("text", "").strip()

text = re.sub(r"```(?:json)?|```", "", text).strip()
text = text[text.find("{"): text.rfind("}") + 1]

json_output = json.loads(text)

entity_name = list(json_output.get("definitions", {}).keys())[0]
json_path = os.path.join(os.path.dirname(csv_path) or ".", f"{entity_name}_datasphere.json")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_output, f, indent=2, ensure_ascii=False)


print(json.dumps(json_output, indent=2, ensure_ascii=False))
