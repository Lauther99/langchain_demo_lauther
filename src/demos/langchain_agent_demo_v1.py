from langchain import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.utilities import SQLDatabase
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.engine import URL
import environ
import pyodbc
from langchain.callbacks import get_openai_callback
from langchain.agents import load_tools, initialize_agent, AgentType, create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI


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

toolkit = SQLDatabaseToolkit(db=sql_database, llm=model)

agent_executor = create_sql_agent(
    llm=model,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

query_str = "how many computers are in the table?"
query_str_v2 = "how many meters does the computer with IP equal to 1.1.1.1 has??"
query_str_v3 = "List the names of the measurement system of the meters that the computer has with tag FQI-3161.01-017?"
query_str_v4 = "List the names of the measurement system of the meters that the computer has with IP equal to 10.233.81.59?"
# response = db_chain.run(query_str_v3)

with get_openai_callback() as cb:
    agent_executor.run(query_str_v3)
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")