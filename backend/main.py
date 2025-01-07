import requests
from fastapi import FastAPI, Query
from typing import List

app = FastAPI()

# Tu API Key de Spoonacular
SPOONACULAR_API_KEY = "96a687a24f0e4287af7d5ab2314a81ea"

@app.get("/recipes")
def get_recipes(
    ingredients: List[str] = Query(...),
    meal_type: str = Query(None, alias="type")
):
    """
    Busca recetas en Spoonacular basadas en los ingredientes y el tipo de comida.
    """
    # Convierte los ingredientes en una lista separada por comas
    ingredients_query = ",".join(ingredients)

    # URL de la API de Spoonacular
    url = "https://api.spoonacular.com/recipes/findByIngredients"

    # Parámetros de la solicitud
    params = {
        "ingredients": ingredients_query,
        "number": 5,  # Número de recetas a devolver
        "apiKey": SPOONACULAR_API_KEY,
    }
    if meal_type:
        params["type"] = meal_type  # Filtrar por tipo de comida

    # Llama a la API
    response = requests.get(url, params=params)

    # Si la solicitud es exitosa, devuelve las recetas
    if response.status_code == 200:
        recipes = response.json()
        return {
            "recipes": [
                {
                    "name": recipe["title"],
                    "ingredients": [ingredient["name"] for ingredient in recipe["usedIngredients"]],
                    "url": f"https://spoonacular.com/recipe/{recipe['title'].replace(' ', '-').lower()}-{recipe['id']}",
                    "image": recipe["image"],  # Incluimos la imagen
                }
                for recipe in recipes
            ]
        }
    else:
        return {"error": "No se pudieron obtener las recetas. Inténtalo más tarde."}
