import os, json, pandas as pd
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from CDS_JSON_PROMPT import CDS_JSON_PROMPT

load_dotenv()

client_id = os.getenv("AICORE_CLIENT_ID")
auth_url = os.getenv("AICORE_AUTH_URL")
client_secret = os.getenv("AICORE_CLIENT_SECRET")
resource_group = os.getenv("AICORE_RESOURCE_GROUP")
base_url = os.getenv("AICORE_BASE_URL")
deployment_id = os.getenv("DEPLOYMENT_ID")

llm = ChatOpenAI(deployment_id=deployment_id, temperature=0)

csv_path = r"C:\Users\LakshmanNavaneethakr\Downloads\BW-DS\Local\Input\Text\csv\Text_Sales.csv"
df = pd.read_csv(csv_path)
csv_data = df.to_string(index=False)

prompt_template = PromptTemplate(
    input_variables=["csv_data"],
    template=CDS_JSON_PROMPT
)

chain = LLMChain(llm=llm, prompt=prompt_template)
response = chain.invoke({"csv_data": csv_data})
text = response.get("text", "").strip()
print(text)

json_output = json.loads(text)

entity_name = list(json_output.get("definitions", {}).keys())[0]
json_path = os.path.join(os.path.dirname(csv_path) or ".", f"{entity_name}_datasphere.json")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_output, f, indent=2, ensure_ascii=False)

