import reflex as rx

config = rx.Config(
    app_name="app",
    backend_url = "https://vseeker-backend.azurewebsites.net",
    frontend_url = "https://vseeker-frontend.azurewebsites.net",
    plugins=[rx.plugins.TailwindV3Plugin()]
)
