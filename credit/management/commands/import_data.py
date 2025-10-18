
from django.core.management.base import BaseCommand
from credit.tasks import import_customer_data, import_loan_data

class Command(BaseCommand):
    help = "Import Excel data using Celery tasks"

    def handle(self, *args, **options):
        import_customer_data.delay('customer_data.xlsx')
        import_loan_data.delay('loan_data.xlsx')
        self.stdout.write(self.style.SUCCESS("Import tasks have been started!"))
