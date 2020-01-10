from django.urls import path

from . import views

# Namespace of the app
app_name = 'tunesweeper'

# Note: All the urlpatterns need to have a unique route and the name just allows
# for referral elsewhere - see:
#   https://docs.djangoproject.com/en/3.0/intro/tutorial01/#path-argument-route
# for more details
urlpatterns = [
	path("", views.index, name="index"),
	path("game/", views.game_interface, name="game_interface"),
]
