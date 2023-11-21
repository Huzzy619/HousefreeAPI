from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsMarketerOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    message = "This user does not have access to post/edit blogs"

    def has_permission(self, request, view):
        """
        Except the user is in a group (Marketers and Content Writers) or is a superuser,
        They would not be able to make changes to the blog

        They would only have READ permission
        Args:
            request (_type_): _description_
            view (_type_): _description_

        Returns:
            _type_: boolean

        """
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.groups.filter(
                name="Marketers and Content Writers"
            ).exists()
            or request.user.is_superuser
        )
