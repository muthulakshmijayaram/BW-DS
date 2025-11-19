import os
import re
import json
import pandas as pd
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from CDS_JSON_PROMPT import CDS_JSON_PROMPT
from flask import Flask, request, jsonify


load_dotenv()

client_id = os.getenv("AICORE_CLIENT_ID")
auth_url = os.getenv("AICORE_AUTH_URL")
client_secret = os.getenv("AICORE_CLIENT_SECRET")
resource_group = os.getenv("AICORE_RESOURCE_GROUP")
base_url = os.getenv("AICORE_BASE_URL")
deployment_id = os.getenv("DEPLOYMENT_ID")


llm = ChatOpenAI(deployment_id=deployment_id)

app = Flask(__name__)

@app.route("/json_generator",methods=["POST"])
def json_generator():
    csv_path=None
    output_path=None
    try:
        csv_path=request.json.get("csv_path")
        if not csv_path:
            return jsonify({"error":"csv path required"})
        json_path = r"C:\Users\Muthulakshmi Jayaram\Desktop\bw_code\prompt_input\json\DF_M_0COSTCENTER_TEXT.json"
        with open(json_path, "r", encoding="utf-8") as f:
            json_input1 = json.load(f)
        json_path1 = r"C:\Users\Muthulakshmi Jayaram\Desktop\bw_code\prompt_input\json\DF_M_0SALARYTY_TEXT.json"
        with open(json_path1, "r", encoding="utf-8") as f:
            json_input2 = json.load(f)
        json_path2 = r"C:\Users\Muthulakshmi Jayaram\Desktop\bw_code\prompt_input\json\Test_Data_Flow.json"
        with open(json_path2, "r", encoding="utf-8") as f:
            json_input3 = json.load(f)
        json_path3 = r"C:\Users\Muthulakshmi Jayaram\Desktop\bw_code\prompt_input\json\DF_M_0FUNCT_LOC_TEXT.json"
        with open(json_path3, "r", encoding="utf-8") as f:
            json_input4 = json.load(f)
        df=pd.read_csv(csv_path)
        csv_output=df.to_string(index=False)
    
        prompt_template = PromptTemplate(input_variables=["csv_output", "json_input1", "json_input2","json_input3","json_input4"],template=CDS_JSON_PROMPT)
        chain = prompt_template | llm 
        response = chain.invoke({"csv_output": csv_output,"json_input1": json_input1,"json_input2": json_input2,"json_input3":json_input3, "json_input4":json_input4})
        llm_text = response.content.strip()
        if llm_text.startswith("```json"):
            llm_text = re.sub(r"^```[a-zA-Z]*\n", "", llm_text)
            llm_text = re.sub(r"\n```$", "", llm_text)
            print("🔹 LLM Output:\n", llm_text)
            
            json_output = json.loads(llm_text)
            file_name = os.path.basename(csv_path)
            base_name = os.path.splitext(file_name)[0]
            output_file = f"{base_name}.json"
            output_folder = r"C:\Users\Muthulakshmi Jayaram\Desktop\bw_code\Data flow\Output\json"
            os.makedirs(output_folder, exist_ok=True)
            output_path = os.path.join(output_folder, output_file)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(json_output, f, indent=4, ensure_ascii=False)
            
            response_data = {
            "message": "JSON generated successfully",
            "output_path": output_path,
            "output_json": json_output
        }
        status_code = 200

    except Exception as e:
        response_data = {"error": str(e)}
        status_code = 500
    finally:
        print("Request completed.")
        if csv_path:
            print(f"Processed CSV: {csv_path}")
        if output_path:
            print(f"Output saved to: {output_path}")

        return jsonify(response_data), status_code
if __name__ == "__main__":
    app.run(port=5001, debug=True)



