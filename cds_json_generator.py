import os,re
import json
import pandas as pd
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

csv_path = r"C:\Users\Muthulakshmi Jayaram\Desktop\bw_code\Data flow\Input\csv\dataflow.csv"
df = pd.read_csv(csv_path)
csv_data = df.to_string(index=False)
# print(csv_data)
json_path = r"C:\Users\Muthulakshmi Jayaram\Desktop\bw_code\prompt_input\json\Test_Data_Flow.json"

with open(json_path, "r", encoding="utf-8") as f:
    json_input = json.load(f)
prompt_template = PromptTemplate(
    input_variables=["csv_data","json_input"],
    template=CDS_JSON_PROMPT
)

chain = LLMChain(llm=llm, prompt=prompt_template)
response = chain.invoke({
    "csv_data": csv_data,
    "json_input": json_input
})

llm_text = response.get("text", "").strip()  

if llm_text.startswith("```json"):
    llm_text = re.sub(r"^```[a-zA-Z]*\n", "", llm_text)
    llm_text=re.sub(r"\n```$", "", llm_text)
print(llm_text)
json_output = json.loads(llm_text)


file_name = os.path.basename(csv_path)
base_name = os.path.splitext(file_name)[0]  
output_file = f"{base_name}.json"

if "Text" in csv_path:
    output_folder = r"Local_Table\Output\Text\json"
elif "Data flow" in csv_path:
    output_folder = r"C:\Users\Muthulakshmi Jayaram\Desktop\bw_code\Data flow\Output\json"
else:
    output_folder = r"Local_Table\Output\json"

output_path = os.path.join(output_folder, output_file)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(json_output, f, indent=4,ensure_ascii=False)
