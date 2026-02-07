import flet as ft
import time
import threading
import os
import winsound
from utils.ffmpeg_engine import run_conversion

class ProcessingView(ft.Container):
    def __init__(self, page, mode, file_path, options, on_finish):
        super().__init__()
        self.page = page
        self.expand = True
        self.mode = mode
        self.file_path = file_path
        self.options = options
        self.on_finish = on_finish
        
        # Audio Player
        self.audio_player = ft.Audio(
            src="assets/notification.wav", 
            autoplay=False
        )
        self.page.overlay.append(self.audio_player)
        self.page.update()
        
        # UI Elements
        self.status_text = ft.Text("Inicializando motor...", size=20, text_align="center")
        self.progress_ring = ft.ProgressRing(width=60, height=60, stroke_width=5, color=ft.Colors.CYAN)
        
        # Mostrar ruta de salida si está disponible
        output_path = options.get('output_path', 'Ubicación predeterminada')
        output_info = ft.Text(f"Guardando en: {output_path}", 
                             size=12, color="grey", text_align="center")
        
        self.content = ft.Column([
            self.progress_ring,
            ft.Container(height=20),
            self.status_text,
            output_info,
            ft.Text("Por favor espera, estamos cocinando los píxeles 👨‍🍳", italic=True, color="grey")
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Iniciamos el proceso en otro hilo para no congelar la UI
        self.did_mount = self.start_process

    def start_process(self):
        t = threading.Thread(target=self._run_ffmpeg_thread)
        t.start()

    def _run_ffmpeg_thread(self):
        # Obtener la ruta de salida de las opciones
        output_path = self.options.get('output_path')
        
        if not output_path:
             self.status_text.value = "❌ Error: No hay ruta de salida"
             self.progress_ring.color = "red"
             self.update()
             return

        self.status_text.value = "Procesando..."
        self.update()

        # Llamada real al motor
        # Determinar encoder basado en aceleración por hardware
        hw_accel = self.options.get('hardware_acceleration', 'cpu')
        encoder = 'libx264' # Default CPU
        
        if hw_accel == 'cuda':
            encoder = 'h264_nvenc'
        elif hw_accel == 'qsv':
            encoder = 'h264_qsv'
        elif hw_accel == 'opencl':
            encoder = 'h264_amf'
            
        quality = self.options.get('quality_preset', 'Auto')
        fps_opt = self.options.get('target_fps')
        res = self.options.get('target_resolution')
        width_opt = self.options.get('custom_width')
        height_opt = self.options.get('custom_height')
        crf_opt = self.options.get('crf')
        target_h = None
        target_w = None
        if res == "480p":
            target_h = 480
        elif res == "720p":
            target_h = 720
        elif res == "1080p":
            target_h = 1080
        elif res == "1440p":
            target_h = 1440
        elif res and "2160" in res:
            target_h = 2160
        if height_opt:
            target_h = height_opt
        if width_opt:
            target_w = width_opt
        
        success, message = run_conversion(self.file_path, output_path, encoder, quality, fps=fps_opt, target_width=target_w, target_height=target_h, crf=crf_opt)
        
        if success:
            try:
                # Intentar reproducir audio personalizado si existe
                if os.path.exists("assets/notification.wav"):
                    self.audio_player.play()
                else:
                    winsound.MessageBeep(winsound.MB_OK)
            except:
                pass # Ignorar si falla el sonido
            self.status_text.value = "¡Terminado!"
            self.progress_ring.value = 1 # 100%
            self.progress_ring.color = "green"
            self.page.snack_bar = ft.SnackBar(ft.Text(message))
            self.page.snack_bar.open = True
        else:
            self.status_text.value = message
            self.progress_ring.value = 0
            self.progress_ring.color = "red"
            
        self.update()
        
        if success:
            time.sleep(2)
            # Opcional: Llamar a on_finish si queremos volver atrás automáticamente
            # self.on_finish()
