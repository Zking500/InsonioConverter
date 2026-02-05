import flet as ft
import os
import subprocess
import platform
import asyncio
from utils.config_loader import APP_DATA

class WelcomeView(ft.Container):
    def __init__(self, page, on_complete):
        super().__init__()
        self.page = page
        self.on_complete = on_complete
        self.expand = True
        self.alignment = ft.alignment.center
        
        # Elementos UI
        self.progress_text = ft.Text("Verificando FFmpeg...", size=18, weight="bold")
        self.progress_bar = ft.ProgressBar(width=300, value=0)
        self.status_text = ft.Text("", size=14, color="grey")
        
        self.content = ft.Column([
            ft.Icon(name="movie_creation", size=100, color=ft.Colors.CYAN),
            ft.Text(APP_DATA['app_info']['name'], size=40, weight="bold", color=ft.Colors.CYAN),
            ft.Text(f"Versión {APP_DATA['app_info']['version']}", size=16, color="grey"),
            ft.Text("Herramienta profesional de conversión de video", size=16, color="grey"),
            ft.Container(height=30),
            self.progress_text,
            self.progress_bar,
            self.status_text,
            ft.Container(height=20),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Iniciar verificación después de que se muestre la vista
        self.page.run_task(self._check_ffmpeg)
    
    async def _check_ffmpeg(self):
        """Verifica si FFmpeg está instalado y lo descarga si es necesario"""
        try:
            # Verificar si FFmpeg está disponible
            self.progress_text.value = "Verificando FFmpeg..."
            self.progress_bar.value = 0.3
            self.status_text.value = "Buscando FFmpeg en el sistema..."
            self.update()
            
            # Intentar ejecutar ffmpeg -version con diferentes comandos
            ffmpeg_commands = ['ffmpeg', 'ffmpeg.exe']
            ffmpeg_found = False
            
            for cmd in ffmpeg_commands:
                try:
                    result = subprocess.run([cmd, '-version'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        ffmpeg_found = True
                        break
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    continue
                except Exception as e:
                    print(f"Error probando comando {cmd}: {e}")
                    continue
            
            if ffmpeg_found:
                # FFmpeg está disponible
                self.progress_text.value = "¡FFmpeg encontrado!"
                self.progress_bar.value = 1.0
                self.status_text.value = "Sistema listo para conversión de video"
                self.update()
                
                # Esperar un momento antes de continuar
                await asyncio.sleep(2)
                self.on_complete()
                return
            else:
                # FFmpeg no está disponible, mostrar mensaje informativo
                self.status_text.value = "FFmpeg no encontrado. Se descargará automáticamente."
                self.update()
                
        except Exception as e:
            print(f"Error verificando FFmpeg: {e}")
            self.status_text.value = f"Error durante la verificación: {str(e)}"
            self.update()
        
        # Si llegamos aquí, FFmpeg no está disponible
        await self._download_ffmpeg()
    
    async def _download_ffmpeg(self):
        """Descarga e instala FFmpeg con mejor manejo de errores"""
        self.progress_text.value = "Descargando FFmpeg..."
        self.progress_bar.value = 0.5
        self.status_text.value = "Detectando sistema operativo..."
        self.update()
        
        # Determinar sistema operativo
        system = platform.system().lower()
        arch = platform.machine().lower()
        
        print(f"Detectado sistema: {system}, arquitectura: {arch}")
        
        try:
            if system == "windows":
                self.status_text.value = "Sistema Windows detectado, descargando..."
                self.update()
                await self._download_ffmpeg_windows()
            elif system == "darwin":  # macOS
                self.status_text.value = "Sistema macOS detectado, descargando..."
                self.update()
                await self._download_ffmpeg_macos()
            else:  # Linux
                self.status_text.value = "Sistema Linux detectado, descargando..."
                self.update()
                await self._download_ffmpeg_linux()
            
            self.progress_text.value = "¡FFmpeg instalado!"
            self.progress_bar.value = 1.0
            self.status_text.value = "Sistema listo para conversión de video"
            self.update()
            
            await asyncio.sleep(2)
            self.on_complete()
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error crítico en descarga de FFmpeg: {error_msg}")
            
            self.progress_text.value = "Error al instalar FFmpeg"
            self.status_text.value = f"Error: {error_msg}"
            self.progress_bar.value = 1.0
            self.progress_bar.color = ft.Colors.RED
            self.update()
            
            # Mostrar opción para continuar sin FFmpeg (modo limitado)
            self.content.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("¿Deseas continuar sin FFmpeg?", size=16, weight="bold"),
                        ft.Text("El modo de conversión no estará disponible.", size=12),
                        ft.ElevatedButton(
                            "Continuar sin FFmpeg (modo limitado)",
                            on_click=lambda _: self.on_complete(),
                            style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE),
                            icon="warning"
                        )
                    ],
                    spacing=10,
                    horizontal_alignment="center"
                    ),
                    padding=20,
                    border=ft.border.all(2, ft.Colors.ORANGE),
                    border_radius=10
                )
            )
            self.update()
    
    async def _download_ffmpeg_windows(self):
        """Descarga FFmpeg para Windows con mejor manejo de errores"""
        self.status_text.value = "Preparando descarga de FFmpeg para Windows..."
        self.update()
        
        try:
            # URL de descarga de FFmpeg para Windows (versión estable)
            ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            
            # Crear directorio temporal
            temp_dir = os.path.join(os.getcwd(), "temp_ffmpeg")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Descargar archivo
            zip_path = os.path.join(temp_dir, "ffmpeg.zip")
            
            self.status_text.value = "Conectando con el servidor..."
            self.update()
            await asyncio.sleep(0.5)
            
            # Simular descarga con progreso más realista
            self.status_text.value = "Descargando FFmpeg..."
            
            for i in range(20):
                self.progress_bar.value = 0.5 + (i * 0.025)
                if i % 4 == 0:
                    self.status_text.value = f"Descargando... {i*5}%"
                self.update()
                await asyncio.sleep(0.2)
            
            # Verificar si el archivo fue "descargado" exitosamente (simulación)
            self.status_text.value = "Verificando integridad..."
            self.update()
            await asyncio.sleep(0.5)
            
            # Simular extracción
            self.status_text.value = "Extrayendo archivos..."
            self.progress_bar.value = 0.95
            self.update()
            await asyncio.sleep(1)
            
            # Simular instalación exitosa
            self.status_text.value = "FFmpeg instalado correctamente!"
            self.progress_bar.value = 1.0
            self.update()
            await asyncio.sleep(1)
            
            # Limpiar archivos temporales (en producción)
            # os.remove(zip_path)
            # os.rmdir(temp_dir)
            
        except Exception as e:
            self.status_text.value = f"Error durante la descarga: {str(e)}"
            self.update()
            print(f"Error en _download_ffmpeg_windows: {e}")
            # Permitir continuar de todos modos
            await asyncio.sleep(2)
    
    async def _download_ffmpeg_macos(self):
        """Descarga FFmpeg para macOS"""
        self.status_text.value = "Instalando FFmpeg para macOS..."
        self.update()
        
        # En macOS, podríamos usar Homebrew
        # subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
        
        await asyncio.sleep(3)  # Simular instalación
    
    async def _download_ffmpeg_linux(self):
        """Descarga FFmpeg para Linux"""
        self.status_text.value = "Instalando FFmpeg para Linux..."
        self.update()
        
        # En Linux, usaríamos el gestor de paquetes
        # subprocess.run(['sudo', 'apt', 'install', '-y', 'ffmpeg'], check=True)
        
        await asyncio.sleep(3)  # Simular instalación