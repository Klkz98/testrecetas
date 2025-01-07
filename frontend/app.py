import streamlit as st
import requests

st.title("Recomendador de Recetas Rápidas 🍳")

# Entrada de ingredientes
ingredientes = st.text_input("Ingresa los ingredientes (separados por comas):")

# Selector de tipo de comida
tipo_comida = st.selectbox(
    "Selecciona el tipo de comida:",
    ["", "Desayuno", "Almuerzo", "Cena", "Snack", "Postre"],
    format_func=lambda x: "Cualquiera" if x == "" else x
)

# Botón para buscar recetas
if st.button("Buscar recetas"):
    if ingredientes:
        # Traducción del tipo de comida al formato de la API de Spoonacular
        tipo_comida_api = {
            "Desayuno": "breakfast",
            "Almuerzo": "lunch",
            "Cena": "dinner",
            "Snack": "snack",
            "Postre": "dessert"
        }.get(tipo_comida, None)

        try:
            # Llamada al backend
            response = requests.get(
                "https://testrecetas.onrender.com/recipes",  # URL del backend
                params={
                    "ingredients": ingredientes.split(","),
                    "type": tipo_comida_api
                }
            )

            # Verificar respuesta del backend
            if response.status_code == 200:
                data = response.json()
                if "recipes" in data and len(data["recipes"]) > 0:
                    for recipe in data["recipes"]:
                        # Mostrar cada receta con su imagen
                        st.subheader(recipe["name"])
                        st.image(recipe["image"], use_container_width=True)
                        st.text("Ingredientes:")
                        st.write(", ".join(recipe["ingredients"]))
                        st.markdown(f"[Ver receta completa aquí]({recipe['url']})")
                        st.write("---")
                else:
                    st.warning("No se encontraron recetas con esos ingredientes.")
            else:
                st.error("Hubo un problema al conectar con el backend.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error al conectar con el servidor: {e}")
    else:
        st.warning("Por favor, ingresa al menos un ingrediente.")
