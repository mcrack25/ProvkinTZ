import datetime

from django.db import transaction
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet

from .filters import BillFilterSet
from .models import Bill, Client, Organization, Service
from .serializers import BillSerializer, UploadSerializer


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

    def upload_data(self, items):
        bills = []
        with transaction.atomic():
            for item in items:
                service, _ = Service.objects.get_or_create(name=item.get('service'))
                organization, _ = Organization.objects.get_or_create(name=item.get('client_org'))
                client, _ = Client.objects.get_or_create(name=item.get('client_name'))
                bills.append(
                    Bill(
                        client=client,
                        organization=organization,
                        service=service,
                        num=item.get('num'),
                        sum=item.get('sum'),
                        date=item.get('date'),
                    )
                )
            Bill.objects.bulk_create(bills, ignore_conflicts=True)

    def is_valid(self, line):
        try:
            fields = line.strip().split(",")
            int(fields[2].strip())
            float(fields[3].strip())
            datetime.datetime.strptime(fields[4].strip(), "%d.%m.%Y").date()
            return True
        except ValueError:
            return False

    def filter_data(self, lines):
        return [
            self.get_data(line.split(","))
            for line in lines[1:]
            if self.is_valid(line)
        ]

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        content_type = file_uploaded.content_type
        if content_type == 'text/csv':
            file_data = file_uploaded.file.read().decode("utf-8")
            lines = file_data.split("\n")
            data = self.filter_data(lines)
            self.upload_data(data)

        response = "POST API and you have uploaded a {} file".format(content_type)
        return Response(response)
