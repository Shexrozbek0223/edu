from decimal import Decimal

from django.core.management import BaseCommand
from django.utils import timezone
import pandas as pd

from research.models import Countries


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        col_names = ('pk', 'name_ru')
        country = pd.read_csv("static/country.csv", sep=";", names=col_names, header=None)
        for index, country in country.iterrows():
            Countries.objects.create(
                pk=country.pk,
                name_ru=country.name_ru,
            )
