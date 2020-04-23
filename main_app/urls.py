from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('new_user', views.new_user),
    path('login', views.login),
    path('all_books/<int:user_id>', views.all_books),
    path('add_book', views.add_book),
    path('process_new', views.process_new),
    path('logout', views.logout),
    path('one_book/<int:this_book_id>', views.one_book),
    path('add_review', views.add_review),
    path('user_page/<int:user_id>', views.user_page)
]