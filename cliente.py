import requests

BASE_URL = 'http://127.0.0.1:5000'

usuario_actual = ""

def registrar():
    usuario = input("Usuario nuevo: ")
    contraseña = input("Contraseña: ")
    res = requests.post(f'{BASE_URL}/registro', json={'usuario': usuario, 'contraseña': contraseña})
    try:
        print(res.json())
    except ValueError:
        print("Error interpretando respuesta del servidor:", res.text)

def login():
    global usuario_actual
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    res = requests.post(f'{BASE_URL}/login', json={'usuario': usuario, 'contraseña': contraseña})
    try:
        data = res.json()
        print(data)
        if res.status_code == 200:
            usuario_actual = usuario
            menu_usuario()
    except ValueError:
        print("Respuesta inválida del servidor:", res.text)

def mostrar_tareas():
    res = requests.get(f'{BASE_URL}/tareas', params={'usuario': usuario_actual})
    print("Respuesta del servidor:")
    print(res.text)

def agregar_tarea():
    descripcion = input("Descripción de la tarea: ")
    res = requests.post(f'{BASE_URL}/agregar_tarea', json={'usuario': usuario_actual, 'descripcion': descripcion})
    try:
        print(res.json())
    except ValueError:
        print("Error interpretando respuesta del servidor:", res.text)

def eliminar_tarea():
    tarea_id = input("ID de la tarea a eliminar: ")
    url = f"{BASE_URL}/tareas/{tarea_id}"
    res = requests.delete(url)
    try:
        print(res.json())
    except ValueError:
        print("Error interpretando respuesta del servidor:", res.text)

def menu():
    while True:
        print("\n1. Registrar\n2. Login\n3. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            registrar()
        elif opcion == '2':
            login()
        elif opcion == '3':
            break
        else:
            print("Opción no válida.")

def menu_usuario():
    while True:
        print("\n1. Ver tareas\n2. Agregar tarea\n3. Eliminar tarea\n4. Cerrar sesión")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            mostrar_tareas()
        elif opcion == '2':
            agregar_tarea()
        elif opcion == '3':
            eliminar_tarea()
        elif opcion == '4':
            break
        else:
            print("Opción no válida.")

if __name__ == '__main__':
    menu()
