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

if st.button("Buscar recetas"):
    if ingredientes:
        # Convertir el tipo de comida al formato de la API (inglés)
        tipo_comida_api = {
            "Desayuno": "breakfast",
            "Almuerzo": "lunch",
            "Cena": "dinner",
            "Snack": "snack",
            "Postre": "dessert"
        }.get(tipo_comida, None)

        # Llamar al backend
        response = requests.get(
            "http://127.0.0.1:8000/recipes",
            params={
                "ingredients": ingredientes.split(","),
                "type": tipo_comida_api
            }
        )
        if response.status_code == 200:
            data = response.json()
            if "recipes" in data and len(data["recipes"]) > 0:
                for recipe in data["recipes"]:
                    # Mostrar cada receta con su imagen
                    st.subheader(recipe["name"])
                    st.image(recipe["image"], use_container_width=True)  # Cambio aquí
                    st.text("Ingredientes:")
                    st.write(", ".join(recipe["ingredients"]))
                    st.markdown(f"[Ver receta completa aquí]({recipe['url']})")
                    st.write("---")
            else:
                st.warning("No se encontraron recetas con esos ingredientes.")
        else:
            st.error("Hubo un problema al conectar con el servidor.")
    else:
        st.warning("Por favor, ingresa al menos un ingrediente.")
