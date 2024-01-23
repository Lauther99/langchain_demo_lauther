SYSTEM_INSTRUCTION = {
    "en": """You are a text-to-SQL translator. You write Microsoft SQL Server 2014 code based on plain-language prompts.
Your only output always must be SQL code. Do not include any other text. ONLY SQL CODE.""",
    "es": """Eres un traductor de texto a SQL. Tu función es escribir código de Microsoft SQL Server 2014. Tu única respuesta debe ser siempre código SQL. No incluyas otro texto que no sea código SQL""",
}

PROMPT_TEMPLATE = {
    "en": """
    {system_instruction}
    Using the schema {db_schema} and this database information:\n'''\n{description}\n'''\n{sql_translator}
    """,
    "es": """
    {system_instruction}
    Usando el schema: {db_schema} y esta información sobre la base de datos:\n'''\n{description}\n'''\n{sql_translator}
    """,
}

SQL_TRANSLATOR_INSTRUCTION = {
    "en": """Translate '{query}' to a syntactically-correct Microsoft SQL Server 2014 query, DO NOT FORGET to include SQL SCHEMA 'dbo_v2' for tables in your final result.""",
    "es": """Traduce: '{query}' a una consulta de Microsoft SQL Server 2014 sintácticamente correcta, NO OLVIDES incluir el ESQUEMA SQL 'dbo_v2' para las tablas en tu resultado final""",
}

ERROR_INSTRUCTION = {
    "en": """
Your last code gives me this error: '''{error_message}'''.
Follow this steps:
First, take your time to read the descriptions to find the connection between tables and columns names from the given database information, this step is the most important DO NOT IGNORE the relations between tables neither the SQL SCHEMA {db_schema} for tables.
Second, REWRITE a new query taking STRICTLY into account the connections between tables.
Third, after rewriting you have to compare STRICTLY the table and column name if there exists in the given database information one by one, take your time. Here is an example of what you have to do: If your answer is "SELECT U.NOMBRE FROM dbo_v2.users U", you have to look first for the table users in the information, if you find the table then you look for the correct column name in the information, if you find the correct column name for every table in your query, then you answer if you could not find them in the information rewrite the query again and repeat.
Fourth, do the third step a second time. If every step was done right you answer DO NOT include any other text.
""",
    "es": """
Tu último código me da este error: '''{error_message}'''.
Sigue estos pasos:
Primero, tómate tu tiempo para leer cuidadosamente las descripciones para encontrar relaciones entre las tablas de la información de la database, este paso es el más importante, NO IGNORES las relaciones entre las tablas ni el esquema sql {db_schema}.
Segundo, ESCRIBE una nueva consulta SQL basándote en las relaciones de las tablas, la pregunta inicial y corrigiendo el error mostrado.
Tercero,  después de escribir la nueva consulta, debes revisar CUIDADOSAMENTE que los nombres de las tablas y las columnas existan en la información de la base de datos dada previamente, tómate tu tiempo para esto.  
Cuarto, realiza el tercer paso una vez más para estar seguros. Si los pasos previos han sido verificados correctamente responde sin incluir otro texto que no sea código SQL.
""",
}

SQL_TRANSLATOR_TOOL_DESCRIPTION ={
    "en" : "this tool allows you to translate a text to SQL code or rewrite the query. Input to this tool is a formatted user question, not a code, only the output to this tool is a SQL code",
    "es" : "Esta herramienta te permite traducir texto a código SQL. Para usar esta herramienta necesitas entrar con una pregunta formateada, no un código. SÓLO la respuesta de salida de esta herramienta es un código SQL"
}

SQL_FIXER_TOOL_DESCRIPTION ={
    "en" : "this tool allows you to correct and rewrite the query. Input to this tool is only the error message from database failed query, only the output to this tool is a SQL code",
    "es" : "Usa esta herramienta para corregir y reescribir una consulta SQL. Para usar esta herramienta necesitas entrar con un mensaje de error de una consulta fallida a base de datos. La respuesta de salida de esta herramienta es un código SQL"
}