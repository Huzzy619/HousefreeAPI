from django.urls import path

from . import views

urlpatterns = [
    path('blogs/', views.BlogListView.as_view(), name='blog-list'),
    # path('blogs/create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('blogs/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    # path('blogs/<int:pk>/update/', views.BlogUpdateView.as_view(), name='blog-update'),
    # path('blogs/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog-delete'),
]
