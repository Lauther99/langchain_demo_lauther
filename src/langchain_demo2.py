import environ
from langchain import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import pyodbc
from sqlalchemy.engine import URL

env = environ.Env()
environ.Env.read_env()
API_KEY = env('OPENAI_API_KEY')
USER = env('USER')
PWD = env('PWD')
HOST = env('HOST')
DBNAME = env('DBNAME')
ODBCDRIVER = env('ODBCDRIVER')

""" Simple LLM call Using LangChain
llm = OpenAI(model_name="text-davinci-003", openai_api_key=API_KEY)
question = "Which language is used to create chatgpt ?"
print(question, llm(question))
"""
""" Creating a prompt template and running the LLM chain
llm = OpenAI(model_name="text-davinci-003", openai_api_key=API_KEY)
template = "What are the top {n} resources to learn {language} programming?"
prompt = PromptTemplate(template=template,input_variables=['n','language'])
chain = LLMChain(llm=llm,prompt=prompt)
input = {'n':3,'language':'Python'}
print(chain.run(input))
""" 

# Setea la DB
connection_uri = URL.create(
    "mssql+pyodbc",
    username=USER,
    password=PWD,
    host=HOST,
    database=DBNAME,
    query={"driver": ODBCDRIVER},
)
db = SQLDatabase.from_uri(connection_uri)

# Setea el modelo
llm = OpenAI(temperature=0, openai_api_key=API_KEY)

# Crea la query
QUERY = """
Given an input question, first create a syntactically correct sql server query to run, then look at the results of the query and return the answer.
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here
{question}
"""

# Setea la conexion de la db con el modelo
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
def run():
    print("Type 'exit' to quit")
    while True:
        prompt = input("Enter a prompt: ")

        if prompt.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                question = QUERY.format(question=prompt)
                print(db_chain.run(prompt))
            except Exception as e:
                print(e)

run()
