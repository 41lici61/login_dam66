import flet as ft
from UsersBBDD import *
from datetime import datetime


def main(page: ft.Page):
    page.title = "login"
    page.window_width = 400
    page.window_height = 600
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"


    nombre_usuario = ft.TextField(label="Nombr", autofocus=True)
    apellidos = ft.TextField(label="Apellidos")
    email = ft.TextField(label="Email")
    password = ft.TextField(label="Contraseña", password=True)
    fecha_nacimiento = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)")
    mensaje = ft.Text()


    rol = ft.Dropdown(
        label="Selecciona el rol", width=400,
        options=[
            ft.dropdown.Option("user", "Usuario"),
            ft.dropdown.Option("admin", "Administrador")
        ],
        value="user"  # Valor por defecto
    )

    def set_mensaje(texto, color="pink"):
        mensaje.value = texto
        mensaje.color = color
        page.update()

    def limpiar_campos():
        nombre_usuario.value = ""
        apellidos.value = ""
        email.value = ""
        password.value = ""
        fecha_nacimiento.value = ""
        mensaje.value = ""
        rol.value = None
        page.update()

    def register(e):
        try:

            datetime.strptime(fecha_nacimiento.value, "%Y-%m-%d")
        except ValueError:
            set_mensaje("Error: Formato de fecha incorrecto. Usa YYYY-MM-DD.", "red")
            return

        # Verificar que el nombre de usuario no esté vacío
        if not nombre_usuario.value:
            set_mensaje("Error: El nombre de usuario no puede estar vacío.", "red")
            return


        if not apellidos.value:
            set_mensaje("Error: Los apellidos no pueden estar vacíos.", "red")
            return


        if not email.value:
            set_mensaje("Error: El email no puede estar vacío.", "red")
            return


        if not password.value:
            set_mensaje("Error: La contraseña no puede estar vacía.", "red")
            return


        if not rol.value:
            set_mensaje("Error: Debes seleccionar un rol (Usuario o Administrador).", "red")
            return

        msg = registrar_usuario(nombre_usuario.value, apellidos.value, email.value, password.value,
                                fecha_nacimiento.value, rol.value)
        set_mensaje(msg, "green" if "éxito" in msg else "red")
        if "éxito" in msg:
            limpiar_campos()

    def mostrar_registro(e=None):
        limpiar_campos()
        page.clean()
        page.add(
            ft.Column([
                nombre_usuario, apellidos, email, password, fecha_nacimiento, rol, mensaje,
                ft.ElevatedButton("Registrar", on_click=register, bgcolor="green", color="white"),
                ft.ElevatedButton("Volver", on_click=mostrar_login, bgcolor="gray", color="white")
            ], alignment="center")
        )
        page.update()

    def mostrar_login(e=None):
        limpiar_campos()
        page.clean()
        email.label = "Email/Usuario"  # Cambiar la etiqueta a "Email/Usuario"
        page.add(
            ft.Column([
                email, password, mensaje,
                ft.ElevatedButton("Iniciar sesión", on_click=login, bgcolor="pink", color="white"),
                ft.ElevatedButton("Registrarse", on_click=mostrar_registro, bgcolor="pink", color="white")
            ], alignment="center")
        )
        page.update()

    def login(e):
        user = verificar_usuario(email.value, password.value)
        if user:
            ultimo_login = user[9] if user[9] else "Nunca"
            set_mensaje("Login exitoso!", "green")
            page.clean()

            if user[10] == "admin":
                mostrar_home(user[1], ultimo_login, es_admin=True)
            else:
                mostrar_home(user[1], ultimo_login, es_admin=False)


            page.add(
                ft.ElevatedButton("Iniciar Aplicación", on_click=iniciar_aplicacion, bgcolor="blue", color="white")
            )

            page.update()
        else:
            set_mensaje("Email/Usuario o contraseña incorrectos. Por favor, intenta nuevamente.", "red")

    def iniciar_aplicacion(e):
        import ActionSelector
        ActionSelector.main(page)

    def mostrar_home(nombre_usuario, ultimo_login, es_admin=False):
        page.clean()
        column_elements = [
            ft.Text(f"Bienvenido, {nombre_usuario}!", size=20, weight="bold", color="blue"),
            ft.Text(f"Último login: {ultimo_login}", size=14, italic=True, color="gray"),
            ft.ElevatedButton("Cerrar sesión", on_click=logout, bgcolor="blue", color="white"),
            ft.ElevatedButton("Eliminar cuenta", on_click=eliminar, bgcolor="red", color="white")
        ]

        if es_admin:
            column_elements.append(
                ft.ElevatedButton("Panel de Administrador",
                                  on_click=lambda e: panel_admin(nombre_usuario, ultimo_login), bgcolor="purple",
                                  color="white")
            )

        page.add(ft.Column(column_elements, alignment="center"))
        page.update()

    def panel_admin(nombre_usuario, ultimo_login):
        page.clean()
        page.add(
            ft.Text("Bienvenido al Panel de Administrador", size=20, weight="bold", color="blue"),
            ft.ElevatedButton("Volver al inicio",
                              on_click=lambda e: mostrar_home(nombre_usuario, ultimo_login, es_admin=True),
                              bgcolor="gray", color="white")
        )
        page.update()

    def eliminar(e):
        user = verificar_usuario(email.value, password.value)
        print(f"Datos del usuario: {user}")
        if user:
            user_id = user[0]
            print(f"El ID del usuario a eliminar es: {user_id}")
            mensaje = eliminar_usuario(user_id)
            set_mensaje(mensaje, "green" if "eliminado" in mensaje else "red")
            limpiar_campos()
            mostrar_login()
        else:
            set_mensaje("No se pudo eliminar la cuenta.", "red")

    def logout(e):
        limpiar_campos()
        mostrar_login()

    mostrar_login()


if __name__ == "__main__":
    ft.app(target=main)
