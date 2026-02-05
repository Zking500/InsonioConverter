import flet as ft
import time
import threading

class PremiumView(ft.Container):
    def __init__(self, page, on_activate_premium):
        super().__init__()
        self.page = page
        self.on_activate_premium = on_activate_premium
        self.expand = True
        
        self.content = self._build_ui()

    def _build_ui(self):
        return ft.Column([
            ft.Icon(name="diamond", size=100, color="amber"),
            ft.Text("InsonioConverter Premium", size=30, weight="bold", color="amber"),
            ft.Text("¡Desbloquea el poder del ORO!", size=16),
            ft.Container(height=20),
            ft.Container(
                content=ft.Column([
                    ft.Row([ft.Icon("check", color="green"), ft.Text("Tema Dorado Exclusivo")]),
                    ft.Row([ft.Icon("check", color="green"), ft.Text("Soporte para desarrollador hambriento")]),
                    ft.Row([ft.Icon("check", color="green"), ft.Text("Estado 'Troll King'")]),
                ]),
                padding=20,
                border=ft.border.all(1, "amber"),
                border_radius=10
            ),
            ft.Container(height=40),
            ft.ElevatedButton(
                "Pagar $1 Dolar",
                icon="attach_money",
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.AMBER_600,
                    color="black",
                    padding=20,
                    text_style=ft.TextStyle(size=18, weight="bold"),
                    shape=ft.RoundedRectangleBorder(radius=10)
                ),
                on_click=self._process_payment
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def _process_payment(self, e):
        # Deshabilitar botón
        btn = e.control
        original_text = btn.text
        btn.disabled = True
        btn.text = "Procesando..."
        btn.update()
        
        # Función en hilo para no congelar
        def process():
            time.sleep(2) # Simular red
            
            # Callback en el hilo principal
            def on_success():
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("¡Pago recibido! Activando Modo Dorado...", color="black"),
                    bgcolor="amber"
                )
                self.page.snack_bar.open = True
                self.page.update()
                
                # Activar modo
                self.on_activate_premium()
                
                # Restaurar botón (aunque ya sea premium)
                btn.text = "¡Ya eres Premium!"
                btn.update()

            # Ejecutar update en hilo principal si es necesario, pero Flet suele manejarlo bien si se tiene cuidado
            # O mejor, usar page.run_task si estuviera disponible, pero aquí llamaremos directo.
            # Nota: En Flet las actualizaciones de UI deben ser thread-safe, a veces directo funciona, a veces no.
            # Lo más seguro es no usar threads para UI updates complejos, pero aquí es simple.
            
            on_success()

        threading.Thread(target=process).start()
