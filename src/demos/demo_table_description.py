import sys
sys.path.append('C:\\Users\\lauth\\OneDrive\\Desktop\\py_projects\\langchain_demo_lauther')
import os
import environ
from langchain.tools import Tool
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from src.sql_toolkit.sql_toolkit import CustomSQLToolkit, SQLDatabaseExamples, SQLDatabaseInfo
from src.agents.sqlagent import create_sql_agent_plus_extra_tools
from src.chain_tools_demos.variable_chain import VariablesInfo
from src.prompts.prompt import CUSTOM_PREFIX_DESC, CUSTOM_FORMAT_INSTRUCTIONS_DESC, CUSTOM_SUFFIX_DESC


from langchain.chat_models import ChatOpenAI
from sqlalchemy.engine import URL
from langchain.utilities import SQLDatabase
from langchain.agents.mrkl.base import ZeroShotAgent



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

# Setting database object
search_tables = ["fcs_computadores", "fcs_computador_medidor", "med_sistema_medicion","var_tipo_variable","var_variable_datos"]
sql_database = SQLDatabase.from_uri(connection_uri, schema='dbo_v2', include_tables=search_tables, sample_rows_in_table_info = 2)

# Setting the agent model
agent_model = ChatOpenAI(temperature=0, openai_api_key=API_KEY, model="gpt-3.5-turbo")

# Getting get_tables_descriptions function
dictionary_path = os.path.abspath('../langchain_demo_lauther/src/dictionary/')
sql_info_instance = SQLDatabaseInfo(dictionary_path, search_tables)
db_variable_info = VariablesInfo(API_KEY, dictionary_path)

database_summary = sql_info_instance.get_tables_descriptions_fuzzywuzzy()

# Getting SQL tools
toolkit = CustomSQLToolkit(db=sql_database, llm=agent_model)

# Creating tools
tools = [
    Tool(
        name="find_correct_variable_name",
        func=db_variable_info.get_variable_name,
        description="Useful to find the correct variable name in the table dbo_v2.var_tipo_variable to construct the SQL QUERY, input for this tool is the variable name you find in the question, output a string you have to use in SQL QUERY for filtering",
    )
]

# Setting the agent_executor
agent_executor = create_sql_agent_plus_extra_tools(
    llm=agent_model,
    toolkit=toolkit,
    verbose=True,
    custom_tools= toolkit.get_tools() + tools,
    top_k=10,
    prefix=CUSTOM_PREFIX_DESC,
    suffix=CUSTOM_SUFFIX_DESC,
    format_instructions=CUSTOM_FORMAT_INSTRUCTIONS_DESC,
    summary=database_summary
)

query_str = "Meters of each computer"
query_str = "how many computers are?"
query_str_v2 = "quantity of meters that the computer with IP equal to 10.233.117.63 has"
query_str_v3 = "List the names of the measurement system of the meters that the computer has with tag FQI-3161.01-017?"
query_str_v4 = "List the names of the measurement system of the meters that the computer has with IP equal to 10.233.81.59?"
query_str_v5 = "the computers that are in port 4000"
query_str_v6 = "Values of the static pressure for all measurements systems for the computer with tag FQI-EMED_05-08-10"
query_str_v6 = "values of the 'average flow' registered in August 2023 of all measurements systems for the computer with tag FQI-EMED_05-08-10"
query_str_v6 = "average of values of the 'static pressure' of all measurements systems for the computer with tag FQI-EMED_05-08-10"
from langchain.callbacks import get_openai_callback
with get_openai_callback() as cb:
    agent_executor.run(query_str_v6)
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")

