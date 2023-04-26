from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="job_index"),
    path('create/', create, name="jobs_create"),
    path('<int:job_id>/', show, name="job_details"),
    path('accounts/signup/', signup, name='signup'),
    path('accounts/login/', login_user, name="login"),
    path('<int:user_id>/logout', logout, name="logout"),
    path('get_user', get_user_from_token, name="fetch_user")
]
