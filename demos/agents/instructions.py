# FORMAT_INSTRUCTIONS = '''
# Only use the information returned by the below tools to construct your final answer.
# You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

# DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

# If the question does not seem related to the database, answer "I don't know".

# Use the following format:
# Question: input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question and the sql query"""
# '''

# flake8: noqa
PREFIX = """You do not know anything about translating SQL, to answer the user question you have to follow this steps:
Step 1, use the "Input_formatter" tool to format correctly the user question. Always do this first.
Step 2, use the "sql_translator" tool to translate text into sql code.
Step 3, use the "sql_db_query" tool to execute the sql query obtained in first step. If you have errors, use the "sql_query_fixer" tool to fix the problem.
Step 4, give the final answer from database to the original input question.
"""
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
