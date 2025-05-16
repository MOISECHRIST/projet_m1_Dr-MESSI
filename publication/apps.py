from django.apps import AppConfig


class PublicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'publication'

    def ready(self):
        import threading
        from .consumer import start_consumer

        # Lancer le consumer dans un thread séparé
        threading.Thread(target=start_consumer, daemon=True).start()