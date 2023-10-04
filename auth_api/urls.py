from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # get token
    path(
        "get-token/", obtain_auth_token, name="get-token"
    ),
]
