from django.apps import AppConfig

class UnoGameConfig(AppConfig):
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uno_game'

    def ready(self):
        import uno_game.signals  # Import the signals module
