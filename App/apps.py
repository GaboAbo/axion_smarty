"""
App configuration for the 'App' Django application.

This module sets up the application configuration and ensures that signals are imported
when the app is ready.
"""

from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    Configuration class for the 'App' application.

    Attributes:
        default_auto_field (str): The default field type for auto-generated primary keys.
        name (str): The full Python path to the application.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'

    def ready(self):
        """
        Hook for application initialization.

        This method is called when the application is fully loaded. It imports
        the `signals` module to register model signals.
        """
        import App.signals
