from django.db import models
from django.contrib.auth.models import User

# class RecipesManager(models.Manager):
#     def get_queryset(self) -> models.QuerySet:
#         return super().get_queryset().fliter(is_deleted=False)

class Receipe(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    # CASCADE -delete all SET_NULL -put null in every receipe SET_DEFAULT-default value
    receipe_name=models.CharField(max_length=100)
    receipe_description=models.TextField()
    receipe_image=models.ImageField(upload_to="receipe")
    receipe_view_count=models.IntegerField(default=1)
    is_deleted=models.BooleanField(default=False)
    
    # objects=ReceipesManager()
    # admin_objects=models.manager()