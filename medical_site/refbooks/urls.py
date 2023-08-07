from django.urls import path
from .views import DirectoryView, ElementView, CheckElementView

urlpatterns = [
    path("", DirectoryView.as_view(), name="refbook-directory"),
    path("<int:id>/elements/", ElementView.as_view(), name="refbook-elements"),
    path("<int:id>/check_element", CheckElementView.as_view(), name="check-element"),
]
