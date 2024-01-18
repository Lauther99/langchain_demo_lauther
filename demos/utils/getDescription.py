import sys
sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")
from demos.data.data_info import tables

def get_description(schema, search_tables):
    description = ""
    for name in search_tables:
        for table in tables:
            if table["schema"] == schema and table["table_name"] == name:
                table_columns = ", ".join([f"'{column}'" for column in table["columns"]])
                result = f'- {table["description"]} and has columns {table_columns}.\n'
                description += result
    
    return description