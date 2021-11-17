from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandError
from django.db import transaction

from hydra_core.auth import create_user

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a user"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, required=True)
        parser.add_argument("--password", type=str, required=True)
        parser.add_argument("--email", type=str)
        parser.add_argument("--super", action="store_true")
        parser.add_argument("--ignore-existing", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):

        is_existing = User.objects.filter(
            username=options["username"]
        ).exists()

        if is_existing:
            if options["ignore_existing"]:
                self.stderr.write(
                    self.style.WARNING(
                        "User %(username)s already exists" % options
                    )
                )
                return

            raise CommandError("User %(username)s already exists" % options)

        params = {
            "username": options["username"],
            "password": options["password"],
            "email": options["email"],
            "super": options["super"],
        }

        create_user(**params)

        self.stderr.write(
            self.style.SUCCESS(
                "Successfuly created user %(username)s" % options
            )
        )
