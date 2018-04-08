from django.contrib.auth.models import User

# Create your models here.
from django.db import models

class GameSession(models.Model):
    name=models.CharField(max_length=30)
    letter=models.CharField(max_length=30)
    used_letter=models.CharField(max_length=30)
    author=models.OneToOneField(User, on_delete=models.CASCADE, )


    def __str__(self):
        return self.name


class UserProfile(models.Model):
    session=models.ForeignKey(GameSession, on_delete=models.CASCADE,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.CharField(max_length=30)
    wins= models.CharField(max_length=30)

    def __str__(self):
        return self.user.username

class UserMethods(User):

    def no_game(self):
        profile = UserProfile.objects.get(user=self)
        if profile.session==None:
            return True
        else:
            return False
    class Meta:
        proxy = True
