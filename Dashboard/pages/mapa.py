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




st.session_state.dataframe = residuos_de_captura
st.session_state.tratamientos_unicos = st.session_state.dataframe["tratamiento_n1_name"].unique()

st.session_state.tratamiento_color_mapa = {tratamiento : TRATAMIENTOCOLOR[i % len(TRATAMIENTOCOLOR)]
                                           for i, tratamiento in enumerate(st.session_state.tratamientos_unicos)}

st.session_state.dataframe["color_capa"] = st.session_state.dataframe["tratamiento_n1_name"].map(st.session_state.tratamiento_color_mapa)

view_state = pdk.ViewState(
                latitude=-33.4489,
                longitude=-70.6693,
                zoom=11,
                pitch=30)
layer = pdk.Layer(
        "ScatterplotLayer",
        data=st.session_state.dataframe[st.session_state.dataframe["mes"] == 12],
        get_position=["longitud","latitud"],
        get_radius="cantidad_toneladas*0.1",
        get_fill_color = "color_capa",
        pickable=True,
        auto_highlight=True
        )
r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "text":"Comuna: {comuna}\nTratamiento: {tratamiento_n1_name}\nCantidad(Tm): {cantidad_toneladas}"},
        )
st.pydeck_chart(r,width="stretch")


#print(df.info())
#print(df.describe())


