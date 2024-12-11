import streamlit as st
import pandas as pd
import os
from PIL import Image
from streamlit_option_menu import option_menu

# Chemin des images
image_folder = os.path.join(os.getcwd(), "images")

# Charger les utilisateurs depuis le fichier CSV
users = pd.read_csv("users.csv", sep=";")

# Interface utilisateur pour la connexion
st.sidebar.title("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

# Initialiser l'état de session si non défini
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Vérification des informations d'identification
if st.sidebar.button("Login"):
    user = users[(users['name'] == username) & (users['password'] == password)]
    if not user.empty:
        st.session_state['authenticated'] = True
        st.sidebar.success(f"Bienvenue {username}!")
    else:
        st.session_state['authenticated'] = False
        st.sidebar.error("Nom d'utilisateur ou mot de passe incorrect.")

# Fonction pour redimensionner les images avec Pillow
def resize_image(image_path, size=(900, 800)):
    image = Image.open(image_path)
    image = image.resize(size)  # Redimensionner à la taille spécifiée
    return image

# Vérification de l'authentification
if st.session_state['authenticated']:
    # Menu latéral
    with st.sidebar:
        selection = option_menu(
            menu_title="Navigation",
            options=["Accueil", "Photos"],
            icons=["house", "camera"],
            menu_icon="cast",
            default_index=0,
        )

    # Page d'accueil
    if selection == "Accueil":
        st.title("Bienvenue sur la page d'accueil !")
        st.image(os.path.join(image_folder, "stadium.jpg"), caption="Bienvenue au stade", use_container_width=True)

    # Page photos
    elif selection == "Photos":
        st.title("Album photos des champions")

        # Utiliser des colonnes uniformes et afficher des images redimensionnées
        col1, col2, col3 = st.columns([1, 1, 1])  # Colonnes avec proportions égales

        with col1:
            st.image(resize_image(os.path.join(image_folder, "jordan.jpg")), caption="Michael Jordan")
        with col2:
            st.image(resize_image(os.path.join(image_folder, "marchand.jpg")), caption="Léon Marchand")
        with col3:
            st.image(resize_image(os.path.join(image_folder, "zidane.jpg")), caption="Zinedine Zidane")

    # Bouton de déconnexion
    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        st.sidebar.success("Vous avez été déconnecté.")
        st.experimental_rerun()  # Recharge l'application pour actualiser l'état

else:
    st.warning("Veuillez vous connecter pour accéder au contenu.")