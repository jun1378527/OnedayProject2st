from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('<int:pk>/', views.review_detail, name='review_detail'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_review, name='create_review'),
    path('<int:pk>/delete/', views.delete_review, name='delete_review'),
    path('graph_visualization/', views.graph_visualization, name='graph_visualization'),
    path('heap_tree/', views.heap_tree, name='heap_tree'),
    path('binary_tree/', views.binary_tree, name='binary_tree'),
    path('quick_sort/', views.quick_sort, name='quick_sort'),
]
