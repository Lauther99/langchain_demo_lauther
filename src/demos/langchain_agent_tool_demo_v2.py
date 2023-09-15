from langchain.utilities import SQLDatabase
from sqlalchemy.engine import URL
import environ
from langchain.chat_models import ChatOpenAI
import json
import os
import environ
import pyodbc

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.agents.agent_toolkits import create_retriever_tool

from langchain.agents import create_sql_agent, AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.callbacks import get_openai_callback


env = environ.Env()
environ.Env.read_env()
API_KEY = env('OPENAI_API_KEY')
USER = env('USER')
PWD = env('PWD')
HOST = env('HOST')
DBNAME = env('DBNAME')
ODBCDRIVER = env('ODBCDRIVER')

connection_uri = URL.create(
    "mssql+pyodbc",
    username=USER,
    password=PWD,
    host=HOST,
    database=DBNAME,
    query={"driver": ODBCDRIVER},
)
search_tables = ["fcs_computadores", "fcs_computador_medidor", "med_sistema_medicion"]

sql_database = SQLDatabase.from_uri(connection_uri, schema='dbo_v2', include_tables=search_tables, sample_rows_in_table_info=2)
model = ChatOpenAI(temperature=0, openai_api_key=API_KEY, model="gpt-3.5-turbo")

ruta_completa = os.path.abspath('../dictionary/dictionary.json')
with open('C:/Users/lauth/OneDrive/Desktop/py_projects/langchain_demo_lauther/src/dictionary/dictionary.json', 'r') as file:
    few_shots = json.load(file)

embeddings = OpenAIEmbeddings()

few_shot_docs = [Document(page_content=question, metadata={'sql_query': few_shots[question]}) for question in few_shots.keys()]
vector_db = FAISS.from_documents(few_shot_docs, embeddings)
retriever = vector_db.as_retriever()

tool_description = """
This tool will help you understand similar examples to adapt them to the user question.
"""

retriever_tool = create_retriever_tool(
        retriever,
        name='similar_examples',
        description=tool_description
    )
custom_tool_list = [retriever_tool]

toolkit = SQLDatabaseToolkit(db=sql_database, llm=model)

custom_suffix = """
I should first get the similar examples that are in tools.
If the examples are enough to construct the query, I can build it.
Otherwise, I can then look at the tables in the database to see what I can query.
I should always use dbo_v2 schema for tables when querying.
"""

agent = create_sql_agent(llm=model,
                         toolkit=toolkit,
                         verbose=True,
                         agent_type=AgentType.OPENAI_FUNCTIONS,
                         extra_tools=custom_tool_list,
                         prefix=custom_suffix
                        )

query_str_v3 = "List the names of the measurement system of the meters that have a computer with Tag equal to EST-3138.05-QUEIMA?"

with get_openai_callback() as cb:
    agent.run(query_str_v3)
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")