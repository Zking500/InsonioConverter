import flet as ft

class StoreView(ft.Container):
    def __init__(self, page, set_theme_callback):
        super().__init__()
        self.page = page
        self.set_theme_callback = set_theme_callback
        self.expand = True
        self.padding = 20
        self.content = self._build_ui()

    def _build_ui(self):
        return ft.Column([
            ft.Text("Tienda de Diseños", size=30, weight="bold"),
            ft.Text("Personaliza tu experiencia Insonio", size=16, color="grey"),
            
            ft.Divider(height=20, color="transparent"),
            
            # --- Sección Gratuitos ---
            ft.Text("Temas Gratuitos", size=20, weight="bold"),
            ft.Row([
                self._build_theme_card("Oscuro (Base)", ft.Colors.BLUE_GREY_900, ft.Colors.WHITE, "dark"),
                self._build_theme_card("Claro", ft.Colors.WHITE, ft.Colors.BLACK, "light"),
                self._build_theme_card("Insonio Red", ft.Colors.BLACK, ft.Colors.RED, "red"),
            ], wrap=True, spacing=20),
            
            ft.Divider(height=40, color="grey"),
            
            # --- Sección Pro ---
            ft.Row([
                ft.Icon(name="lock", color="amber"),
                ft.Text("Versión Pro (Exclusivos)", size=20, weight="bold", color="amber"),
            ]),
            ft.Text("Desbloquea temas premium y apoya el desarrollo.", size=14),
            
            ft.Row([
                self._build_pro_card("Gold King", ft.Colors.AMBER),
                self._build_pro_card("Cyberpunk Neon", ft.Colors.PURPLE),
                self._build_pro_card("Matrix", ft.Colors.GREEN),
            ], wrap=True, spacing=20),
            
            ft.Container(height=20),
            
            ft.ElevatedButton(
                "Comprar Versión Pro",
                icon="shopping_cart",
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.AMBER_700,
                    color="white",
                    padding=20,
                    text_style=ft.TextStyle(size=18, weight="bold")
                ),
                on_click=lambda _: self.page.launch_url("https://google.com") # URL de ejemplo
            )
            
        ], scroll=ft.ScrollMode.AUTO)

    def _build_theme_card(self, title, bg_color, text_color, theme_id):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    width=100, height=60, 
                    bgcolor=bg_color,
                    border=ft.border.all(1, "grey"),
                    border_radius=5
                ),
                ft.Text(title, weight="bold", size=14),
                ft.ElevatedButton("Aplicar", on_click=lambda _: self.set_theme_callback(theme_id), height=30)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
            border=ft.border.all(1, "grey"),
            border_radius=10,
            bgcolor=ft.Colors.with_opacity(0.1, "grey"),
            width=150,
            height=180
        )

    def _build_pro_card(self, title, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(name="lock_outline", size=40, color=color),
                ft.Text(title, weight="bold", size=14),
                ft.Text("PRO", size=10, color="amber", weight="bold")
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
            border=ft.border.all(1, color),
            border_radius=10,
            width=150,
            height=120,
            opacity=0.7
        )
