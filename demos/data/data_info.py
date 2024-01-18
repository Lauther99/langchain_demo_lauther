
tables =  [
        {
            "schema": "dbo_v2",
            "table_name": "fcs_computadores",
            "columns": ["Id", "IP", "Puerto", "Puerto_Secundario", "Id_Modbus", "Id_Modbus_Secundario", "Tag", "Compatibilidad_Modicon", "Id_Computador_Redundante", "Estado", "Master", "Usuario", "Contraseña", "Leer_Tiempo_Real", "Leer_Configuracion", "Leer_Alarmas", "Leer_Eventos", "Leer_Historicos", "Grupo_Destino", "Unidad_Destino", "Grupo_Fuente", "Unidad_Fuente", "Orden_Archivos", "Numero_Maximo_Horarios", "Numero_Maximo_Diarios", "Numero_Maximo_Proves", "Numero_Maximo_Batch", "Tipo_Protocolo", "Tiempo_Proceso_Historico", "Tiempo_Proceso_TiempoReal", "IdFirmware_fk", "IdEquipo_fk", "Servidor_OPC"],
            "description": "The fcs_computadores table has information about computers"
        },
        {
            "schema": "dbo_v2",
            "table_name": "med_sistema_medicion",
            "columns": ["Id", "IdPlataforma_fk", "Nombre", "Tag", "Estado", "FechaInicialMuestreo", "IdCliente", "IdTipoFluido_fk", "SubTipoFluido", "IdAplicabilidad_fk", "VarCromatografia", "Prover", "IsDisponible", "IdMeteringStation_fk", "IdClase_fk", "SamplingPointTag", "LimiteEstadisticoInicial", "PROFACCODE", "SOURCE", "RefPid", "NumeroLineaProceso", "Localizacion", "NominalLineSize", "IdSchedule_fk", "IdRating_fk", "ClasificacionArea", "Servicio", "LimiteEstadistico_Default", "LimiteEstadistico_Manual", "IdSamplingPoint_fk", "IsVisible", "Uso", "IdArea_fk","IdDeBaseOperacional_fk", "EsProvador", "Tramo", "IdDelSistemaAsociado_fk"],
            "description": "The med_sistema_medicion table has information about measurement systems"
        },
        {
            "schema": "dbo_v2",
            "table_name": "var_tipo_variable",
            "columns": ["Id", "Nombre", "Reporte_Manual", "IdRepManual", "Id_Field", "Cromatografia", "Estado"],
            "description": "The var_tipo_variable table has information about the name of medition variables for example: pressure, temperature, density, volume, average flow, etc, and their respective ids"
        },
        {
            "schema": "dbo_v2",
            "table_name": "var_variable_datos",
            "columns": ["Fecha", "idVariable_fk", "idSistemaMedicion_fk", "Valor", "Valor_String"],
            "description": "The var_variable_datos table has information about the values of the variables in var_variable_datos table. The idVariable_fk is a foreign key referencing the Id column in the var_tipo_variable table and the idSistemaMedicion_fk is a foreign key referencing the Id column in the med_sistema_medicion table"
            # "description": "The var_variable_datos table is a connector between variables in var_tipo_variable table and measurement systems in med_sistema_medicion table. Has information about the values of the variables in var_variable_datos table."
        },
        {
            "schema": "dbo_v2",
            "table_name": "fcs_computador_medidor",
            "columns": ["Id", "Codigo_Medidor", "Estado", "Id_Sisema_Medicion", "Id_Sistema_Medicion_Redundante", "IdComputador_fk"],
            "description": "The fcs_computador_medidor table connect fcs_computadores table and med_sistema_medicion with IdComputador_fk that is a foreign key referencing the Id column in the fcs_computadores table and the Id_Sisema_Medicion is a foreign key referencing the Id column in the med_sistema_medicion table"
            # "description": "The fcs_computador_medidor table is a connector between fcs_computadores table and med_sistema_medicion table. Has information about meters in the computers like meter codes, status of the meter and the id of measurement system that the computer is connected"
        },
    ]