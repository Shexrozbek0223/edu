from decimal import Decimal

from django.core.management import BaseCommand
from django.utils import timezone
import pandas as pd

from research.models import ProductTypes


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        col_names = ('pk', 'crops',)
        typess = pd.read_csv("static/productTypes.csv", sep=",", names=col_names, header=None)
        for index, types in typess.iterrows():
            print(types.crops)
            if types.pk == "pk":
                continue
            ProductTypes.objects.get_or_create(
                pk=types.pk,
                product=types.crops,
            )
