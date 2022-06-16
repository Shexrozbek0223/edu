
import pandas as pd

from django.core.management.base import BaseCommand
from django.utils import timezone

from research.models import Months


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        # time = timezone.now().strftime('%X')
        # self.stdout.write("It's now %s" % time)

        col_names = ['id', 'ismi']
        monthss = pd.read_csv("static/months.csv", sep=',',names=col_names, header=None)
        
        for index, months in monthss.iterrows():
            if months.ismi == "name":
                continue
            Months.objects.get_or_create(
                pk=months.id,
                month=months.ismi,
            )
            