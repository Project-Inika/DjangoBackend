from django.urls import path
from .views import ApiConnectionView, ImageResultsView, TextSearchResultsView, ImageSearchView

urlpatterns = [path('apiConnection/', ApiConnectionView.as_view(), name='api_connection'), path('imageResults/', ImageResultsView.as_view(), name='image_results'), path('textSearch/', TextSearchResultsView.as_view(), name='text_search'), path('imageSearch/', ImageSearchView.as_view(), name='image_search')]
