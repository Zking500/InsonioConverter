import flet as ft
import asyncio
import threading
import time
from utils.config_loader import APP_DATA

class WelcomeWindow:
    def __init__(self, on_complete):
        self.on_complete = on_complete
        self.page = None
        self.should_close = False
    
    async def create_window(self):
        """Crea una ventana separada para la pantalla de bienvenida"""
        
        def main_welcome(page: ft.Page):
            self.page = page
            page.title = f"{APP_DATA['app_info']['name']} - Iniciando"
            page.window_width = 500
            page.window_height = 400
            page.window_resizable = False
            page.window_maximizable = False
            page.window_minimizable = False
            page.window_always_on_top = True
            page.theme_mode = "dark"
            page.padding = 20
            
            # Crear la vista de bienvenida
            from views.welcome_view import WelcomeView
            welcome_view = WelcomeView(page, lambda: self.signal_completion())
            page.add(welcome_view)
        
        # Crear la aplicación en una ventana separada
        await ft.app_async(target=main_welcome)
    
    def signal_completion(self):
        """Señaliza que la ventana debe cerrarse y continuar con la aplicación principal"""
        # Ejecutar on_complete directamente
        # No intentamos cerrar la ventana para evitar errores
        self.on_complete()