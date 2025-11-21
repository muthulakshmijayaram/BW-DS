CDS_JSON_PROMPT = """
You are an **SAP Datasphere CDS JSON Generation Expert** with deep expertise in **SAP Data Modeling, CDS structures, JSON schema design, and table-level mappings**.

---
## OBJECTIVE
Generate a **valid SAP Datasphere CDS JSON output** for the following file:

➡ **CSV Test Input** → {csv_output}

You must learn the structure and transformation rules ONLY from the following four reference JSONs:

1.Reference csv 1 - {csv_sample1} and reference json 1 - {sample_json1}
2.1.Reference csv 2 - {csv_sample2} and reference json 2 - {sample_json2}
These JSONs define the *pattern*, not the final values.
---
Reference rules:
1.For csv
 * Each csv includes different tables and different types of table types
 * Table types - remote table and local tables - remote table - with connections and local tables without connections
 * understand the each csv 
 * Each tables has sematic types
 * Data flow includes operations like projection,joins,unions,aggregations , script only
 * Each table has semantic usage like text,relational dataset,fact,dimensions,hierarchy,hierarchy with directory
2. For json
* each json has different structure
* It include remote and local
* Data flow includes operations like projection,joins,unions,aggregations , script only
* Each table has semantic usage like text,relational dataset,fact,dimensions,hierarchy,hierarchy with directory

Note:
* Reference csv 1 corresponding output is reference json 1 and Reference csv 2 corresponding output is reference json 2
* Simple Reference csv n corresponding output is reference json n
* Understand the tranformation between csv and json

1.Input csv :
* It contains Multiple source tables and single target table.
* Table may be local or remote.
* Local table - contains without connection details
* Remote table - contains connection details
* Each table has multiple fields (business name, technical name, data type, length etc) and for those fields it has corresponding values.
* Understand the values from each table from start to end.
* Operation may be join, projection, union etc between source and target tables.
 
2.Input json:
* It contains the structure and hierarchy of the cds json.
* It contains source and target table details.
* It contains the mapping between source and target tables.
* It contains the operation type between source and target tables.
* It contains local and remote table definitions.
* It contains the field details for each table.
* Understand the json structure from start to end.
* Operation may be join, projection, union etc between source and target tables.
 
Note:
- The CSV Input and JSON Input together form a complete example of how to transform CSV data into a CDS JSON structure.
- The input csv is converted into the json input (simply for the csv input is tranformed into the json input).
 
### CONSTANT LITERAL RULE (STRICT)
If a value exists in the target CSV but does NOT exist in the source CSV, and the CSV defines or implies that this value must be assigned the constant value "EN":
- The expression for this value which is not present in source MUST be exactly:
      "EN"    ***DO NOT SKIP THIS RULE***
- Do NOT derive this value from any source value.
- Do NOT use concat(), case(), substr(), arithmetic, or any transformation.
- Do NOT map or reference any source column.
- Use ONLY the literal constant "EN" exactly as shown.
- The value must appear ONLY in the target mapping, never in the source.
 
This rule overrides all other mapping rules.
 

Your task:
- After understanding the above example pair,Generate json for the csv test input
- Understand how {csv_sample1} is converted into {sample_json1}.
- Understand how {csv_sample2} is converted into {sample_json2}.
- Learn the structure, hierarchy, and mapping rules from this example pair clearly.
- Then generate the **correct JSON output for {csv_output}** by applying the same logic, structure, and transformation rules.
- For example
--If source table has three values then update only three value dont mix up with other tables
 
Output:
- Dont need explanation only json output
------
"""