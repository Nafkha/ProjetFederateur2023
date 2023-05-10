from django.apps import AppConfig
from django.db.models.signals import post_migrate

class JoboffersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'joboffers'

    def ready(self):
        # import the signal handlers
        from .signals import handle_algolia_update

        # register the signal handlers
        post_migrate.connect(handle_algolia_update, sender=self)