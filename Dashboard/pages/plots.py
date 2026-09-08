import pandas as pd
import streamlit as st
import pydeck as pdk

# Pagina Mapa del Dashboard

st.set_page_config(page_title="Demo de mapa", page_icon=":material/map:")
st.markdown("# Mapa de servicio")
st.sidebar.header("Demo de mapa")
st.write("""Este mapa representa las comunas con servicio de reciclaje ReSimple.
         El tamaño representa las toneladas de basura recolectadas por ReSimple mientras que el color representa el tipo de
         tratamiento de basura.""")
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

SOLIDOS2024 = "../Databases/residuos-solidos-acumulados-2024.csv"
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
st.session_state.tratamiento_color_mapa = {tratamiento : TRATAMIENTOCOLOR[i % len(TRATAMIENTOCOLOR)]
                                           for i, tratamiento in enumerate(st.session_state.tratamientos_unicos)}
st.session_state.dataframe["color_capa"] = st.session_state.dataframe["tratamiento_n1_name"].map(st.session_state.tratamiento_color_mapa)
dataframe_filtrado = st.session_state.dataframe[(st.session_state.dataframe["mes"] == 12)]

maximum = dataframe_filtrado["cantidad_toneladas"].max()
minimum = dataframe_filtrado["cantidad_toneladas"].min()

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
    st.header("Filtros de Mapa")
    desecho_seleccionado = st.selectbox("Tipo de desecho", 
                                     ["Todo tipo de desecho"] + st.session_state.tratamientos_unicos.tolist())
    region_seleccionada = st.selectbox("Región", 
                                       ["Todas las regiones"] + REGIONES)

if region_seleccionada != "Todas las regiones":
        dataframe_filtrado = dataframe_filtrado[dataframe_filtrado["region"] == region_seleccionada]
if desecho_seleccionado != "Todo tipo de desecho":
        dataframe_filtrado = dataframe_filtrado[st.session_state.dataframe["tratamiento_n1_name"] == desecho_seleccionado]


# --------- Filtros ---------  


# --------- Mapa ---------  

view_state = pdk.ViewState(
                latitude=-33.4489,
                longitude=-70.6693,
                zoom=11,
                pitch=30)

layer = pdk.Layer(
        "ScatterplotLayer",
        data = dataframe_filtrado,
        get_position = ["longitud","latitud"],
        get_radius = "cantidad_toneladas*0.1",
        get_fill_color = "color_capa",
        pickable = True,
        auto_highlight = True
        )
r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "text":"Comuna: {comuna}\nTratamiento: {tratamiento_n1_name}\nCantidad(Tm): {cantidad_toneladas}"},
        )

maincol1, maincol2 = st.columns([3,1])

with maincol1:
    st.pydeck_chart(r,width="stretch")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Reciclado", value="1,500 Ton", delta="+5%", border = True)
    with col2:
        st.metric(label="Familias Activas", value="12,000", delta="800", border = True)
    with col3:
        st.metric(label="Tasa de Captura", value="65%", delta="2%", border = True)
    with col4:
        st.metric(label="Meta Alcanzada", value="85%", delta="-1%", border = True)

with maincol2:
    tonelaje = dataframe_filtrado["cantidad_toneladas"].to_frame().style.apply(color_rows_by_score, axis = 1)
    st.dataframe(tonelaje, height = "stretch", hide_index=True,
                 column_config = {
                     "cantidad_toneladas":st.column_config.NumberColumn("Desechos Recolectados", format="%f Tn")
                     }
                 )
# --------- Mapa ---------  

#print(df.info())
#print(df.describe())


