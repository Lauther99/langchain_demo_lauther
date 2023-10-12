"""Toolkit for interacting with an SQL database."""
from typing import List

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.pydantic_v1 import Field
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools import BaseTool
from langchain.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain.utilities.sql_database import SQLDatabase

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from typing import (List)
from pandas import DataFrame
import pandas as pd

import spacy
import faiss
import numpy as np
from fuzzywuzzy import fuzz


class CustomSQLToolkit(BaseToolkit):
    """Toolkit for interacting with SQL databases."""

    db: SQLDatabase = Field(exclude=True)
    llm: BaseLanguageModel = Field(exclude=True)

    @property
    def dialect(self) -> str:
        """Return string representation of SQL dialect to use."""
        return self.db.dialect

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        list_sql_database_tool = ListSQLDatabaseTool(db=self.db)
        info_sql_database_tool_description = (
            "Input to this tool is a comma-separated list of tables, output is the "
            "schema and sample rows for those tables. "
            "Be sure that the tables actually exist by calling "
            f"{list_sql_database_tool.name} first! "
            "Example Input: 'table1, table2, table3'"
        )
        info_sql_database_tool = InfoSQLDatabaseTool(
            db=self.db, description=info_sql_database_tool_description
        )
        # query_sql_database_tool_description = (
        #     "Input to this tool is a detailed and correct SQL query, output is a "
        #     "result from the database. If the query is not correct, an error message "
        #     "will be returned. If an error is returned, rewrite the query, check the "
        #     "query, and try again. If you encounter an issue with Unknown column "
        #     f"'xxxx' in 'field list', using {info_sql_database_tool.name} "
        #     "to query the correct table fields."
        # )
        improved_query_sql_database_tool_description = (
            "Input to this tool is a detailed and correct SQL query, output is a "
            "result from the database. If the query contanis statements like INSERT, UPDATE, DELETE, DROP "
            "you have to return you don't have the permission to do this action."
            "Never make a 'SELECT * FROM ...' from a table, only ask for the relevant columns given the question."
            "If the query is not correct, an error message will be returned. If an error is returned, "
            "rewrite the query, check the query, and try again."
            "If have troubles with table name, use this tool or you encounter an issue with Unknown column 'xxxx' in 'field list', "
            f"use this tool {info_sql_database_tool.name} to query the correct table fields and then compare to the columns or table names that "
            " you have in the query and try to replace with the correct columns or table names."
        )
        
        query_sql_database_tool = QuerySQLDataBaseTool(
            db=self.db, description=improved_query_sql_database_tool_description
        )
        query_sql_checker_tool_description = (
            "Use this tool to double check if your query is correct before executing "
            "it. Always use this tool before executing a query with "
            f"{query_sql_database_tool.name}!"
        )
        query_sql_checker_tool = QuerySQLCheckerTool(
            db=self.db, llm=self.llm, description=query_sql_checker_tool_description
        )
        
        return [
            query_sql_database_tool,
            info_sql_database_tool,
            list_sql_database_tool,
            query_sql_checker_tool,
        ]

class SQLDatabaseExamples: #Todo: Comparar con los resultados de 'Vectara, Pinecone, Chroma' para ver cual es más conveniente
    def __init__(self, hf_model_name: str, splitted_documents: List[Document]):
        self.document_list = splitted_documents
        self.hf_model_name = hf_model_name
        self.hf_model = HuggingFaceEmbeddings(model_name=self.hf_model_name)
        self.db = FAISS.from_documents(self.document_list, self.hf_model)

    def get_similar_sql_examples(self, query: str):
        '''Use this tool to get similar SQL queries from a database'''
        embedding_vector = self.hf_model.embed_query(query)
        similar_results = self.db.similarity_search_with_score_by_vector(embedding_vector, k=1, score_threshold=0.25)
        #return similar_results # To see the score and results
        page_content = similar_results[0][0].page_content if similar_results else ""
        lineas = page_content.split('\n')
        for linea in lineas:
            if linea.startswith('Query:'):
                query = linea[len('Query:'):].strip()
                return query
        else:
            return ""
        
    def get_similar_sql_examples_with_score(self, query: str):
        '''Use this tool to get similar SQL queries from a database'''
        embedding_vector = self.hf_model.embed_query(query)
        similar_results = self.db.similarity_search_with_score_by_vector(embedding_vector, k=1, score_threshold=0.25)
        return similar_results # To see the score and results

