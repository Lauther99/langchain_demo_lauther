import environ

env = environ.Env()
environ.Env.read_env()

USER = env("USER")
PWD = env("PWD")
HOST = env("HOST")
DBNAME = env("DBNAME")
ODBCDRIVER = env("ODBCDRIVER")
PINECONE_API_KEY = env("PINECONE_API_KEY")
PINECONE_ENV = env("PINECONE_ENV")
OPENAI_API_KEY = env("OPENAI_API_KEY")
