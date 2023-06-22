from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import HTTP_HEADER_ENCODING, exceptions


def enforce_csrf(request):
    check = CSRFCheck()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)


class CustomAuthentication(JWTAuthentication):

    def authenticate(self, request):
        user_cookie = request.COOKIES.get("access")
        if user_cookie:
            token = user_cookie.encode(HTTP_HEADER_ENCODING)
            validated_token = self.get_validated_token(token)

            return self.get_user(validated_token), validated_token
        return None
