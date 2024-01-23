PREFIX_INSTRUCTION = {
    "en": """You do not know anything about translating SQL, to answer the user question you have to follow this steps:
Step 1, At first use the "Input_formatter" tool to format correctly the original question. Do not clean the simple quotes from original question.
Step 2, use the "sql_translator" tool to translate text into sql code.
Step 3, use the "sql_db_query" tool to execute the sql query obtained in last step. 
Step 4, give the final answer from database to the original input question.
If you have errors with "sql_db_query", use the "sql_query_fixer" tool until you fix the problem.
""",
    "es": """No sabes nada sobre traducir SQL, para responder la pregunta del usuario tienes que seguir estos pasos:
Paso 1. En primer lugar debes usar la herramienta "Input_formatter" para formatear correctamente la pregunta original. No limpie las citas simples de la pregunta original.
Paso 2, usa la herramienta "sql_translator" para traducir texto a código SQL.
Paso 3, usa la herramienta "sql_db_query" para ejecutar la consulta SQL obtenida en el paso anterior.
Paso 4, proporcione la respuesta final de la base de datos a la pregunta de entrada original.
Si tiene errores con "sql_db_query", usa la herramienta "sql_query_fixer" hasta solucionar el problema.
Tu respuesta final debe ser en español.
""",
}
FORMAT_INSTRUCTIONS = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""
SUFFIX = """Begin!
Question: {input}
Thought:{agent_scratchpad}"""
