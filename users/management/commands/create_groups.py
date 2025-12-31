from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from lms.models import Course, Lesson


class Command(BaseCommand):
    help = 'Создает группы модераторов'

    def handle(self, *args, **options):
        moder_group, created = Group.objects.get_or_create(name='Модераторы')

        # Добавляем права просмотра и изменения
        content_types = {
            Course: ['view', 'change'],
            Lesson: ['view', 'change']
        }

        for model, perms in content_types.items():
            content_type = ContentType.objects.get_for_model(model)
            for perm in perms:
                codename = f'{perm}_{model._meta.model_name}'
                try:
                    permission = Permission.objects.get(
                        content_type=content_type,
                        codename=codename
                    )
                    moder_group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'Permission {codename} not found')
                    )

        self.stdout.write(
            self.style.SUCCESS('Группа модераторов создана и настроена')
        )