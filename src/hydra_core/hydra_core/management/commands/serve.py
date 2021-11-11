"""
Django admin waitress integration.
"""

from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.core.wsgi import get_wsgi_application
import environ
from paste.translogger import TransLogger
import waitress

env = environ.Env()

DEFAULT_LISTEN_ADDRESS = env("LISTEN_ADDRESS", default="127.0.0.1:8000")
DEFAULT_THREADS = env(
    "THREADS", default=waitress.adjustments.Adjustments.threads
)


class Command(BaseCommand):
    """
    Starts a new server listening on the supplied listen address.

    Args:
        --threads: The number of threads
        listen_address: The listen address and port
    """

    help = "Starts a production-ready web server"

    def add_arguments(self, parser):
        parser.add_argument(
            "--threads",
            type=int,
            default=DEFAULT_THREADS,
            help=f"Number of threads (default: {DEFAULT_THREADS}",
        )
        parser.add_argument(
            "listen_address",
            nargs="?",
            default=DEFAULT_LISTEN_ADDRESS,
            help=f"Listen address (default: {DEFAULT_LISTEN_ADDRESS}",
        )

    def handle(self, *args, **options):

        if not settings.DEBUG and not settings.ALLOWED_HOSTS:
            raise CommandError(
                "You must set settings.ALLOWED_HOSTS if DEBUG is false."
            )

        if settings.DEBUG:
            self.stdout.write(
                "Warning! Never run with DEBUG enabled in production!",
                style_func=self.style.ERROR,
            )

        self.stdout.write(
            f"Server listening on http://{options['listen_address']} "
            f"using {options['threads']} threads"
        )

        application = get_wsgi_application()
        waitress.serve(
            TransLogger(application),
            listen=options["listen_address"],
            threads=options["threads"],
            _quiet=True,
        )
