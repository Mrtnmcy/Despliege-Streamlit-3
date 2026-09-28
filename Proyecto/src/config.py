# Ubicacion: src/config.py
from pathlib import Path

# ===============
# 1. Rutas
# ===============

# Raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Directorios importantes
DATA_DIR = BASE_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw" 
DATA_PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"

# Rutas de archivos de entrada
FILE_INGRESOS = DATA_RAW_DIR / "ingresos_municipales_2024.xlsx"
FILE_EDUCACION = DATA_RAW_DIR / "educacion_censada_2024.xlsx"
FILE_POBLACION = DATA_RAW_DIR / "poblacion_censada_2024.xlsx"
FILE_DESECHOS_MUNI = DATA_RAW_DIR / "desechos_municipales_2024.xlsx"

# Ruta a archivo procesado
MASTER_DATASET_PATH = DATA_PROCESSED_DIR / "master_comunal_2024.csv"


# ===============
# 2. Constantes
# ===============


REGIONES_SERVICIO = [ "Arica y Parinacota", 
                     "Antofagasta", 
                     "Coquimbo", 
                     "Valparaíso", 
                     "Metropolitana de Santiago"
                     "Libertador Gral. Bernardo O'Higgins", 
                     "Maule", 
                     "Biobío",
                     "Los Ríos",
                     "Ñuble"
                     ]

COMUNAS = ["Arica", "Antofagasta", "Coquimbo", "La Serena", 
           "Concón", "Viña del Mar", "Buin", "Calera de Tango", 
           "Cerrillos", "Cerro Navia", "Colina", "Conchalí",
           "Curacaví", "El Bosque", "Estación Central", 
           "Independencia", "La Cisterna","La Florida", "La Granja", 
           "La Pintana", "La Reina", "Lampa", "Lo Espejo",
           "Macul", "Maipú", "María Pinto", "Melipilla", "Ñuñoa", 
           "Padre Hurtado", "Paine", "Pedro Aguirre Cerda", 
           "Peñalolén", "Pirque", "Providencia","Pudahuel", 
           "Puente Alto", "Quinta Normal", "Renca", "San Bernardo",
           "San Joaquín", "San Miguel", "San Ramón", "Santiago", 
           "Talagante", "Vitacura", "Rancagua", "San Fernando", 
           "Curicó", "Talca", "Chillán", "Concepción", "Coronel", 
           "Hualpén", "San Pedro de la Paz", "Talcahuano","Valdivia"
           ]

SOLIDOSCOLS = ["año", "mes", "nombre_establecimiento", "razon_social",
               "region", "provincia", "codigo_unico_territorial","comuna", "latitud", "longitud",
               "tipo_recepcion", "cantidad_toneladas", "tratamiento_n1_name",
               "tratamiento_n2_name", "tratamiento_n3_name", "LER"]
EDUCACIONCOLS = ["Región", "Provincia", "Código comuna", "Comuna", 
                           "Sexo", "Años de escolaridad promedio"]
INGRESOSCOLS = ["CODIGO", "MUNICIPIO", "2024"]
POBLACIONCOLS = ["Región", "Provincia", "Código comuna", "Comuna", "Población censada"]

#SOLIDOS2024 = "./Databases/gm-sinader-2024-ckan.xlsx"
#EDUCACION2024 = "./Databases/P7_Educacion.xlsx"
#INGRESOS2024 = "./Databases/datos_municipales_20260926233528_Sin-Corrección-Monetaria.xlsx"
#POBLACION2024 = "./Databases/D1_Poblacion-censada-por-sexo-y-edad-en-grupos-quinquenales.xlsx"


