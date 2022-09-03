from django.views.generic import TemplateView
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer, BillSerializer
import datetime
from .models import Organization, Client, Service, Bill
from .filters import BillFilterSet


class BillViewSet(ReadOnlyModelViewSet):
    queryset = Bill.objects.all().order_by('id')
    serializer_class = BillSerializer
    filterset_class = BillFilterSet


class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def validate_data(self, data):
        if data.get('service') == '-':
            raise ValueError

    def get_data(self, fields):
        return {
            'client_name': fields[0].strip(),
            'client_org': fields[1].strip(),
            'num': int(fields[2].strip()),
            'sum': float(fields[3].strip()),
            'date': datetime.datetime.strptime(fields[4].strip(), "%d.%m.%Y").date(),
            'service': fields[5].strip(),
        }

    def upload_data(self, data):
        service, _ = Service.objects.get_or_create(name=data.get('service'))
        organization, _ = Organization.objects.get_or_create(name=data.get('client_org'))
        client, _ = Client.objects.get_or_create(name=data.get('client_name'))
        Bill.objects.get_or_create(
            client=client,
            organization=organization,
            service=service,
            num=data.get('num'),
            sum=data.get('sum'),
            date=data.get('date'),
        )

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        content_type = file_uploaded.content_type
        if content_type == 'text/csv':
            file_data = file_uploaded.file.read().decode("utf-8")
            lines = file_data.split("\n")
            for index, line in enumerate(lines):
                if index > 0:
                    try:
                        fields = line.split(",")
                        data = self.get_data(fields)
                        self.validate_data(fields)
                        self.upload_data(data)
                    except ValueError:
                        pass

        response = "POST API and you have uploaded a {} file".format(content_type)
        return Response(response)
