import sys

sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")
from demos.tools.sql_translator.tool import SQLTranslatorTool, SQLQueryFixer
from demos.tools.sql_result.tool import SQLQueryTool
from demos.tools.question_formater.tool import InputFormatterTool
from demos.config.env_config import OPENAI_API_KEY
from demos.agents.agent import create_agent
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback

search_tables = [
    "fcs_computadores",
    "fcs_computador_medidor",
    "med_sistema_medicion",
    "var_tipo_variable",
    "var_variable_datos",
]

# Model
llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model_name="gpt-3.5-turbo")

# Tools
tools = [
    InputFormatterTool(),
    SQLTranslatorTool(search_tables=search_tables, db_schema="dbo_v2"),
    SQLQueryTool(),
    SQLQueryFixer(),
]

# Agent
agent = create_agent(llm=llm, verbose=True, tools=tools, max_iterations=10)

# Testing
q1 = "average of 'Pressão Estática (kPa)' values registered between october 17th in 2022 and october 31th in 2022 for the measurement system with tag EMED-3138.09-005"
q1 = "average of 'static pressure' values registered between october 17th in 2022 and october 31th in 2022 for the measurement system with tag EMED-3138.09-005"
# q1 = "'Pressão Estática (kPa)' values registered between october 17th in 2022 and october 31th in 2022 for the computer with tag FQI-EMED_05-08-10 and meter code 1"
# q2 = "Meters of each computer"
q3 = "how many computers are?"
q4 = "quantity of meters that the computer with IP equal to 10.233.117.63 has"
q5 = "List the names of the measurement system of the meters that the computer has with tag FQI-3161.01-017?"
# q6 = "List the names of the measurement system of the meters that the computer has with IP equal to 10.233.81.59?"
q7 = "quantity of computers that are in port 4000"
# q8 = "'static pressure' values for all measurements systems for the computer with tag FQI-EMED_05-08-10"
q9 = "'average flow' registered in August 2023 for all measurements systems for the computer with tag FQI-EMED_05-08-10"
q10 = "average 'temperature' value for all measurements systems for the computer with tag FQI-EMED_05-08-10"
q11 = "average 'static pressure' value for measurement system with id 70 in the computer with tag FQI-EMED_05-08-10"


def start(query: str):
    with get_openai_callback() as cb:
        agent.invoke({"input": query})
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")


start(q11)
