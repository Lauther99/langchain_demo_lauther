from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI 
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain, RetrievalQA, LLMChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
import tempfile
import os
import environ
from langchain.prompts import PromptTemplate


# env = environ.Env()
# environ.Env.read_env()
# API_KEY = env('OPENAI_API_KEY')


class VariablesInfo():
    def __init__(self, api_key, root_path : str):
        self.api_key = api_key
        self.root_path = root_path

    def get_variable_name(self, fake_name : str):
        '''Use this tool to get the correct variable name from the database'''

        dictionary_path = self.root_path + '\data_variables.csv'
        loader = CSVLoader(file_path=dictionary_path, encoding="utf-8", csv_args={'delimiter': ';'})
        data = loader.load()

        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(data, embeddings)
        llm = OpenAI(temperature=0, model="text-davinci-003", openai_api_key=self.api_key)

        prompt_template = """
        You are a expert petroleum engineer
        You will be asked for this variable: {question}. 
        The following context have two columns, one for 'Input' and one 'Name'. 
        Use your knowledge and the context to find the most accurate name in the context:
        {context}
        Once you find the name, just answer with the the first 'Name' finded, do not try to do more explanation or a list.
        Answer:"""
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        custom_prompt = {"prompt": PROMPT}
        chain = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=vectorstore.as_retriever(), chain_type_kwargs=custom_prompt)
        
        result = chain.run(fake_name)
        final_res = result.strip()

        return final_res
    