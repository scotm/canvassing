from django.contrib.gis.db import models
from django.db import models

# Create your models here.
from campaigns.models import Campaign


class CanvassQuestionaire(models.Model):
    campaign = models.ForeignKey(Campaign)


class CanvassQuestion(models.Model):
    polling_question = models.CharField(max_length=200)
    ordering = models.IntegerField()


class CanvassChoice(models.Model):
    question = models.ForeignKey(CanvassQuestion)
    choice = models.CharField(max_length=200)


class CanvassLongAnswer(models.Model):
    question = models.ForeignKey(CanvassQuestion)
    answer = models.TextField()