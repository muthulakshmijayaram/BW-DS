CDS_JSON_PROMPT = """
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