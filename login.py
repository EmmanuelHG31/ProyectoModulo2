import requests

url = "http://127.0.0.1:5000/login"

datos_login = {
    "email": "emmanuel@usuario.com", 
    "password": "123456789"
}

try:
    respuesta = requests.post(url, json=datos_login)
    
    # Si la respuesta es exitosa (200)
    if respuesta.status_code == 200:
        print(f"Éxito: {respuesta.json().get('mensaje')}")
    else:
        # Imprimimos el texto crudo si no es JSON para ver el error real
        print(f"Error {respuesta.status_code}")
        print(f"Contenido de la respuesta: {respuesta.text}") 

except Exception as e:
    print(f"Error de conexión: {e}")