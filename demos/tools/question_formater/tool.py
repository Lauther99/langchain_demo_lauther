import sys

sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")

from demos.config.env_config import OPENAI_API_KEY
from demos.tools.question_formater.variables import VariablesTool
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain, LLMChain
from langchain.llms.openai import OpenAI

from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from demos.agents.agent import create_agent
from demos.tools.question_formater.instructions import (
    PREFIX,
    INPUT_FORMATER_TOOL_DESCRIPTION,
    GET_VARIABLE_NAME_FUNCTION,
    VARIABLES_FILE_PATH
)
from langchain.document_loaders.csv_loader import CSVLoader
import os
from langchain.vectorstores.faiss import FAISS
import re
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA


def get_formatted_question(query_input) -> str:
    # Model
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model_name="gpt-3.5-turbo")

    # Tools
    tools = [
        VariablesTool(),
    ]

    # Agent
    agent = create_agent(
        llm=llm, verbose=True, tools=tools, max_iterations=10, prefix=PREFIX
    )

    # query = "Format this question: {query_input}"
    response = ""
    with get_openai_callback() as cb:
        response = agent.invoke({"input": query_input})
        print(f"Total Tokens: {cb.total_tokens}")

    return response.get("output", query_input)


def get_variable_name(initial_input: str, lan: str = "en"):
    """Use this tool to get the correct variable name"""
    # Obteniendo la data de variables
    root_path = os.path.abspath("../open_ai_assistant/demos/data")
    dictionary_path = os.path.join(root_path, VARIABLES_FILE_PATH[lan])
    loader = CSVLoader(
        file_path=dictionary_path, encoding="utf-8", csv_args={"delimiter": ";"}
    )
    data = loader.load()
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents=data, embedding=embeddings)

    # Modelo LLM
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY, temperature=0, model_name="gpt-3.5-turbo"
    )

    prompt = PromptTemplate(
        template=GET_VARIABLE_NAME_FUNCTION[lan],
        input_variables=["context", "question"],
    )

    chain = RetrievalQA.from_chain_type(
        llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": prompt},
    )

    # Formateando el inital input
    pattern = r"'(.*?)'"

    def procesar(match):
        result = chain.invoke(str(match))
        final_res = result["result"]
        return f"'{final_res}'"

    res = re.sub(pattern, procesar, initial_input)

    return res


class InputFormatterTool(BaseTool):
    name = "Input_formatter"
    lan = "en"
    description = INPUT_FORMATER_TOOL_DESCRIPTION[lan]

    def __init__(self, lan="en"):
        super().__init__()
        self.lan = lan
        self.description = INPUT_FORMATER_TOOL_DESCRIPTION[lan]

    def _run(self, initial_input: str):
        return get_variable_name(initial_input=initial_input, lan=self.lan)

    def _arun(self, initial_input: str):
        return get_variable_name(initial_input=initial_input, lan=self.lan)


# # Test
# tool = InputFormatterTool(lan="es")
# response = tool._run(
#     "average of 'presión estatica' values registered between october 17th in 2022 and october 31th in 2022 for the measurement system with tag EMED-3138.09"
# )
# print(response)
