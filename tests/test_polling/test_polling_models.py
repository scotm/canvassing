from tests.factories import CanvassQuestionFactory, CanvassChoicesAvailableFactory, CanvassQuestionaireFactory
from tests.testcase import LazyTestCase


class ModelsTest(LazyTestCase):
    def load_data(self):
        self.question = CanvassQuestionFactory(short_name='Holyrood 2016',
                                               polling_question='Which party will you vote for on the list in 2016?',
                                               type='Multiple-choice')

    def test_question(self):
        self.assertEqual(unicode(self.question), 'Which party will you vote for on the list in 2016?')

    def test_multiple_choice(self):
        objects = CanvassChoicesAvailableFactory.create_batch(3, question=self.question)
        self.assertEqual(self.question.choices(), 'Answer 0, Answer 1, Answer 2')
        compare = self.question.choices_objects()
        for i in objects:
            self.assertIn(i, compare)
        self.assertEqual(unicode(objects[0]), 'Which party will you vote for on the list in 2016? -> Answer 0')

    def test_questionaire(self):
        questions = CanvassQuestionFactory.create_batch(3)
        questionaire = CanvassQuestionaireFactory(questions=questions)
        self.assertEqual(unicode(questionaire), "Independence, Heard of Org, West Lothian Hospital")
