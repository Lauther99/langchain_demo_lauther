import sys

sys.path.append("C:\\Users\\lauth\\OneDrive\\Desktop\\open_ai_assistant")
import os
from demos.tools.question_formater.instructions import (
    VARIABLES_FILE_PATH
)
# import pandas as pd

# root_path = os.path.abspath("../open_ai_assistant/demos/data")
# dictionary_path = os.path.join(root_path, VARIABLES_FILE_PATH["en"])
# data = pd.read_csv(dictionary_path, sep=';')

# for indice, fila in data.iterrows():
#     # Acceder al dato de la primera columna
#     InputName = fila['InputName']
#     # Acceder al dato de la segunda columna
#     CorrectName = fila['CorrectName']
    
#     # Imprimir los datos de las dos columnas
#     res = '''vn.train(documentation="Whe user asks about '{var_name}' use '{new_var_name}' in the WHERE statement instead")'''
#     print(res.format(var_name = InputName, new_var_name = CorrectName))
    

# fluids = ["Gás Natural", "Óleo Cru", "Água", "Condensado", "Vapour", "Água + MEG", "MEG"]
fluids = ["Gás Natural", "Óleo Cru", "Água", "Vapour"]
fluids2 = ["natural gas", "Crude Oil", "water", "Vapour"]

i = 0
for fluid in fluids:
    InputName = fluids2[i]
    CorrectName = fluid
    
    # Imprimir los datos de las dos columnas
    res = '''vn.train(documentation="Whe user asks about a fluid like '{var_name}' use '{new_var_name}' in the WHERE statement instead")'''
    print(res.format(var_name = InputName, new_var_name = CorrectName))
    i=i+1