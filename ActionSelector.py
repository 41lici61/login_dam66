import flet as ft
import os
import signal
from crontab import CronTab


def main(page: ft.Page):
    page.title = "SELECCIONAR OPCIÓN"
    page.window_width = 400
    page.window_height = 600
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def ir_a_vista(e):
        page.clean()  # Limpia la pantalla antes de cambiar de vista

        if opcion_drop.value == "Control Usuarios":
            user_control()
        elif opcion_drop.value == "Copia Seguridad":
            copia_seguridad()

    # Dropdown con evento on_change
    opcion_drop = ft.Dropdown(
        label="Selecciona opción", width=400,
        options=[
            ft.dropdown.Option("Control Usuarios"),
            ft.dropdown.Option("Copia Seguridad"),
        ],
        on_change=ir_a_vista
    )

    # Vista principal
    def vista_principal():
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("Selecciona una opción:", size=20, weight="bold"),
                    opcion_drop
                ],
                alignment="center",
                horizontal_alignment="center"
            )
        )

    def user_control():
        page.clean()

        pid_input = ft.TextField(label="Introduce el PID", keyboard_type=ft.KeyboardType.NUMBER)
        result_text = ft.Text()

        def kill_process(e):
            try:
                pid = int(pid_input.value)
                os.kill(pid, signal.SIGKILL)  # Matar el proceso en Linux
                result_text.value = f"Proceso {pid} finalizado con éxito."
                result_text.color = "green"
            except ValueError:
                result_text.value = "Introduce un número válido."
                result_text.color = "red"
            except ProcessLookupError:
                result_text.value = f"No se encontró el proceso con PID {pid}."
                result_text.color = "red"
            except PermissionError:
                result_text.value = "No tienes permisos para finalizar este proceso."
                result_text.color = "red"

            page.update()

        btn_kill = ft.ElevatedButton("Finalizar Proceso", on_click=kill_process)
        btn_volver = ft.ElevatedButton("Volver", on_click=lambda e: vista_principal())

        page.add(
            ft.Column(
                [
                    ft.Text("Control de Usuarios", size=20, weight="bold"),
                    pid_input,
                    btn_kill,
                    result_text,
                    btn_volver
                ],
                alignment="center",
                horizontal_alignment="center"
            )
        )

    def copia_seguridad():
        page.clean()

        src_input = ft.TextField(label="Directorio de Origen", width=400)
        dest_input = ft.TextField(label="Directorio de Destino", width=400)

        # Lista de los días de la semana
        days_of_week = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        # Dropdown para seleccionar el día de la semana
        day_dropdown = ft.Dropdown(label="Día de la Semana", width=400,
                                   options=[ft.dropdown.Option(i) for i in days_of_week])

        minutes = [str(i).zfill(2) for i in range(60)]
        hours = [str(i).zfill(2) for i in range(24)]

        minute_dropdown = ft.Dropdown(label="Minuto", width=400, options=[ft.dropdown.Option(i) for i in minutes])
        hour_dropdown = ft.Dropdown(label="Hora", width=400, options=[ft.dropdown.Option(i) for i in hours])

        result_text = ft.Text()

        def show_alert(title, message):
            result_text.value = f"{title}: {message}"
            result_text.color = "red" if title == "Error" else "green"
            page.update()

        def schedule_backup(e):
            src = src_input.value.strip()
            dest = dest_input.value.strip()
            minute = minute_dropdown.value
            hour = hour_dropdown.value
            day = day_dropdown.value

            if not src or not dest:
                show_alert("Error", "Debes introducir ambos directorios.")
                return

            cron = CronTab(user=True)
            job = cron.new(command=f"cp -r {src} {dest}")

            # Convertir el día de la semana a un formato que crontab reconozca
            # Lunes -> 1, Martes -> 2, ..., Domingo -> 7
            days_mapping = {
                "Lunes": 1, "Martes": 2, "Miércoles": 3, "Jueves": 4, "Viernes": 5, "Sábado": 6, "Domingo": 7
            }

            cron_day = days_mapping.get(day, "*")  # Por defecto, se ejecutaría todos los días si no se encuentra el día

            # Programar la tarea en crontab para el día de la semana seleccionado
            job.setall(f"{minute} {hour} * * {cron_day}")

            cron.write()

            show_alert("Copia Programada", f"Copia de seguridad programada para {minute}:{hour} del {day}.")

        btn_schedule = ft.ElevatedButton("Programar Copia", on_click=schedule_backup)
        btn_volver = ft.ElevatedButton("Volver", on_click=lambda e: vista_principal())

        page.add(
            ft.Column(
                [
                    ft.Text("Copia de Seguridad", size=20, weight="bold"),
                    src_input,
                    dest_input,
                    minute_dropdown,
                    hour_dropdown,
                    day_dropdown,
                    btn_schedule,
                    result_text,
                    btn_volver
                ],
                alignment="center",
                horizontal_alignment="center"
            )
        )

    vista_principal()


if __name__ == "__main__":
    ft.app(target=main)
