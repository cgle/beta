from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50,default='')
    age = models.IntegerField(null=True)
    university = models.CharField(max_length=100,default='')
    home_city = models.CharField(max_length=50,default='')
    away_city = models.CharField(max_length=50,default='')
    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

class KoinboxUser(models.Model):
    user = models.ForeignKey(User)
    koinbox_username = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    def __str__(self):
        return self.koinbox_username

class Friends(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField(max_length=50)
    friend_username = models.CharField(max_length=50)
    def __str__(self):
        return self.friend_username

class Interest(models.Model):
    user = models.ForeignKey(User)
    type_interest = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return '%s,%s, %s' %(user.username, type_interest, description)

class Interest_Tag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    interests = models.ManyToManyField(Interest)
    def __str__(self):
        return self.name

class Friendship(models.Model):
    from_friend = models.ForeignKey(
        User, related_name='friend_set'
    )
    to_friend = models.ForeignKey(
        User, related_name='to_friend_set'
    )
    def __str__(self):
        return '%s, %s' % (
            self.from_friend.username,
            self.to_friend.username
        )
    class Admin:
        pass
    class Meta:
        unique_together = (('to_friend', 'from_friend'), )