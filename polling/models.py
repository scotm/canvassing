from django.contrib.gis.db import models
from django.db import models

from campaigns.models import Campaign
from core.models import Contact


class CanvassQuestion(models.Model):
    polling_question = models.CharField(max_length=200)
    ordering = models.IntegerField()
    type = models.CharField(max_length=20, choices=(
    ('True/False', 'binary'), ('Multiple-choice', 'choice'), ('Detailed Answer', 'answer')), default='binary')


# Is it a multiple-choice question? If so, what choices do we have for this question?
class CanvassChoicesAvailable(models.Model):
    question = models.ForeignKey(CanvassQuestion)
    option = models.CharField(max_length=100)


class CanvassResponse(models.Model):
    contact = models.ForeignKey('core.Contact', null=True)
    question = models.ForeignKey(CanvassQuestion)

    class Meta:
        abstract = True


class CanvassChoice(CanvassResponse):
    choice = models.CharField(max_length=200)


class CanvassTrueFalse(CanvassResponse):
    choice = models.NullBooleanField()


class CanvassLongAnswer(CanvassResponse):
    answer = models.TextField()


class CanvassQuestionaire(models.Model):
    campaign = models.ForeignKey(Campaign)
    questions = models.ManyToManyField(CanvassQuestion)


class Conversation(models.Model):
    person = models.ForeignKey(Contact)
    notes = models.TextField()