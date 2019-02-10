"""Debug runserver."""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Command."""

    def handle(self, *args, **options):
        call_command(
            "runserver",
            use_threading=False,
            use_reloader=False
        )
