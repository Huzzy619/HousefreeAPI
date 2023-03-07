from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.core.validators import EmailValidator

from blog.models import Blog, Image

User = get_user_model()


class Command(BaseCommand):
    help = "Creates the Marketer groups so that users that will post blogs can be added"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--add",
            nargs="+",
            type=str,
            help="Email addresses of the users to be added",
            required=False,
        )

        parser.add_argument(
            "--remove",
            # action=
            help=" Remove users from the marketers group",
            type=str,
            nargs="+",
        )

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name="Marketers and Content Writers"
        )

        if emails := options.get("add", None):

            for email in emails:
                try:
                    validate = EmailValidator()
                    validate(email)
                except ValidationError as e:
                    raise CommandError(e.message)

            self.add_users(emails, group)

        elif emails := options.get("remove", None):

            self.remove_users(emails, group)

        else:

            self.create_group_permissions(group, [Blog, Image])

    def create_group_permissions(self, group, models: list):
        for model in models:
            content_type = ContentType.objects.get_for_model(model)

            model_permissions = Permission.objects.filter(content_type=content_type)

            for permission in model_permissions:

                group.permissions.add(permission)

        self.stdout.write(
            self.style.SUCCESS(
                f"{group.name} Group created successfully \n\n       Assigning permissions................... \n\n Permissions assigned. "
            )
        )

    def add_users(self, emails, group):

        for email in emails:
            try:

                user = User.objects.get(email=email)

            except User.DoesNotExist:
                raise CommandError(f"User with email ~ ({email}) does not exist")

            user.groups.add(group)

        return self.stdout.write(self.style.SUCCESS(f"User(s) added Successfully"))

    def remove_users(self, emails, group):

        users = User.objects.filter(email__in=emails)

        if users:
            for user in users:
                user.groups.remove(group)

            return self.stdout.write(
                self.style.SUCCESS(
                    f"User(s) removed Successfully from {group.name} Group"
                )
            )
        if len(emails) > 1:
            raise CommandError(f"Users do not exist")

        raise CommandError(f"User does not exist")
