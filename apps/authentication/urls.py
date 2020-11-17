from django.urls import path
from . import views

# auth/
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_step_1'),
    path('register/<str:email>/step/<int:step>', views.RegisterView.as_view(),
         name='register_steps')
]
