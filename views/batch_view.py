import flet as ft
import os
from utils.ffmpeg_engine import run_conversion
from utils.config_loader import APP_DATA

def BatchVideoView(page: ft.Page):
    files_view = ft.Column(scroll=ft.ScrollMode.AUTO)
    stored_paths = []
    stored_files_info = []  # Store file info (name, type, etc.)
    
    # Variables for configuration
    selected_format = None
    selected_bitrate = None
    selected_fps = None
    selected_resolution = None
    custom_width = None
    custom_height = None
    selected_crf = None
    
    def get_file_type(file_path):
        """Determine if file is video, image, or audio"""
        ext = os.path.splitext(file_path)[1].lower()
        image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.webp', '.gif', '.tiff']
        audio_exts = ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg']
        video_exts = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
        
        if ext in image_exts:
            return "image"
        elif ext in audio_exts:
            return "audio"
        elif ext in video_exts:
            return "video"
        else:
            return "unknown"

    def on_files_picked(e):
        if e.files:
            # Group files by type and limit to 10 per type
            video_count = 0
            image_count = 0
            audio_count = 0
            
            for f in e.files:
                file_type = get_file_type(f.path)
                
                # Skip if we've reached the limit for this type
                if file_type == "video" and video_count >= 10:
                    continue
                elif file_type == "image" and image_count >= 10:
                    continue
                elif file_type == "audio" and audio_count >= 10:
                    continue
                elif file_type == "unknown":
                    continue
                
                # Add to appropriate counter
                if file_type == "video":
                    video_count += 1
                elif file_type == "image":
                    image_count += 1
                elif file_type == "audio":
                    audio_count += 1
                
                stored_paths.append(f.path)
                stored_files_info.append({
                    'name': f.name,
                    'type': file_type,
                    'size': f.size
                })
                
                # Get appropriate icon
                icon_name = "movie" if file_type == "video" else "image" if file_type == "image" else "audiotrack"
                icon_color = "blue" if file_type == "video" else "green" if file_type == "image" else "orange"
                
                files_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(name=icon_name, color=icon_color),
                            ft.Text(f.name, size=14),
                            ft.Text(f"({file_type})", size=12, color="grey")
                        ], spacing=10),
                        padding=10,
                        bgcolor="#1AFFFFFF", 
                        border_radius=5,
                        animate=ft.Animation(200, "easeOut")
                    )
                )
            
            files_view.update()
            
            # Show summary
            if video_count > 0 or image_count > 0 or audio_count > 0:
                summary_text = f"Añadidos: {video_count} videos, {image_count} imágenes, {audio_count} audios"
                page.snack_bar = ft.SnackBar(ft.Text(summary_text))
                page.snack_bar.open = True
                page.update()

    def _open_batch_options_dialog(e):
        if not stored_paths:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor añade archivos primero"))
            page.snack_bar.open = True
            page.update()
            return
        
        # Determine what types of files we have
        file_types = set(info['type'] for info in stored_files_info)
        has_video = "video" in file_types
        has_image = "image" in file_types
        has_audio = "audio" in file_types
        
        # Create appropriate format options
        format_options = []
        if has_video:
            format_options.extend(["mp4", "avi", "mkv", "mov"])
        if has_image:
            format_options.extend(["png", "jpg", "webp", "bmp", "tiff"])
        if has_audio:
            format_options.extend(["mp3", "wav", "flac", "aac", "m4a"])
        
        # Default format based on primary type
        default_fmt = "mp4" if has_video else "png" if has_image else "mp3"
        
        # Create UI controls based on file types
        tf_name = ft.TextField(label="Nombre base para archivos", value="converted", dense=True)
        dd_format = ft.Dropdown(label="Formato de Salida", options=[ft.dropdown.Option(f) for f in format_options], value=default_fmt)
        
        controls = [tf_name, dd_format]
        
        # Add video-specific controls
        if has_video:
            dd_fps = ft.Dropdown(
                label="FPS",
                options=[ft.dropdown.Option(o) for o in ["Mantener", "24", "30", "60"]],
                value="Mantener"
            )
            dd_resolution = ft.Dropdown(
                label="Resolución",
                options=[ft.dropdown.Option(o) for o in ["Mantener", "480p", "720p", "1080p", "Personalizado"]],
                value="Mantener"
            )
            tf_width = ft.TextField(label="Ancho", value="", dense=True, keyboard_type=ft.KeyboardType.NUMBER, visible=False)
            tf_height = ft.TextField(label="Alto", value="", dense=True, keyboard_type=ft.KeyboardType.NUMBER, visible=False)
            
            def on_res_change(e):
                show_custom = dd_resolution.value == "Personalizado"
                tf_width.visible = show_custom
                tf_height.visible = show_custom
                page.update()
            
            dd_resolution.on_change = on_res_change
            dd_quality = ft.Dropdown(
                label="Calidad",
                options=[ft.dropdown.Option(o) for o in ["Auto", "High", "Medium", "Low", "CRF Manual"]],
                value="Auto"
            )
            slider_crf = ft.Slider(min=18, max=28, divisions=10, value=23, label="{value}", visible=False)
            
            def on_quality_change(e):
                show_crf = dd_quality.value == "CRF Manual"
                slider_crf.visible = show_crf
                page.update()
            
            dd_quality.on_change = on_quality_change
            
            controls.extend([dd_fps, dd_resolution, tf_width, tf_height, dd_quality, slider_crf])
        
        # Add image-specific controls
        if has_image and not has_video:
            dd_resolution = ft.Dropdown(
                label="Tamaño",
                options=[ft.dropdown.Option(o) for o in ["Mantener", "480p", "720p", "1080p", "Personalizado"]],
                value="Mantener"
            )
            tf_width = ft.TextField(label="Ancho", value="", dense=True, keyboard_type=ft.KeyboardType.NUMBER, visible=False)
            tf_height = ft.TextField(label="Alto", value="", dense=True, keyboard_type=ft.KeyboardType.NUMBER, visible=False)
            
            def on_res_change(e):
                show_custom = dd_resolution.value == "Personalizado"
                tf_width.visible = show_custom
                tf_height.visible = show_custom
                page.update()
            
            dd_resolution.on_change = on_res_change
            controls.extend([dd_resolution, tf_width, tf_height])
        
        def close_dlg(e):
            dialog.open = False
            page.update()
        
        def proceed(e):
            # Store configuration
            nonlocal selected_format, selected_fps, selected_resolution, custom_width, custom_height, selected_crf
            
            selected_format = dd_format.value
            if has_video:
                selected_fps = dd_fps.value
                selected_resolution = dd_resolution.value
                custom_width = tf_width.value if tf_width.visible else None
                custom_height = tf_height.value if tf_height.visible else None
                selected_crf = slider_crf.value if hasattr(slider_crf, 'visible') and slider_crf.visible else None
            elif has_image and not has_video:
                selected_resolution = dd_resolution.value
                custom_width = tf_width.value if tf_width.visible else None
                custom_height = tf_height.value if tf_height.visible else None
            
            dialog.open = False
            page.update()
            
            # Start processing
            process_batch_with_config()
        
        content_controls = ft.Container(
            content=ft.Column(controls, spacing=15, scroll=ft.ScrollMode.AUTO),
            padding=20,
            border_radius=15,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.with_opacity(0.1, "purple"), ft.Colors.with_opacity(0.1, "deeppurple")]
            ),
            animate=ft.Animation(300, "easeOut")
        )
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Opciones de Conversión por Lotes"),
            content=content_controls,
            actions=[ft.TextButton("Cancelar", on_click=close_dlg), ft.TextButton("Continuar", on_click=proceed)],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialog
        dialog.open = True
        page.update()

    def process_batch_with_config():
        if not stored_paths:
            return

        prog_bar = ft.ProgressBar(width=400, color="amber")
        files_view.controls.append(prog_bar)
        files_view.update()

        count = 0
        errors = 0
        
        for i, path in enumerate(stored_paths):
            try:
                file_info = stored_files_info[i]
                file_type = file_info['type']
                
                # Generate output path
                base_name = os.path.splitext(os.path.basename(path))[0]
                output_name = f"{base_name}_converted.{selected_format}"
                output_path = os.path.join(os.path.dirname(path), output_name)
                
                # Determine encoder based on file type and format
                encoder = "libx264"  # Default
                if file_type == "audio":
                    encoder = "mp3" if selected_format == "mp3" else "aac"
                elif file_type == "image":
                    encoder = selected_format
                
                # Prepare parameters
                fps = selected_fps if file_type == "video" and selected_fps != "Mantener" else None
                width = custom_width if custom_width else None
                height = custom_height if custom_height else None
                crf = selected_crf if file_type == "video" and selected_crf else None
                
                # Run conversion
                success, message = run_conversion(
                    path, output_path, encoder,
                    fps=fps, width=width, height=height, crf=crf
                )
                
                if success:
                    count += 1
                else:
                    errors += 1
                    
            except Exception as ex:
                errors += 1
                print(f"Error processing {path}: {ex}")
        
        files_view.controls.remove(prog_bar)
        
        # Show completion notification
        if errors == 0:
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ Se completaron {count} archivos exitosamente"))
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ Completados: {count}, ❌ Errores: {errors}"))
        
        page.snack_bar.open = True
        page.update()

    def clear_list(e):
        stored_paths.clear()
        stored_files_info.clear()
        files_view.controls.clear()
        files_view.update()
        page.snack_bar = ft.SnackBar(ft.Text("Lista limpiada"))
        page.snack_bar.open = True
        page.update()

    file_picker = ft.FilePicker()
    file_picker.on_result = on_files_picked
    page.overlay.append(file_picker)
    page.update()

    return ft.Column([
        ft.Text("Modo Lote Multi-Formato", size=25, weight="bold"),
        ft.Text("Convierte hasta 10 archivos del mismo tipo (video, imagen o audio)."),
        ft.Row([
            ft.ElevatedButton("Añadir Archivos", icon="add", on_click=lambda _: file_picker.pick_files(allow_multiple=True)),
            ft.ElevatedButton("Limpiar Lista", icon="delete", color="red", on_click=clear_list)
        ]),
        ft.Container(
            content=files_view,
            height=300,
            border=ft.border.all(1, "grey"),
            border_radius=8,
            padding=10
        ),
        ft.ElevatedButton(
            "Configurar y Procesar Todo", 
            icon="settings", 
            on_click=_open_batch_options_dialog, 
            bgcolor="green", 
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=15
            )
        )
    ], spacing=15)