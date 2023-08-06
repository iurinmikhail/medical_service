from django.urls import path
from .views import RefbookListView

urlpatterns = [

    path('', RefbookListView.as_view(), name='refbook-list'),
    # path('[?date=<date>/]', RefbooksListView.as_view(), name='refbooks-list'),
    # path('', get_refbooks, name='get_refbooks'),

]