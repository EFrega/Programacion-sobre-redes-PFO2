import requests

BASE_URL = 'http://127.0.0.1:5000'

def registrar():
    usuario = input("Usuario nuevo: ")
    contraseña = input("Contraseña: ")
    res = requests.post(f'{BASE_URL}/registro', json={'usuario': usuario, 'contraseña': contraseña})
    print(res.json())

def login():
    global usuario_actual
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    res = requests.post(f'{BASE_URL}/login', json={'usuario': usuario, 'contraseña': contraseña})
    print(res.json())
    if res.status_code == 200:
        usuario_actual = usuario
        menu_usuario()

def mostrar_tareas():
    res = requests.get(f'{BASE_URL}/tareas', params={'usuario': usuario_actual})
    print("Respuesta del servidor:")
    print(res.text)

def agregar_tarea():
    descripcion = input("Descripción de la tarea: ")
    res = requests.post(f'{BASE_URL}/agregar_tarea', json={'usuario': usuario_actual, 'descripcion': descripcion})
    print(res.json())

def eliminar_tarea():
    tarea_id = input("ID de la tarea a eliminar: ")
    res = requests.post(f'{BASE_URL}/eliminar_tarea', json={'id': tarea_id})
    print(res.json())

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

usuario_actual = ""
if __name__ == '__main__':
    menu()
