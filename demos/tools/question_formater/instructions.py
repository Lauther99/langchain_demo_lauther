PREFIX = """
You will be given a question and you have to read it carefully, take your time. 
After you read the question use a tool to format the it into correct question.
You have this tools: Variables_name_tool.
"""
INPUT_FORMATER_TOOL_DESCRIPTION = {
    "en": "Use this tool to pre process and format the user question. Input to this tool is the user unformatted question, you DO NOT have to create a dictionary to enter this tool just use the original question as string to use it, output is a question formatted",
    "es": "Usa esta herramienta para pre procesar y formatear la pregunta original del usuario. La entrada a esta herramienta es la pregunta original NO FORMATEADA del usuario, NO DEBES crear un diccionario para entrar a esta herramienta, usa la pregunta original como una cadena. El resultado de salida de esta herramienta es la pregunta formateada.",
}

VARIABLES_FILE_PATH = {
    "en" : "data_variables_en.csv",
    "es" : "data_variables_es.csv"
}

GET_VARIABLE_NAME_FUNCTION = {
    "en": """
        You are a expert petroleum engineer
        You will be asked for this variable: {question}. 
        The following context have two columns, one for 'InputName' and one 'CorrectName'. 
        Use your knowledge and the context to find the most accurate name in the context:
        {context}
        Once you find the name, just answer with the the first 'Name' finded, do not try to do more explanation or a list.
        Answer:""",
    "es": """
        Eres un experto ingeniero especializado en la industria del petróleo.
        Se te va a preguntar por la siguiente variable: {question}.
        Además tienes un contexto con 2 columnas, una con nombre 'InputName' y otra con 'CorrectName':
        {context}
        Lo que harás es usar tu conocimiento como ingeniero de petroleo y el contexto para encontrar el nombre más acertado respecto al nombre incorrecto: '{question}' y una vez que encuentres el nombre correcto en el contexto en la columna 'CorrectName' respondes con ese nombre. NO INTENTES DAR MÁS EXPLICACIÓN O UNA LISTA.
    """,
}
