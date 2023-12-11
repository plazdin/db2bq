Este script Python automatiza el proceso de extraer datos de una base de datos SQL a BigQuery. Utiliza las bibliotecas pyodbc y pandas para realizar las tareas de:

    Conexión: Establecer una conexión segura con la base de datos SQL y BigQuery.
    Extracción: Ejecutar consultas SQL personalizadas para extraer los datos deseados.
    Transformación: Manipular y transformar los datos según sea necesario (cambio de tipo de datos, eliminación de duplicados, etc.).
    Carga: Subir los datos transformados a un dataset específico de BigQuery.

Beneficios:

    Automatización: Elimina la necesidad de realizar manualmente la extracción y carga de datos.
    Precisión: Reduce el riesgo de errores humanos en el manejo de datos.
    Eficiencia: Optimiza el tiempo y recursos dedicados a la migración de datos.
    Flexibilidad: Permite personalizar la extracción y transformación de datos a través de la configuración del script.

Prerrequisitos:

    Docker compose instalado.

Instalación:
    
    Agregar carpeta config con los datos necesarios, incluyendo datos de la base de datos y el json_setting que es requerido para el ingreso a bigquery.
    Una vez hecho esto, puede modificar el script app/backup.sh para agregar las tablas que crea conveniente en el horario más adecuado y hacer el cron correspondiente.
    
    Finalmente, cree el contenedor con docker compose up -d.

Uso:

    Modifique el archivo de configuración con los detalles de conexión a la base de datos SQL y BigQuery.
    Ejecute el script para iniciar el proceso de extracción y carga de datos.

Adaptaciones:

El script puede adaptarse a diferentes escenarios modificando:

    Consultas SQL: Extraer datos específicos de distintas tablas.
    Transformaciones: Limpiar, formatear y manipular los datos antes de la carga.
    Destino de BigQuery: Cargar los datos a diferentes datasets o tablas.
