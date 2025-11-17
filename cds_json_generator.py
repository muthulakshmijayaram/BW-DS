import os
import re
import json
import pandas as pd
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from CDS_JSON_PROMPT import CDS_JSON_PROMPT


load_dotenv()

client_id = os.getenv("AICORE_CLIENT_ID")
auth_url = os.getenv("AICORE_AUTH_URL")
client_secret = os.getenv("AICORE_CLIENT_SECRET")
resource_group = os.getenv("AICORE_RESOURCE_GROUP")
base_url = os.getenv("AICORE_BASE_URL")
deployment_id = os.getenv("DEPLOYMENT_ID")


llm = ChatOpenAI(deployment_id=deployment_id)

csv_path = r"C:\Users\Muthulakshmi Jayaram\Desktop\bw_code\Data flow\Input\csv\dataflow.csv"
json_path1 = r"C:\Users\Muthulakshmi Jayaram\Desktop\bw_code\prompt_input\json\Test_Data_Flow.json"
json_path2=r"C:\Users\Muthulakshmi Jayaram\Desktop\bw_code\prompt_input\json\DF_M_0SALARYTY_TEXT.json"

df = pd.read_csv(csv_path)
csv_data = df.to_string(index=False)


with open(json_path1, "r", encoding="utf-8") as f:
    json_input1 = json.load(f)

with open(json_path2, "r", encoding="utf-8") as f:
    json_input2 = json.load(f)
prompt_template = PromptTemplate(
    input_variables=["csv_data", "json_input1","json_input2"],
    template=CDS_JSON_PROMPT
)


chain = prompt_template | llm 


response = chain.invoke({
    "csv_data": csv_data,
    "json_input1": json_input1,
    "json_input2":json_input2
})


llm_text = response.content.strip()


if llm_text.startswith("```json"):
    llm_text = re.sub(r"^```[a-zA-Z]*\n", "", llm_text)
    llm_text = re.sub(r"\n```$", "", llm_text)

print("🔹 LLM Output:\n", llm_text)


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

os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, output_file)


with open(output_path, "w", encoding="utf-8") as f:
    json.dump(json_output, f, indent=4, ensure_ascii=False)

print(f"\n✅ JSON successfully written to:\n{output_path}")
