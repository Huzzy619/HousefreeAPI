from pyotp import HOTP, random_base32


class OTPView:


    def __init__(self, **kwargs) -> None:
        self.secret_key = '5NFWHMRBTBZETE3KDA2VJPIOFDBIN5QW'


    def get_otp(self, user_id):

        hotp = HOTP(self.secret_key)

        otp = hotp.at(user_id)

        # request.session["value"] = otp

        return ""

    # def check_otp(self, request):


    #     otp = serializer.validated_data["otp"]
    #     hotp = request.session.get("value", "")
    #     if hotp:
    #         if hotp.verify(otp, 1):

    #             # user = request.user
    #             # user.is_verified = True
    #             # user.save()
    #             return Response(
    #                 {"success": "2FA successful"}, status=status.HTTP_202_ACCEPTED
    #             )

    #         return Response({"error": "invalid otp"})

    #     return Response({"no value"})
