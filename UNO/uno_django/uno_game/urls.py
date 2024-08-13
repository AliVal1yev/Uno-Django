from django.urls import path
from . import views

urlpatterns = [
    path('game/<int:game_id>/', views.game_view, name='game_view'),
    path('game/<int:game_id>/color/', views.ask_color, name='ask_color'),
    path('new/', views.create_game, name='create_game'),
    path('game/<int:game_id>/next_player/', views.next_player, name='next_player'),
]
