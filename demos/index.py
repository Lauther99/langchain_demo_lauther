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
language = "es"
tools = [
    InputFormatterTool(lan=language),
    SQLTranslatorTool(search_tables=search_tables, db_schema="dbo_v2", lan=language),
    SQLQueryTool(lan=language),
    SQLQueryFixer(db_schema="dbo_v2", lan=language),
]

# Agent
agent = create_agent(llm=llm, verbose=True, tools=tools, max_iterations=10, lan=language)

# Testing
q1 = "average of 'Pressão Estática (kPa)' values registered between october 17th in 2022 and october 31th in 2022 for the measurement system with tag EMED-3138.09-005"
q1 = "average of 'static pressure' values registered between october 17th in 2022 and october 31th in 2022 for the measurement system with tag EMED-3138.09-005"
# q2 = "how many computers are?"
q5 = "List the names of the measurement system of the meters that the computer has with tag FQI-3161.01-017?"
# q8 = "'static pressure' values for all measurements systems for the computer with tag FQI-EMED_05-08-10"
q9 = "value of 'average flow' registered in August 2023 for all measurements systems for the computer with tag FQI-EMED_05-08-10"
q10 = "average value of 'temperature' for all measurements systems for the computer with tag FQI-EMED_05-08-10"
q11 = "average value of 'static pressure' for measurement system with id 70 in the computer with tag FQI-EMED_05-08-10"
q12 = "average value for 'temperature' from measurement system with id 70 in the computer with tag FQI-EMED_05-08-10 registered in August 2023"
q13 = "promedio de los valores para 'temperatura' registrados en Agosto del 2023 del sistema de medicion con id 70 en el computador con tag FQI-EMED_05-08-10"


def start(query: str):
    with get_openai_callback() as cb:
        agent.invoke({"input": query})
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")


start(q13)
