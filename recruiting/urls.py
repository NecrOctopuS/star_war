from django.urls import path
from . import views


app_name = 'recruiting'


urlpatterns = [
    path('', views.choice, name='choice'),
    path('for_sith/', views.for_sith, name='for_sith'),
    path('for_recruit/', views.for_recruit, name='for_recruit'),
    path('<int:planet_id>/recruit_data/', views.recruit_data, name='recruit_data'),
    path('<int:planet_id>/recruit_data/create_recruit/', views.create_recruit, name='create_recruit'),
    path('<int:recruit_id>/test/', views.test, name='test'),
    path('<int:recruit_id>/test/send_test', views.send_test, name='send_test'),
    path('<int:sith_id>/sith_data/', views.sith_data, name='sith_data'),
    path('<int:sith_id>/sith_data/accept_recruit', views.accept_recruit, name='accept_recruit'),
]
