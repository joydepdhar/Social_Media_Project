from django.urls import path
from social_media import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/',views.comment_post, name='comment_post'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path("search/", views.search_view, name="search"),
]