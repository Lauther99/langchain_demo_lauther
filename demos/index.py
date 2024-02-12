import sys
sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")
from demos.tools.sql_translator.tool import sql_translator, sql_filter_tool, sql_empty_db_response
from demos.tools.sql_result.tool import sql_db_query
from demos.config.env_config import OPENAI_API_KEY, OPENAI_AGENT_MODEL
from demos.agents.agent import create_agent
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback

# search_tables = [
#     "fcs_computadores",
#     "fcs_computador_medidor",
#     "med_sistema_medicion",
#     "var_tipo_variable",
#     "var_variable_datos",
# ]

# Model
llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model_name=OPENAI_AGENT_MODEL)

# Tools
tools = [
    sql_filter_tool,
    sql_translator,
    sql_db_query,
    sql_empty_db_response
]

# Agent
agent = create_agent(llm=llm, verbose=True, tools=tools, max_iterations=10)

# Preguntas
q1 = "average of 'Pressão Estática (kPa)' values registered between october 17th in 2022 and october 31th in 2022 for the measurement system with tag EMED-3138.09-005"
q1 = "average of 'static pressure' values registered between october 17th in 2022 and october 31th in 2022 for the measurement system with tag EMED-3138.09-005"
q2 = "how many computers are?"
q5 = "List the names of the measurement system of the meters that the computer has with tag FQI-3161.01-017?"
# q8 = "'static pressure' values for all measurements systems for the computer with tag FQI-EMED_05-08-10"
# q13 = "promedio de los valores para 'temperatura' registrados en Agosto del 2023 del sistema de medicion con id 70 en el computador con tag FQI-EMED_05-08-10"
# q13 = "¿Cuál es el promedio de los valores de 'temperatura' registrados en agosto de 2023 para cada uno de los sistemas de medición con ID 70 y 71 en el computador con la etiqueta FQI-EMED_05-08-10?"
# q13 = "¿Cuál es el promedio de los valores de 'temperatura' registrados en agosto de 2023 para el sistema de medicion con id 70 y para el sistema de medicion con id 71 que estan en el computador con la etiqueta FQI-EMED_05-08-10?"
# q13 = "Cuáles son los promedios de los valores de 'temperatura' registrados en agosto de 2023 para el sistema de medicion con id 70 y para el sistema de medicion con id 71 que estan en el computador con la etiqueta FQI-EMED_05-08-10, da los valores de forma independiente"
q9 = "average value of 'temperature' registered in August 2023 for all measurements systems for the computer with tag FQI-EMED_05-08-10"
q11 = "average value of 'static pressure' for measurement system with id 70 in the computer with tag FQI-EMED_05-08-10"
q12 = "average value for 'temperature' from measurement system in the computer with tag FQI-EMED_05-08-1044 registered in August 2023"
q13 = "what can you do?"
q13 = "do you know how many computers are?"
q13 = "hello"
q12 = "find average effective flow time recorded in August 2023 for each the measurement system from the computer with tag FQI-EMED_05-08-10"
q15 = "find the average value of each variable recorded in August 2023 for second meter in the computer with tag FQI-EMED_05-08-10"
q15 = "how much meters has the computer with tag FQI-EMED_05-08-10"
q15 = "tell me the meters in the computer with tag FQI-EMED_05-08-10"
q15 = "could you tell me the measurement systems that are in the computer with tag FQI-EMED_05-08-10"
q16 = 'find the average value of each variable recorded in August 2023 for each meter that reads natural gas in the computer with tag FQI-EMED_05-08-10'

def start(query: str):
    with get_openai_callback() as cb:
        agent.invoke({"input": query})
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")

start(q13)
