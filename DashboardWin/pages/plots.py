import pandas as pd
import streamlit as st
import plotly.express as px
# Pagina Mapa del Dashboard

st.set_page_config(page_title="Demo de mapa", page_icon=":material/map:")
st.markdown("# *Permoformance*")
st.sidebar.header("Demo de mapa")
st.markdown("""Los dos gráficos de abajo representan el comportamiento a lo largo del tiempo de/los KPI seleccionado/s, 
y una comparación entre el desempeño de cada comuna en un KPI.
         """)
# --------- Constantes --------- 
REGIONES = ['Antofagasta', 'Coquimbo', 'Valparaíso',
            "Libertador Gral. Bernardo O'Higgins", 'Maule', 'Biobío',
            'Metropolitana de Santiago','Los Ríos', 'Arica y Parinacota', 'Ñuble']

COMUNAS = ["Arica", "Antofagasta", "Coquimbo", "La Serena", "Concón", "Viña del Mar",
           "Buin", "Calera de Tango", "Cerrillos", "Cerro Navia", "Colina", "Conchalí",
           "Curacaví", "El Bosque", "Estación Central", "Independencia", "La Cisterna",
           "La Florida", "La Granja", "La Pintana", "La Reina", "Lampa", "Lo Espejo",
           "Macul", "Maipú", "María Pinto", "Melipilla", "Ñuñoa", "Padre Hurtado",
           "Paine", "Pedro Aguirre Cerda", "Peñalolén", "Pirque", "Providencia",
           "Pudahuel", "Puente Alto", "Quinta Normal", "Renca", "San Bernardo", 
           "San Joaquín", "San Miguel", "San Ramón", "Santiago", "Talagante",
           "Vitacura", "Rancagua", "San Fernando", "Curicó", "Talca", "Chillán",
           "Concepción", "Coronel", "Hualpén", "San Pedro de la Paz", "Talcahuano",
           "Valdivia"]

SOLIDOS2024 = "residuos-solidos-acumulados-2024.csv"
EXCOLS = ["año", "mes", "nombre_establecimiento", "razon_social", "region", 
                            "provincia", "comuna", "latitud", "longitud", 
                            "tipo_recepcion", "cantidad_toneladas", "tratamiento_n1_name",
                            "tratamiento_n2_name", "tratamiento_n3_name",
                            "trazabilidad__nombre_establecimiento","trazabilidad__razon_social", "trazabilidad__comuna",
                            "tipo_dato"]
TRATAMIENTOCOLOR = [
        [200, 30, 0, 160], #Rojo -> eliminación
        [0, 120, 200, 160], #Azul -> pretrataminento
        [40, 180, 40, 160], #Verde -> valorización
        ]

# --------- Constantes --------- 


# --------- Dataframe ---------  

residuos_de_captura = pd.read_csv(SOLIDOS2024, sep = ";")

# --------- Dataframe ---------  


# --------- Session state ---------  
st.session_state.dataframe = residuos_de_captura
st.session_state.tratamientos_unicos = st.session_state.dataframe["tratamiento_n1_name"].unique()

maximum = st.session_state.dataframe["cantidad_toneladas"].max()
minimum = st.session_state.dataframe["cantidad_toneladas"].min()

def color_rows_by_score(row):
    val = row["cantidad_toneladas"]
    ratio = (maximum - val) / (maximum - minimum)

    r = int(255 * ratio)
    g = int(255 * (1 - ratio))
    b = 0
    return [f"background-color: rgba({r}, {g}, {b}, 0.5)" for _ in row]



# --------- Session states ---------  


# --------- Elementos ---------  


# --------- Filtros --------- 



with st.sidebar:
    
    st.header("Filtro serie")
    series_region_seleccionada = st.selectbox("Region",
                                      ["Todas las regiones"] + REGIONES, key="serie_region")
    series_comuna_seleccionada = st.selectbox("Comuna",
                                       ["Todas las comunas"] + COMUNAS, key="serie_comuna")
    series_desecho_seleccionado = st.selectbox("Desecho",
                                        ["Acumulación total", "Eliminación", "Valorización", "Recepción y Almacenamiento"], key="serie_desecho")

    st.header("Filtro barra")
    barra_region_seleccionada = st.selectbox("Barra Region",
                                      ["Todas las regiones"] + REGIONES, key="barra_region")
    barra_desecho_seleccionado = st.selectbox("Barra Desecho",
                                        ["Acumulación total", "Eliminación", "Valorización", "Recepción y Almacenamiento"], key="barra_desecho")
    barra_mes_seleccionado = st.selectbox("Barra Mes", [i for i in range(1,13)], key="barra_mes" )


series_data = st.session_state.dataframe.copy()
barra_data = st.session_state.dataframe.copy()
barra_data = barra_data[barra_data["mes"] == barra_mes_seleccionado]
if series_region_seleccionada != "Todas las regiones":
    series_data = series_data[series_data["region"] == series_region_seleccionada]

if series_comuna_seleccionada != "Todas las comunas":
    series_data = series_data[series_data["comuna"] == series_comuna_seleccionada]

if series_desecho_seleccionado != "Acumulación total":
    series_data = series_data[series_data["tratamiento_n1_name"] == series_desecho_seleccionado]
    series_data = series_data.groupby(["region", "comuna"]).agg({"cantidad_toneladas":"sum",
                                                                                                                                                                  "longitud":"first",
                                                                                                                                                                  "latitud":"first",
                                                                                                                                                                  "tratamiento_n1_name":"first",
                                                                                                                                                                  "mes":"first"}).reset_index()

if barra_region_seleccionada != "Todas las regiones":
    barra_data = barra_data[barra_data["region"] == barra_region_seleccionada]

if barra_desecho_seleccionado != "Acumulación total":
    barra_data = barra_data[barra_data["tratamiento_n1_name"] == barra_desecho_seleccionado]
    barra_data = barra_data.groupby(["region", "comuna"]).agg({"cantidad_toneladas":"sum",                                                                                                                                                                "longitud":"first","latitud":"first", "tratamiento_n1_name":lambda x:None,"mes":lambda x:None}).reset_index()

# --------- Filtros ---------  


# --------- Mapa ---------  

serie_tiempo = px.line(series_data, x = "mes", y = "cantidad_toneladas", color = "tratamiento_n1_name")
barras = px.bar(barra_data, x = "comuna", y = "cantidad_toneladas")



# --------- Layout ---------  
maincol1, maincol2 = st.columns([3,1])

with maincol1:
    st.plotly_chart(serie_tiempo)
    st.plotly_chart(barras)

with maincol2:
    st.metric(label="Total Reciclado", value="1,500 Ton", delta="+5%", border = True)
    st.metric(label="Familias Activas", value="12,000", delta="800", border = True)
    st.metric(label="Tasa de Captura", value="65%", delta="2%", border = True)
    st.metric(label="Meta Alcanzada", value="85%", delta="-1%", border = True)
# --------- Mapa ---------  

#print(df.info())
#print(df.describe())


