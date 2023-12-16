from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_game, name='start_game'),  # Add this line
    path('game/<int:game_id>/', views.play_game, name='play_game'),
    path('win/<int:game_id>', views.win_view, name='win_view'),
    # You can add additional URLs here for other views, such as a win view, lobby view, etc.
]
