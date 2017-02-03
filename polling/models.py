from django.db import models
from memoize import memoize
from sortedm2m.fields import SortedManyToManyField

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
            return ", ".join(x.option for x in self.choices_objects())

    @memoize(timeout=10)
    def choices_objects(self):
        return CanvassChoicesAvailable.objects.filter(question=self)


# Is it a multiple-choice question? If so, what choices do we have for this question?
class CanvassChoicesAvailable(models.Model):
    question = models.ForeignKey(CanvassQuestion)
    option = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s -> %s" % (unicode(self.question), unicode(self.option))


class CanvassResponseException(Exception):
    pass


class CanvassResponse(models.Model):
    contact = models.ForeignKey('core.Contact', null=True)
    question = models.ForeignKey(CanvassQuestion)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-date_added',)

    def store_response(self, *args, **kwargs):
        raise CanvassResponseException("Cannot call store_response on a CanvassResponse object directly")


# A choice made from the question's response set
class CanvassChoice(CanvassResponse):
    choice = models.CharField(max_length=200)

    @classmethod
    def store_response(cls, contact, question, answer):
        possible_answers = set(x.option for x in question.choices_objects())
        if answer not in possible_answers:
            raise CanvassResponseException('Answer for %s: %s is not in the list of possible choices (%s)' %
                                           (contact, question, question.choices()))
        cls.objects.create(contact=contact, question=question, choice=answer)


# Binary response
class CanvassTrueFalse(CanvassResponse):
    choice = models.NullBooleanField()

    @classmethod
    def store_response(cls, contact, question, answer):
        if answer not in ['True', 'False']:
            raise CanvassResponseException('Answer is neither "True", nor "False"')
        answer = True if answer == 'True' else False
        cls.objects.create(contact=contact, question=question, choice=answer)


class CanvassLongAnswer(CanvassResponse):
    answer = models.TextField()

    @classmethod
    def store_response(cls, contact, question, answer):
        cls.objects.create(contact=contact, question=question, choice=answer)


# Scale of 1-10
class CanvassRange(CanvassResponse):
    answer = models.IntegerField()

    @classmethod
    def store_response(cls, contact, question, answer):
        answer = int(answer)
        if not 1 <= answer <= 10:
            raise CanvassResponseException('Answer for %s is not between 1 and 10' % question)
        cls.objects.create(contact=contact, question=question, choice=answer)


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
