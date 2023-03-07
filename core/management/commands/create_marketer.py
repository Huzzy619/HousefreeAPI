from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError, CommandParser

from blog.models import Blog, Image

from django.contrib.auth import get_user_model




class Command(BaseCommand):
    help = "Creates the Marketer groups so that users that will post blogs can be added"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "emails", nargs="+", type=str, help="Email address of the user to be added"
        )

        parser.add_argument(
            "--remove",
            # action=
            help=" Remove users from the marketers group",
        )

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name="Marketers and Content Writers"
        )

        blog_content_type = ContentType.objects.get_for_model(Blog)

        blog_permissions = Permission.objects.filter(content_type=blog_content_type)

        for permission in blog_permissions:

            group.permissions.add(permission)

        image_content_type = ContentType.objects.get_for_model(Image)

        image_permissions = Permission.objects.filter(content_type=image_content_type)

        for permission in image_permissions:

            group.permissions.add(permission)


        User = get_user_model()
        for email in options["emails"]:
            try:
                user = User.objects.get(email = email)
            except user.DoesNotExist:
                raise CommandError(f"User with email~{email} does not exist")
            
            user.groups.add(nm)

        if options['remove']:

            get_user_model().objects.filter(email__in = options["emails"] )


        self.stdout.write(
            self.style.SUCCESS(f"{group.name} Group created successfully")
        )
