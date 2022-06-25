import pandas as pd

from django.core.management.base import BaseCommand
from django.utils import timezone

from users.models import UserInfo


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        # time = timezone.now().strftime('%X')
        # self.stdout.write("It's now %s" % time)

        col_names = ('id', 'section', 'position', 'full_name', 'date_of_birthday', 'gender', 'degree','inps_number', 'phone_number','user_role')
        users = pd.read_csv("static/users.csv", sep=",", names=col_names, header=None)
        for index, user in users.iterrows():
            if user.id == "id":
                continue
            
            new_user = UserInfo(
                section=user.section,
                position=user.position,
                full_name=user.full_name,
                date_of_birthday=user.date_of_birthday,
                gender=user.gender,
                degree=user.degree,
                user_role = int(user.user_role),
                inps_number=user.inps_number,
                phone_number=user.phone_number,
                username=f'u{str(user.inps_number)}'
            )
            if UserInfo.objects.filter(username=f'u{str(user.inps_number)}').exists() or UserInfo.objects.filter(
                    phone_number=user.phone_number).exists():
                continue
            new_user.set_password(str(user.inps_number))
            new_user.save()
            print('Finish')
            # print(f'User {user.full_name_latin} has been created successfully')
            # print(user.full_name)
