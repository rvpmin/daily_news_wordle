import requests
import os
import json

api_key = os.getenv("NYT_API")
if not api_key:
    raise ValueError("NYT_API environment variable is not set.")

url = f"https://api.nytimes.com/svc/topstories/v2/world.json?api-key={api_key}"


try:
    response = requests.get(url)
    data = response.json()
    response.raise_for_status()


    with open('nyt_data.json', 'w', encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False, indent=4)

    print(f"Total de artículos recibidos: {len(data.get('results', []))}")

except requests.exceptions.RequestException as e:
    print(f"Error en la solicitud: {e}")
except json.JSONDecodeError:
    print("Error al decodificar la respuesta JSON")
except Exception as e:
    print(f"Error inesperado: {e}")
#print("https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key=uAoMAen9WjPa9A0GXsDI39V5u92XdT59"== response.request.url)
