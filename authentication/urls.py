'''
    Views for Authentication and profile pages using
    path.
    Authentication is the process of determining whether someone or something
    is, in fact, who or what it says it is.

    Login, Sign Up and Profile view
    '''
from django.urls import path, include
from authentication.views import (ActivateUser, )

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/user/activate/<uid>/<token>/',
         ActivateUser.as_view({'get': 'activation'})),
]
