
tables =  [
        {
            "schema": "dbo_v2",
            "table_name": "fcs_computadores",
            "columns": ["Id", "IP", "Puerto", "Puerto_Secundario", "Id_Modbus", "Id_Modbus_Secundario", "Tag", "Compatibilidad_Modicon", "Id_Computador_Redundante", "Estado", "Master", "Usuario", "Contraseña", "Leer_Tiempo_Real", "Leer_Configuracion", "Leer_Alarmas", "Leer_Eventos", "Leer_Historicos", "Grupo_Destino", "Unidad_Destino", "Grupo_Fuente", "Unidad_Fuente", "Orden_Archivos", "Numero_Maximo_Horarios", "Numero_Maximo_Diarios", "Numero_Maximo_Proves", "Numero_Maximo_Batch", "Tipo_Protocolo", "Tiempo_Proceso_Historico", "Tiempo_Proceso_TiempoReal", "IdFirmware_fk", "IdEquipo_fk", "Servidor_OPC"],
            "description": {
                "en" : "The fcs_computadores table has information about computers",
                "es" : "La tabla fcs_computadores tiene informacion sobre los computadores"
            }
        },
        {
            "schema": "dbo_v2",
            "table_name": "med_sistema_medicion",
            "columns": ["Id", "IdPlataforma_fk", "Nombre", "Tag", "Estado", "FechaInicialMuestreo", "IdCliente", "IdTipoFluido_fk", "SubTipoFluido", "IdAplicabilidad_fk", "VarCromatografia", "Prover", "IsDisponible", "IdMeteringStation_fk", "IdClase_fk", "SamplingPointTag", "LimiteEstadisticoInicial", "PROFACCODE", "SOURCE", "RefPid", "NumeroLineaProceso", "Localizacion", "NominalLineSize", "IdSchedule_fk", "IdRating_fk", "ClasificacionArea", "Servicio", "LimiteEstadistico_Default", "LimiteEstadistico_Manual", "IdSamplingPoint_fk", "IsVisible", "Uso", "IdArea_fk","IdDeBaseOperacional_fk", "EsProvador", "Tramo", "IdDelSistemaAsociado_fk"],
            "description": {
                "en" : "The med_sistema_medicion table has information about measurement systems",
                "es" : "La tabla med_sistema_medicion tiene información sobre sistemas de medición asociados a los computadores"
            }
        },
        {
            "schema": "dbo_v2",
            "table_name": "var_tipo_variable",
            "columns": ["Id", "Nombre", "Reporte_Manual", "IdRepManual", "Id_Field", "Cromatografia", "Estado"],
            "description": {
                "en" : "The var_tipo_variable table has information about the name of medition variables for example: pressure, temperature, density, volume, average flow, etc, and their respective ids",
                "es" : "La tabla var_tipo_variable tiene información sobre los nombres de las variables de medición como por ejemplo: presión, temperatura, densidad, volumen, flujo, etc y sus respectivos ids"
            }
        },
        {
            "schema": "dbo_v2",
            "table_name": "var_variable_datos",
            "columns": ["Fecha", "idVariable_fk", "idSistemaMedicion_fk", "Valor", "Valor_String"],
            "description": {
                "en" : "The var_variable_datos table has information about the values of the variables in var_tipo_variable table. The idVariable_fk is a foreign key referencing the Id column in the var_tipo_variable table and the idSistemaMedicion_fk is a foreign key referencing the Id column in the med_sistema_medicion table",
                "es" : "La tabla var_variable_datos tiene informacion sobre los valores que tienen las variables en var_tipo_variable. La idVariable_fk es la llave foránea que referencia a la columna Id en la tabla var_tipo_variable y idSistemaMedicion_fk es otra llave foránea que referencia a la columna Id en la tabla med_sistema_medicion"
            }
        },
        {
            "schema": "dbo_v2",
            "table_name": "fcs_computador_medidor",
            "columns": ["Id", "Codigo_Medidor", "Estado", "Id_Sisema_Medicion", "Id_Sistema_Medicion_Redundante", "IdComputador_fk"],
            "description": {
                "en" : "The fcs_computador_medidor table connect fcs_computadores table and med_sistema_medicion with IdComputador_fk that is a foreign key referencing the Id column in the fcs_computadores table and the Id_Sisema_Medicion is a foreign key referencing the Id column in the med_sistema_medicion table",
                "es" : "La tabla fcs_computador_medidor conecta a las tablas fcs_computadores y med_sistema_medicion mediante IdComputador_fk que es la llave foránea que referencia a la columna Id en la tabla fcs_computadores además existe Id_Sisema_Medicion que es la llave foránea que referencia a la columna Id en la tabla med_sistema_medicion"
            }
        },
    ]