class SQLDatabaseInfo():
    def __init__(self, ruta_completa: str, table_names: List[str], ):
        self.table_names = table_names
        self.descriptions_root_path = ruta_completa

    def get_tables_descriptions(self, table_name: str):
        '''Use this tool to get descriptions of tables from database'''
        table_name = ""
        path = self.descriptions_root_path + '\data_descriptions.csv'
        data = pd.read_csv(path, delimiter=';')

        datos = [(table, des) for table, des in zip(data['Table'], data['Description'])]
        
        # Cargar el modelo de lenguaje de spaCy
        nlp = spacy.load('es_core_news_md')

        # Obtener los vectores de palabras para cada descripción
        descripciones = [nlp(descripcion).vector for _, descripcion in datos]

        # Configurar el índice
        index = faiss.IndexFlatL2(len(descripciones[0]))
        descripciones = np.array(descripciones).astype('float32')
        res = []
        for name in self.table_names:
            table_query = [des for table, des in datos if table == name][0]
            vector_query = nlp(table_query).vector
            D, I = index.search(np.array([vector_query]).astype('float32'), k=1)
            indice_resultado = I[0][0]
            descripcion_resultado = datos[indice_resultado][1]
            
            descripcion = f"The table {name} is a {descripcion_resultado}"
            res.append(descripcion)
        
        return '. \n '.join(res)
    
    def get_tables_descriptions_fuzzywuzzy(self):
        path = self.descriptions_root_path + '\data_descriptions.csv'
        data = pd.read_csv(path, delimiter=';')
        datos = [(table, des) for table, des in zip(data['Table'], data['Description'])]
        
        # Cargar el modelo de lenguaje de spaCy
        nlp = spacy.load('es_core_news_md')

        # Obtener los vectores de palabras para cada descripción
        descripciones = [nlp(descripcion).vector for _, descripcion in datos]

        descripciones = np.array(descripciones).astype('float32')
        res = []
        for name in self.table_names:
            best_match = max(datos, key=lambda x: fuzz.ratio(name, x[0]))
            table_name = best_match[0]
            table_des = best_match[1]

            descripcion = f"The table {table_name} is a {table_des}"
            res.append(descripcion)

        return '. \n '.join(res)
    
    def get_variable_names(self, variable_list_strings : str):
        '''Use this tool to get the real names of the variables in the table'''
        path = self.descriptions_root_path + '\data_variables.csv'
        data = pd.read_csv(path, delimiter=';', encoding='utf-8')
        datos = [(input, name) for input, name in zip(data['Input'], data['Name'])]
        variables_array = variable_list_strings.split(",")
        # Cargar el modelo de lenguaje de spaCy
        nlp = spacy.load('es_core_news_md')

        # Obtener los vectores de palabras para cada descripción
        descripciones = [nlp(descripcion).vector for _, descripcion in datos]

        descripciones = np.array(descripciones).astype('float32')
        res = []
        for name in variables_array:
            best_match = max(datos, key=lambda x: fuzz.ratio(name, x[0]))
            bm = best_match[1]
            res.append(bm)

        return ','.join(res)
    
    def get_variable_names_v2(self, variable_string : str):
        '''Use this tool to get the real names of the variables in the table'''
        path = self.descriptions_root_path + '\data_variables.csv'
        data = pd.read_csv(path, delimiter=';', encoding='utf-8')
        datos = [(input, name) for input, name in zip(data['Input'], data['Name'])]
        # Cargar el modelo de lenguaje de spaCy
        nlp = spacy.load('es_core_news_md')

        # Obtener los vectores de palabras para cada descripción
        descripciones = [nlp(descripcion).vector for _, descripcion in datos]

        descripciones = np.array(descripciones).astype('float32')
        
        best_match = max(datos, key=lambda x: fuzz.ratio(variable_string, x[0]))
        bm = best_match[1]
        return bm
            





