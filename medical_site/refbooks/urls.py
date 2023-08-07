from django.urls import path
from .views import DirectoryView, ElementView, CheckElementView, index

urlpatterns = [
    path("", index, name="refbook-directory"),
    path("refbooks/", DirectoryView.as_view(), name="refbook-directory"),
    path("refbooks/<int:id>/elements/", ElementView.as_view(), name="refbook-elements"),
    path("refbooks/<int:id>/check_element", CheckElementView.as_view(), name="check-element"),
]
