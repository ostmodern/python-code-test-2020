from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Initial users'

    def handle(self, *args, **options):
        user_model = get_user_model()
        if user_model.objects.filter(username='admin').first():
            return
        print('loading initial data')
        admin = user_model.objects.create_superuser('admin', 'admin@some.random.domainfffm', 'admin')
        # system wallet which receives all transfers fees

        for user in ('user1', 'user2', 'user3'):
            u = user_model.objects.create_user(username=user,
                                               email=f'{user}@some.random.domainfffm',
                                               password='random pass for !')
        print('loaded')
