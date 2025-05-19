from django.apps import AppConfig


class AbonnementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'abonnement'

    def ready(self):
        import threading
        from .consumer import start_consumer

        # Lancer le consumer dans un thread séparé
        threading.Thread(target=start_consumer, daemon=True).start()