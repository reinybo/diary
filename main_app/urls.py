from django.urls import path
from . import views

urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('entries/', views.entries_index, name='index'),
    path('entries/<int:entry_id>/', views.entry_detail, name='detail'),
    path('entries/create/', views.EntryCreate.as_view(), name='entry_create'),
    path('entries/<int:pk>/update/', views.EntryUpdate.as_view(), name='entry_update'),
    path('entries/<int:pk>/delete/', views.EntryDelete.as_view(), name='entry_delete'),
    path('entries/<int:entry_id>/add_photo/', views.add_photo, name='add_photo'),
]