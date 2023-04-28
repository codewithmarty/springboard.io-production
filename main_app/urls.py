from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('<int:user_id>/my_created_jobs/', get_my_created_jobs),
    path('<int:user_id>/my_applied_jobs/', get_my_applied_jobs),
    path('create/', create),
    path('<int:user_id>/create_job/', create_job),
    path('<int:user_id>/get_applications/<int:job_id>/', get_application),
    path('<int:user_id>/apply/<int:job_id>/', apply_to_job),
    path('<int:job_id>/', show),
    path('accounts/signup/', signup),
    path('accounts/login/', login_user),
    path('<int:user_id>/logout', logout),
    path('get_user', get_user_from_token),
    path('<int:user_id>/<int:job_id>/delete/', delete_job)
]
