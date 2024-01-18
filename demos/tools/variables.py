import sys

sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain.chains import RetrievalQA
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores.faiss import FAISS
import os
from langchain.prompts import PromptTemplate
from demos.config.env_config import OPENAI_API_KEY
from langchain_openai import OpenAIEmbeddings
from langchain.tools import BaseTool
import re


def get_variable_name_v1(initial_input: str):
    """Use this tool to get the correct variable name"""
    # Obteniendo la data de variables
    root_path = os.path.abspath("../open_ai_assistant/demos/data")
    dictionary_path = root_path + "\\data_variables.csv"
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

    prompt_template = """
        You are a expert petroleum engineer
        You will be asked for this variable: {question}. 
        The following context have two columns, one for 'Input' and one 'Name'. 
        Use your knowledge and the context to find the most accurate name in the context:
        {context}
        Once you find the name, just answer with the the first 'Name' finded, do not try to do more explanation or a list.
        Answer:"""

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(
        llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": prompt},
    )
    
    # Formateando el inital input
    pattern = r"'(.*?)'"
    
    def format_function(match):
        result = chain.invoke(str(match))
        final_res = result["result"]
        return final_res
    
    nueva_oracion = re.sub(pattern, format_function, initial_input) 
        
    return nueva_oracion

def get_variable_name_v2(initial_input: str):
    """Use this tool to get the correct variable name from the database"""
    root_path = os.path.abspath("../open_ai_assistant/demos/data")

    dictionary_path = root_path + "\\data_variables.csv"

    loader = CSVLoader(
        file_path=dictionary_path, encoding="utf-8", csv_args={"delimiter": ";"}
    )
    data = loader.load()
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents=data, embedding=embeddings)
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY, temperature=0, model_name="gpt-3.5-turbo"
    )

    prompt_template = """
    You are an expert petroleum engineer, you have to correct the following question input:
    Question input: {question}
    To correct, follow this steps:
    First, use your knowledge to find the actual variable name in the question, it could be like: "...static pressure..", "...average flow..", "...bsw..", "...differential pressure..", etc. Once you find the actual variable name reserve it.
    Second, the following context have two columns: 'Input' and 'CorrectName'. 
    Use your knowledge and the context to find the most accurate variable name in the context to the actual variable name. This new correct name ALWAYS MUST BE FROM THE 'CorrectName' column from the CONTEXT.
    Context:
    {context} \n
    Third, Once you find the CorrectName, you have to replace it into the question.
    
    Here is an example of what you have to do:
    Question input: "Static pressure average registered between october 17th in 2022 and october 31th in 2022 for the measurement system with tag EMED-3138.09-005".
    Actual variable: Static pressure, this is founded in the question input.
    New variable: Pressão Estática (kPa), this is founded after you check in the context.
    Final result: Pressão Estática (kPa) average registered between october 17th in 2022 and october 31th in 2022 for the measurement system with tag EMED-3138.09-005.
    """

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(
        llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": prompt},
    )
    
    result = chain.invoke(initial_input)
    final_res = result["result"]
    return final_res

class VariablesTool(BaseTool):
    name = "Variables_name_tool"
    description = "Useful when you have to find the correct variable name in a question, input to this tool is the complete user question and the output is the corrected formatted question"

    def _run(self, initial_input: str):
        return get_variable_name_v1(initial_input)

    def _arun(self, initial_input: str):
        raise get_variable_name_v1(initial_input)

# Test

# newname = get_variable_name_v1("'Average flow' registered between october 17th in 2022 and october 31th in 2022 for the computer with tag FQI-EMED_05-08-10 and meter code 1")
# print(newname)

# newname = get_variable_name_v2(
#     "previous density registered between october 17th in 2022 and october 31th in 2022 for the computer with tag FQI-EMED_05-08-10 and meter code 1"
# )
# print(newname)