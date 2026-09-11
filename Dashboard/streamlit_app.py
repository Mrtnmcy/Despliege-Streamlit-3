import streamlit as st

#Configuración de la pagina inicial
st.set_page_config(page_title="Priorización de servicio",
                   layout = "wide",
                   initial_sidebar_state="collapsed")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
# Boton de login
def login():
    st.title("Bienvenido al priorizador de servicio de ReSimple")
    st.subheader("Por favor inicie sesión para continuar")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type = "password")
    if st.button("Iniciar Sesión"):
        if username == "admin" and password == "admin123":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("El usuario o contraseña son invalidos")

#  Dialogo de logout
@st.dialog("Cerrar sesión")
def logout():
    st.write("¿Estas seguro de que quieres cerrar tu sesión?")
    if st.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.rerun()


login_page = st.Page(login, title = "Log in", icon=":material/login:")
logout_page = st.Page(logout, title = "Log out", icon=":material/logout:")
map_page = st.Page("./pages/mapa.py", title = "Mapa de\npriorización", icon=":material/map:")
series_page = st.Page("./pages/plots.py", title = "Gráfico de Performance")
if st.session_state.authenticated == True:
    pg = st.navigation(
            {
                "Reportes":[map_page, series_page],
                "Sesión":[logout_page],
                }
            )
else:
    pg = st.navigation([login_page])
pg.run()
