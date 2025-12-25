# 使用Django默认User模型
# 可以在后续需要时通过OneToOneField扩展用户模型

from django.db import models
from django.conf import settings

# 示例：用户资料扩展模型（可选）
# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
#     bio = models.TextField('个人简介', max_length=500, blank=True)
#     created = models.DateTimeField('创建时间', auto_now_add=True)
#
#     class Meta:
#         verbose_name = '用户资料'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.user.username