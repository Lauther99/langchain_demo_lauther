PREFIX = """
You will be given a question and you have to read it carefully, take your time. 
After you read the question use a tool to format the it into correct question.
You have this tools: Variables_name_tool.
"""
INPUT_FORMATER_TOOL_DESCRIPTION = "Use this tool to pre process and format the user question. Input to this tool is the user unformatted question, you DO NOT have to create a dictionary to enter this tool just use the original question as string to use it, output is a question formatted"

VARIABLES_FILE_PATH = "data_variables_en.csv"

GET_VARIABLE_NAME_FUNCTION = """
 You are a expert petroleum engineer
 You will be asked for this variable: {question}. 
 The following context have two columns, one for 'InputName' and one 'CorrectName'. 
 Use your knowledge and the context to find the most accurate name in the context:
 {context}
 Once you find the name, just answer with the the first 'Name' finded, do not try to do more explanation or a list.
Answer:
"""