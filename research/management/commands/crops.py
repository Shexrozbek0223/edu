import pandas as pd

from django.core.management.base import BaseCommand
from django.utils import timezone

from research.models import Plants


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        # time = timezone.now().strftime('%X')
        # self.stdout.write("It's now %s" % time)

        col_names = ['name',]
        plants = pd.read_csv("static/crops.csv", sep=',',names=col_names, header=None)
        
        for index, plant in plants.iterrows():
            if plant.name == "name":
                continue
            print(plant.name)
            Plants.objects.get_or_create(
                name=plant.name,
            )