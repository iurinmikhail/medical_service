from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Directory, Version
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Directory

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Directory


class RefbookListView(APIView):
    def get(self, request):
        date = self.request.query_params.get('date')

        if date:
            directories = Directory.objects.filter(
                version__start_date__lte=date).distinct()
        else:
            directories = Directory.objects.all()

        directory_data = []
        for directory in directories:
            if date:
                latest_version = directory.version_set.filter(
                    start_date__lte=date).latest('start_date')
            else:
                latest_version = directory.version_set.latest('start_date')

            directory_data.append({
                "id": directory.id,
                "code": directory.code,
                "name": directory.name,
            })

        return Response({'refbooks': directory_data})


