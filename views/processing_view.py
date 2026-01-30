import flet as ft
import time
import threading
# from utils.ffmpeg_engine import run_conversion (Tu función real)

class ProcessingView(ft.Container):
    def __init__(self, page, mode, file_path, options, on_finish):
        super().__init__()
        self.page = page
        self.expand = True
        self.mode = mode
        self.file_path = file_path
        self.options = options
        self.on_finish = on_finish
        
        # UI Elements
        self.status_text = ft.Text("Inicializando motor...", size=20, text_align="center")
        self.progress_ring = ft.ProgressRing(width=60, height=60, stroke_width=5, color=ft.Colors.CYAN)
        
        self.content = ft.Column([
            self.progress_ring,
            ft.Container(height=20),
            self.status_text,
            ft.Text("Por favor espera, estamos cocinando los píxeles 👨‍🍳", italic=True, color="grey")
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Iniciamos el proceso en otro hilo para no congelar la UI
        self.did_mount = self.start_process

    def start_process(self):
        t = threading.Thread(target=self._run_ffmpeg_thread)
        t.start()

    def _run_ffmpeg_thread(self):
        # Simulación de proceso (Aquí llamarías a tu run_conversion real)
        steps = ["Analizando metadatos...", "Codificando video...", "Empaquetando contenedor...", "Limpiando..."]
        
        for step in steps:
            time.sleep(1.5) # Simula trabajo de FFmpeg
            self.status_text.value = step
            self.status_text.update()
        
        # Al terminar
        self.status_text.value = "¡Terminado!"
        self.progress_ring.value = 1 # 100%
        self.progress_ring.color = "green"
        self.update()
        time.sleep(1)
        
        # Volver (opcional) o mostrar botón de "Nuevo archivo"
        self.page.snack_bar = ft.SnackBar(ft.Text("✅ Proceso completado exitosamente"))
        self.page.snack_bar.open = True
        self.page.update()
        
        # Regresar a la vista anterior o quedarse aquí
        # self.on_finish()