from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth import aauthenticate
from django.utils import timezone
from django.contrib.auth.models import Permission
# History
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

# from django.contrib.contenttypes.models import ContentType # Если нужно будет ссылаться на модели динамически


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']  # List of required fields besides USERNAME_FIELD

    def __str__(self):
        return self.first_name if self.first_name else self.email

    def _log_action(self, user_making_change, action_flag, message=""):
        """
        Вспомогательный метод для создания записи в LogEntry.
        :param user_making_change: Объект User, который вносит изменения.
        :param action_flag: ADDITION, CHANGE, или DELETION.
        :param message: Описание изменения (например, какие поля были изменены).
        """
        LogEntry.objects.log_action(
            user_id=user_making_change.pk,
            content_type_id=ContentType.objects.get_for_model(self).pk,
            object_id=self.pk,
            object_repr=str(self),  # Или более подробное представление объекта
            action_flag=action_flag,
            change_message=message
        )

    def save(self, *args, **kwargs):
        """
        Переопределенный метод save для логирования изменений.
        Ожидается, что 'user_making_change' будет передан в kwargs, если это не создание.
        """
        user_making_change = kwargs.pop('user_making_change', None)
        is_new = self._state.adding  # Проверяем, создается ли новый объект

        super().save(*args, **kwargs)  # Сначала сохраняем объект

        if user_making_change:
            action_flag = ADDITION if is_new else CHANGE
            # Для более детального сообщения можно сравнивать старые и новые значения полей,
            # но это усложнит логику. Пока оставим простое сообщение.
            change_message = "Объект создан программно." if is_new else "Объект изменен программно."
            if action_flag == CHANGE:
                # Здесь можно добавить логику для формирования более детального сообщения,
                # например, перечислить измененные поля.
                # Это потребует хранения состояния объекта до сохранения.
                pass
            self._log_action(user_making_change, action_flag, change_message)

    async def asave(self, *args, **kwargs):
        """
        Переопределенный асинхронный метод save для логирования изменений.
        Ожидается, что 'user_making_change' будет передан в kwargs, если это не создание.
        """
        user_making_change = kwargs.pop('user_making_change', None)
        is_new = self._state.adding

        # В Django 4.1+ super().asave() доступен.
        # Для более старых версий Django асинхронный save нужно реализовывать через sync_to_async.
        # Будем считать, что у вас Django >= 4.1
        if hasattr(super(), 'asave'):
            await super().asave(*args, **kwargs)
        else:
            # Для Django < 4.1 (примерная реализация)
            from django.db import router
            from django.utils.asyncio import async_unsafe
            db = router.db_for_write(self.__class__, instance=self)
            await async_unsafe(self.save_base)(using=db, force_insert=is_new, force_update=not is_new)


        if user_making_change:
            action_flag = ADDITION if is_new else CHANGE
            change_message = "Объект создан программно (async)." if is_new else "Объект изменен программно (async)."
            # Асинхронное создание LogEntry
            # Используем sync_to_async, так как LogEntry.objects.log_action синхронный
            from django.utils.asyncio import sync_to_async
            log_action_async = sync_to_async(self._log_action, thread_sensitive=True)
            await log_action_async(user_making_change, action_flag, change_message)

    # Метод delete также можно переопределить для логирования DELETION
    def delete(self, *args, **kwargs):
        user_making_change = kwargs.pop('user_making_change', None)
        # Сохраняем pk и repr до удаления, так как после удаления они могут быть недоступны
        obj_pk = self.pk
        obj_repr = str(self)
        content_type_id = ContentType.objects.get_for_model(self).pk

        result = super().delete(*args, **kwargs)

        if user_making_change:
            LogEntry.objects.log_action(
                user_id=user_making_change.pk,
                content_type_id=content_type_id,
                object_id=obj_pk, # Используем сохраненный pk
                object_repr=obj_repr, # Используем сохраненное представление
                action_flag=DELETION,
                change_message="Объект удален программно."
            )
        return result

    async def adelete(self, *args, **kwargs):
        user_making_change = kwargs.pop('user_making_change', None)
        obj_pk = self.pk
        obj_repr = str(self)
        content_type_id = ContentType.objects.get_for_model(self).pk

        if hasattr(super(), 'adelete'):
            result = await super().adelete(*args, **kwargs)
        else:
            from django.utils.asyncio import async_unsafe
            result = await async_unsafe(self.delete)(*args, **kwargs) # Вызываем синхронный delete, если adelete нет

        if user_making_change:
            from django.utils.asyncio import sync_to_async
            # Адаптируем _log_action для асинхронного вызова или создаем отдельный async_log_action
            # Для простоты, предположим, что LogEntry.objects.log_action можно вызвать через sync_to_async
            log_action_func = sync_to_async(LogEntry.objects.log_action, thread_sensitive=True)
            await log_action_func(
                user_id=user_making_change.pk,
                content_type_id=content_type_id,
                object_id=obj_pk,
                object_repr=obj_repr,
                action_flag=DELETION,
                change_message="Объект удален программно (async)."
            )
        return result


    @classmethod
    async def authenticate(cls, username, password):
        user = await aauthenticate(username=username, password=password)
        if user:
            return user
        # TODO Check broot force Attack..
        return None


    # Переопределяем get_user_permissions и get_group_permissions,
    # чтобы они учитывали разрешения из наших ролей
    def get_user_permissions(self, obj=None):
        # Сначала получаем стандартные разрешения пользователя
        user_permissions = super().get_user_permissions(obj)
        # Можно расширить ...
        # Проверить создателя объекта и решить можно или нет...
        return user_permissions.union(user_permissions)

    def get_group_permissions(self, obj=None): #
        # Если вы не используете стандартные группы Django, можно оставить как есть
        # или также агрегировать разрешения из ролей, если это имеет смысл в вашей логике
        return super().get_group_permissions(obj)

    def has_perm(self, perm, obj=None): #TODO async
        """
        Проверяет, имеет ли пользователь указанное разрешение.
        perm должен быть в формате "app_label.codename".
        """
        # Сначала проверяем стандартные разрешения пользователя (включая is_superuser)
        if self.is_active and self.is_superuser:
            return True
        if super().has_perm(perm, obj):
            return True
        # Похоже разрешений не нашлось... лесом...
        return False

class Sessions(models.Model):
    sid = models.CharField(primary_key=True, max_length=12, editable=False, verbose_name="Session ID")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sessions')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created at")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="Closed at")
    active = models.BooleanField(default=True, verbose_name="Active")
    ws_connect_cnt = models.IntegerField(default=0, verbose_name="WS Connect Count")

    def __str__(self):
        return f'{self.sid} - {self.user}'

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"
        indexes = [
            models.Index(fields=['sid', 'user', 'active'])
        ]