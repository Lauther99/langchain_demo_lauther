import environ

env = environ.Env()
environ.Env.read_env()

OPENAI_API_KEY = env("OPENAI_API_KEY")
MONGODB_URL = env("MONGODB_URL")
MONGODB_DATABASE_NAME = env("MONGODB_DATABASE_NAME")

USER = env("USER")
PWD = env("PWD")
HOST = env("HOST")
DBNAME = env("DBNAME")
ODBCDRIVER = env("ODBCDRIVER")
