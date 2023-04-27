from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="job_index"),
    path('create/', create, name="jobs_create"),
    path('<int:user_id>/create_job/', create_job, name="create_job"),
    path('<int:user_id>/apply/<int:job_id>/', apply_to_job, name="apply_to_job"),
    path('<int:job_id>/', show, name="job_details"),
    path('accounts/signup/', signup, name='signup'),
    path('accounts/login/', login_user, name="login"),
    path('<int:user_id>/logout', logout, name="logout"),
    path('get_user', get_user_from_token, name="fetch_user")
]
