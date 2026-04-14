import requests

url = "http://127.0.0.1:5000/actualizar"

datos_actualizar = {
    "email": "emmanuel@usuario.com", 
    "password": "123456789",  
    "role": "admin"
}

respuesta = requests.put(url, json=datos_actualizar)
print(f"Resultado: {respuesta.status_code} - {respuesta.json()}")   