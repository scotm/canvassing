from django.db import models

from campaigns.models import Campaign
from core.models import Contact
from leafleting.models import CanvassRun, LeafletRun


class CanvassQuestion(models.Model):
    polling_question = models.CharField(max_length=200)
    ordering = models.IntegerField()
    type = models.CharField(max_length=20, choices=(
        ('True/False', 'binary'), ('Multiple-choice', 'choice'), ('Range', 'range'), ('Detailed Answer', 'answer')),
                            default='binary')

    def __unicode__(self):
        return self.polling_question


# Is it a multiple-choice question? If so, what choices do we have for this question?
class CanvassChoicesAvailable(models.Model):
    question = models.ForeignKey(CanvassQuestion)
    option = models.CharField(max_length=100)


class CanvassResponse(models.Model):
    contact = models.ForeignKey('core.Contact', null=True)
    question = models.ForeignKey(CanvassQuestion)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class CanvassChoice(CanvassResponse):
    choice = models.CharField(max_length=200)


class CanvassTrueFalse(CanvassResponse):
    choice = models.NullBooleanField()


class CanvassLongAnswer(CanvassResponse):
    answer = models.TextField()


class CanvassRange(CanvassResponse):
    answer = models.IntegerField()


class CanvassParty(CanvassResponse):
    answer = models.CharField(max_length=5, choices=(
    ('Scottish Socialist Party', 'SSP'), ('SNP', 'SNP'), ('Scottish Labour', 'SLAB'), ('Scottish Green', 'GRN'),
    ('Conservative', 'CON'), ('Liberal Democrat', 'LD'), ('Other', 'Other')))


class CanvassQuestionaire(models.Model):
    campaign = models.ForeignKey(Campaign)
    questions = models.ManyToManyField(CanvassQuestion)


class Conversation(models.Model):
    person = models.ForeignKey(Contact)
    notes = models.TextField()

