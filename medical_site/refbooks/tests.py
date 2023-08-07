from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import datetime
from .models import Directory, Version, Element


class RefbookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.directory = Directory.objects.create(code="1", name="Справочник1")
        self.version = Version.objects.create(
            directory=self.directory, version="1.0", start_date=datetime.now()
        )
        self.element = Element.objects.create(
            directory_version=self.version, element_code="E01", element_value="Хирург"
        )

    def test_get_directory(self):

        response = self.client.get(reverse("refbook-directory"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["refbooks"]), 1)

    def test_get_elements(self):
        response = self.client.get(
            reverse("refbook-elements", args=[self.directory.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["elements"]), 1)

    def test_check_element(self):
        data = {"code": self.element.element_code, "value": self.element.element_value}
        response = self.client.get(
            reverse("check-element", args=[self.directory.id]),
            data={
                "code": self.element.element_code,
                "value": self.element.element_value,
            },
        )
        self.assertEqual(response.status_code, 200)
