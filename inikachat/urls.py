from django.urls import path
from .views import StartOutfitsView, EditOutfitsView

urlpatterns = [path('startOutfits/', StartOutfitsView.as_view(), name='start_outfits'), path('editOutfits/', EditOutfitsView.as_view(), name='edit_outfits')]