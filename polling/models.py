from django.db import models
from sortedm2m.fields import SortedManyToManyField
from memoize import memoize

from campaigns.models import Campaign
from core.models import Contact


class CanvassQuestion(models.Model):
    short_name = models.CharField(max_length=255)
    polling_question = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=(
        ('True/False', 'binary'), ('Multiple-choice', 'choice'), ('Range', 'range'), ('Detailed Answer', 'answer')),
                            default='binary')

    def __unicode__(self):
        return self.polling_question

    @memoize(timeout=10)
    def choices(self):
        if self.type == 'Multiple-choice':
            return ", ".join(x.option for x in self.canvasschoicesavailable_set.all())

    @memoize(timeout=10)
    def choices_objects(self):
        return [x for x in self.canvasschoicesavailable_set.all()]


# Is it a multiple-choice question? If so, what choices do we have for this question?
class CanvassChoicesAvailable(models.Model):
    question = models.ForeignKey(CanvassQuestion)
    option = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s -> %s" % (unicode(self.question), unicode(self.option))


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
    questions = SortedManyToManyField(CanvassQuestion)

    def __unicode__(self):
        return ", ".join(unicode(x.short_name) for x in self.questions.all())


class Conversation(models.Model):
    person = models.ForeignKey(Contact)
    notes = models.TextField()
