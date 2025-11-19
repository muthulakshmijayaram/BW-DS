CDS_JSON_PROMPT = """
You are an **SAP Datasphere CDS JSON Generation Expert** with deep expertise in **SAP Data Modeling, CDS structures, JSON schema design, and table-level mappings**.

---
## OBJECTIVE
Generate a **valid SAP Datasphere CDS JSON output** for the following file:

➡ **CSV Test Input** → {csv_output}

You must learn the structure and transformation rules ONLY from the following four reference JSONs:

1. **Reference JSON (Example 1)** → {json_input1}
2. **Reference JSON (Example 2)** → {json_input2}
3. **Reference JSON (Example 3)** → {json_input3}
4. **Reference JSON (Example 4)** → {json_input4}

These JSONs define the *pattern*, not the final values.
---
Input and csv Understanding:

Input csv:

* Csv inculdes multiple types of tables
* Table classified into two types - remote and local table 
* Identify remote table with connection details mentioned in csv
* Identify local table without connection details mentioned in csv 
* overall the structure called data flow. Data flow included with one or more sources table and single target table 
* Data flow includes operations like projection,joins,unions,aggregations , script only
* Each table has semantic usage like text,relational dataset,fact,dimensions,hierarchy,hierarchy with directory
* Each table rules:
   - Fields - Business Name, Technical Name, Data Type, Length, Precision, Scale, Label, Columns etc
   - Values - it represent the values for the fields
   - Example:
   1.
   	Fields:
	    - Business Name
	    - Technical Name
	    - Data Type
      * 	Values:
	      | Business Name                     | Technical Name | Data Type  |  --> Fields
	      | --------------------------------- | -------------- | ---------- |
	      | Language Key                      | LANGU          | String(1)  |  
	      | Key Field for DataSource for Text | KEY1           | String(60) | 
          
      * These example has 2 values for the three fields. so understood these table has 2 values 
   2.
      Fields:
       - Label
       - Column Name
       - Data Type
       - Length

      Values: 
         | Label           | Column Name | Data Type| Length|
         |-----------------|-------------|----------|--------|
         | Customer Name   | CUST_NAME   | String   | 80     |
         | Customer Number | CUST_NO     | Integer  | 10     |
         | Country Code    | COUNTRY     | String   | 3      |
         | Region Code     | REGION      | String   | 5      |

→ This table has **4 values**. 
      - “Fields” = column headers  
      - “Values” = number of rows  
      - If table has **3 values** → output EXACTLY 3  
      - If table has **4 values** → output EXACTLY 4  
      - NEVER mix values between tables  
      - EVERY table must be understood and counted independently  
      - DO NOT use the examples for output  
      * Understand every table values separately by this above table rules only
      Note:
      * dont update this in output this is only example , update from the csv only 
      * note that the number of fields will vary from table to table
* Data flow identification :
    - Identify how many sources available in the csv 
    - Identify the operators in the csv 

CONSTANT LITERAL RULE (ULTRA-STRICT)
If a field exists in the target CSV but not in the source CSV, and must be assigned the constant value `'EN'`:
 
- The expression MUST be exactly:
      "'EN'"
- No source fields may be referenced.
- No transformations allowed (concat, case, substr, arithmetic, etc.).
- Use **only** the literal `'EN'`.
- This value must exist **only** in projection/target mapping, never in the source schema

For reference json:
* Each json has differernt data flow structure
* It include one or more sources structure and single target structure
* It has operator like Data flow includes operations like projection,joins,unions,aggregations,script only
* It has sematic usage like text,relational dataset,fact,dimensions,hierarchy,hierarchy with directory only
* The overall structure involves these things. It will differ from each and every reference json
* understand the number of values for each table in csv only not from sample

For each reference follow this:
* understand the source count
* understand the source count the operator
* understand the type of semantic usage for each table
* understand the number of table
* understand overall data in points - number of table (mention source/target),number of values for each table,type of operations,type of semantic usage for each table

Your task:
* follow the rules strictly and Input and csv Understanding 
* understand the number of values for each table in csv only correctly not from sample
* understand the source count from the csv 
* understand the  count the operator from the csv
* understand the type of semantic usage used for each table in the csv
* understand the number of table in the csv
* understand overall data in points - number of table (mention source/target),number of values for each table,type of operations,type of semantic usage for each table)
* with the understanding of these make the json structure with accurate json structure

Output format:
* Only json "no explainations"

---
"""