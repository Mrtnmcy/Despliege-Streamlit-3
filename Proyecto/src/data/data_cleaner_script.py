from pathlib import Path
import pandas as pd
import numpy as np
from src.config import MASTER_DATASET_PATH, INGRESOSCOLS, FILE_INGRESOS, EDUCACIONCOLS, FILE_EDUCACION, POBLACIONCOLS, FILE_POBLACION, SOLIDOSCOLS, FILE_DESECHOS_MUNI


def estandarizar_cut(data: pd.DataFrame, col_cut: str = "CUT") -> pd.DataFrame:
    """
    Asegura que el Código Único Territorial (CUT) sea una cadena de 5 dígitos
    rellenando con ceros a la izquierda (ej. 5101 -> '05101'). 
    """
    df = data.copy()
    df[col_cut] = (
            df[col_cut]
            .astype(str)
            .str.split(pat = ".")
            .str[0]
            .str.zfill(5)
            )
    df = df.where(df[col_cut].str.isdigit()).dropna(how = "all")
    return df


def limpiar_ingresos_municipales(filepath: Path = FILE_INGRESOS) -> pd.DataFrame:
    """ 
    Carga y limpia la base de Ingresos Municipales 2024 (SINIM). 
    """
    df = pd.read_excel(filepath, skiprows = [0,1], usecols = INGRESOSCOLS)
    df.rename(columns = {
        "CODIGO":"CUT",
        "MUNICIPIO":"comuna",
        "2024":"ingreso_2024_miles"
        }, inplace = True)
    df = estandarizar_cut(df)
    return df


def limpiar_educacion_censo(filepath: Path = FILE_EDUCACION) -> pd.DataFrame:
    """ 
    Carga y limpia la base de Nivel Educacional del Censo 2024 (Hoja 4). 
    """
    df = pd.read_excel(filepath, sheet_name = "4", skiprows = [0,1,2], usecols = EDUCACIONCOLS)
    df.rename(columns = {
        "Comuna": "comuna",
        "Código comuna": "CUT",
        "Región": "region",
        "Provincia": "provincia",
        "Años de escolaridad promedio": "educacion_promedio"
        }, inplace = True)
    df = df[(df["Sexo"] == "Total Comuna") & (df["region"] != "País")].drop(columns = "Sexo")
    df = estandarizar_cut(df, "CUT")
    return df


def limpiar_poblacion_censo(filepath: Path = FILE_POBLACION) -> pd.DataFrame:
    """
    Carga y limpia la base de Población Censada 2024 (Hoja 2).
    """
    df = pd.read_excel(filepath, sheet_name = "2", skiprows = [0,1,2], usecols = POBLACIONCOLS)
    df.rename(columns = {
        "Código comuna":"CUT",
        "Población censada":"poblacion_total_2024",
        "Región":"region",
        "Provincia":"provincia",
        "Comuna":"comuna"
        }, inplace = True)
    df = df[df["region"] != "País"]
    df = estandarizar_cut(df, "CUT")
    return df


def limpiar_desechos_muni(filepath: Path = FILE_DESECHOS_MUNI) -> pd.DataFrame:
    df = pd.read_excel(filepath, sheet_name = "Datos", usecols = SOLIDOSCOLS)
    df.rename(columns = {
        "codigo_unico_territorial":"CUT"
        }, inplace = True)
    df = estandarizar_cut(df, "CUT")
    return df


def ejecutar_pipeline_limpieza() -> pd.DataFrame:
    """
    Función orquestadora que carga todas las fuentes, ejecuta los joins 
    y guarda el dataset maestro consolidado en /data/processed/.
    """ 
    print("Iniciando pipeline de limpieza de datos...")
    df_ingresos = limpiar_ingresos_municipales()
    print("Datos de ingresos limpiados...")
    df_educacion = limpiar_educacion_censo()
    print("Datos de educacion limpiados...")
    df_poblacion = limpiar_poblacion_censo()
    print("Datos de poblacion limpiados...")
    df_desechos = limpiar_desechos_muni()
    print("Datos de desechos limpios")
    print("Uniendo tablas...")
    
    shared_key_ingresos = df_ingresos.columns.intersection(df_desechos.columns).drop("CUT")
    shared_key_educacion = df_educacion.columns.intersection(df_desechos.columns).drop("CUT")
    shared_key_poblacion = df_poblacion.columns.intersection(df_desechos.columns).drop("CUT")
    df_ingresos = df_ingresos.drop(columns=shared_key_ingresos)
    df_educacion = df_educacion.drop(columns=shared_key_educacion)
    df_poblacion = df_poblacion.drop(columns=shared_key_poblacion)
    master = df_desechos.merge(df_ingresos, on = "CUT", how = "left")
    master = master.merge(df_educacion, on = "CUT", how = "left")
    master = master.merge(df_poblacion, on = "CUT", how = "left")
    master.to_csv(MASTER_DATASET_PATH, index = False, sep = ";", encoding = "utf-8-sig")
    print(f"Datasets unidos y guardados exitosamente en: {MASTER_DATASET_PATH}")
    return master

