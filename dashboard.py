import pandas as pd
import plotly as px
import streamlit as st
import pydeck as pdk


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

SOLIDOS2024 = "./sample_data/gm-sinader-2024-ckan.xlsx"
df = pd.read_excel(SOLIDOS2024, sheet_name="Datos", 
                   usecols = ["año", "mes", "nombre_establecimiento", "razon_social", "region", 
                            "provincia", "comuna", "latitud", "longitud", 
                            "tipo_recepcion", "cantidad_toneladas", "tratamiento_n1_name",
                            "tratamiento_n2_name", "tratamiento_n3_name",
                            "trazabilidad__nombre_establecimiento","trazabilidad__razon_social", "trazabilidad__comuna",
                            "tipo_dato"]
                   )
df = df[df["region"].isin(REGIONES) & df["comuna"].isin(COMUNAS) & df["tratamiento_n1_name"].notna() & df["latitud"].notna() & df["longitud"].notna()]
st.session_state.dataframe=df

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
        get_fill_color = "[200,30,0,160]",
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


