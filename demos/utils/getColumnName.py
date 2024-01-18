import sys
sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")
from demos.config.database_connection import conn


cursor = conn.cursor()
table_name = 'fcs_computador_medidor'
query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"


cursor.execute(query)
column_names = [row.COLUMN_NAME for row in cursor.fetchall()]
print(f"Columnas de la tabla '{table_name}': {column_names}")

