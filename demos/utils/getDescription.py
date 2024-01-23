import sys
sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")
from demos.data.data_info import tables

def get_description(schema, search_tables, lan = "en"):
    description = ""
    for name in search_tables:
        for table in tables:
            if lan == "en":
                if table["schema"] == schema and table["table_name"] == name:
                    table_columns = ", ".join([f"'{column}'" for column in table["columns"]])
                    result = f'- {table["description"][lan]} and has columns {table_columns}.\n'
                    description += result
            elif lan == "es":
                if table["schema"] == schema and table["table_name"] == name:
                    table_columns = ", ".join([f"'{column}'" for column in table["columns"]])
                    result = f'- {table["description"][lan]}, tiene columnas como: {table_columns}.\n'
                    description += result
            
            
    
    return description

# search_tables = [
#     "fcs_computadores",
#     "fcs_computador_medidor",
#     "med_sistema_medicion",
#     "var_tipo_variable",
#     "var_variable_datos",
# ]
# print(get_description("dbo_v2", search_tables, "es"))