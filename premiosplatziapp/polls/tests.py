import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice

def create_question_with_special_time(question_text, pub_date):
    """
    Create a question with the given "question_text", and a "pub_date"
    """
    question = Question(question_text=question_text, pub_date=pub_date)
    choice1 = Choice(question=question, choice_text="Choice 1", votes=0)
    choice2 = Choice(question=question, choice_text="Choice 2", votes=0)
    question.save(choices=(choice1, choice2))
    return question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """
        Allows 'was_published_recently' to return False when a question has 
        a pub_date from the future.
        """
        # Creating a future question.
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = create_question_with_special_time(
            question_text="Who is the best Course Director of Platzi?", 
            pub_date=time
            )
        # Asserting that no, it was not published recently.
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_past_questions(self):
        """
        Allows 'was_published_recently' to return False when a question has 
        a pub_date from the past.
        """
        # Creating a past question.
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = create_question_with_special_time(
            question_text="Who is the best Course Director of Platzi?", 
            pub_date=time
            )
        # Asserting that no, it was not published recently.
        self.assertIs(past_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_questions(self):
        """
        Allows 'was_published_recently' to return True when a question has a 
        pub_date from today.
        """
        # Creating a recent question.
        time = timezone.now() - datetime.timedelta(seconds=100)
        recent_question = create_question_with_special_time(
            question_text="Who is the best Course Director of Platzi?", 
            pub_date=time
            )
        # Asserting that yes, it was published recently.
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given "question_text", and a "pub_date" 
    that equals the given number of days, minus the current date.

    Note: The number of days should be negative for past questions, 
    and positive for future questions.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question(question_text=question_text, pub_date=time)
    choice1 = Choice(question=question, choice_text="Choice 1", votes=0)
    choice2 = Choice(question=question, choice_text="Choice 2", votes=0)
    question.save(choices=(choice1, choice2))
    return question


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropiate message should be displayed.
        """
        # Sending http GET request to the index.html page.
        response = self.client.get(reverse("polls:index"))
        # Asserting that the status code of the response equals to 200.
        self.assertEqual(response.status_code, 200)
        # Asserting that the response has a message equal to
        # "No polls are available."
        self.assertContains(response, "No polls are available.")
        # Asserting that "latest_questions_list" equals to an empty list.
        self.assertQuerysetEqual(response.context["latest_questions_list"], [])

    def test_future_questions(self):
        """
        Questions with a pub_date in the future, should not be displayed
        on the index page.
        """
        # Creating a future question.
        create_question(question_text="Future Question", days=30)
        # Sending http GET request to the index.html page.
        response = self.client.get(reverse("polls:index"))
        # Asserting that the status code of the response equals to 200.
        self.assertEqual(response.status_code, 200)
        # Asserting that the response has a message equal to
        # "No polls are available."
        self.assertContains(response, "No polls are available.")
        # Asserting that "latest_questions_list" equals to an empty list.
        self.assertQuerysetEqual(response.context["latest_questions_list"], [])

    def test_past_questions(self):
        """
        Questions with a pub_date in the past, have to be displayed
        on the index page.
        """
        # Creating a past question.
        past_question = create_question(question_text="Past Question", days=-30)
        # Sending http GET request to the index.html page.
        response = self.client.get(reverse("polls:index"))
        # Asserting that the status code of the response equals to 200.
        self.assertEqual(response.status_code, 200)
        # Asserting that the response has a message equal to
        # the question_text of past_question.
        self.assertContains(response, past_question.question_text)
        # Asserting that "latest_questions_list" equals to a list 
        # containing 'past_question' only.
        self.assertQuerysetEqual(response.context["latest_questions_list"], [past_question])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions are displayed.
        """
        # Creating 1 past question and 1 future question.
        past_question = create_question(question_text="Past Question", days=-30)
        future_question = create_question(question_text="Future Question", days=30)
        # Sending http GET request to the index.html page.
        response = self.client.get(reverse("polls:index"))
        # Asserting that the response has a message equal to
        # the question_text of past_question.
        self.assertContains(response, past_question.question_text)
        # Asserting that "latest_questions_list" equals to a list 
        # containing 'past_question' only.
        self.assertQuerysetEqual(response.context["latest_questions_list"], [past_question])

    def test_two_past_questions(self):
        """
        The index page can display multiple questions.
        """
        # Creating 2 past questions.
        past_question1 = create_question(question_text="Past Question 1", days=-30)
        past_question2 = create_question(question_text="Past Question 2", days=-30)
        # Sending http GET requst to the index.html page.
        response = self.client.get(reverse("polls:index"))
        # Asserting that "latest_questions_list" contains
        # 'past_question1" and "past_question2."
        self.assertQuerysetEqual(response.context["latest_questions_list"], [past_question1, past_question2])

    def test_two_future_questions(self):
        """
        The index page should not display any past questions.
        """
        # Creating 2 future questions.
        future_question1 = create_question(question_text="Future Question 1", days=30)
        future_question2 = create_question(question_text="Future Question 2", days=30)
        # Sending http GET requst to the index.html page.
        response = self.client.get(reverse("polls:index"))
        # Asserting that the response has a message equal to
        # "No polls are available."
        self.assertContains(response, "No polls are available.")
        # Asserting that "latest_questions_list" equals to an empty list.
        self.assertQuerysetEqual(response.context["latest_questions_list"], [])


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a pub_date from the future 
        returns a 404 error not found.
        """
        # Creating a future question.
        future_question = create_question(question_text="Future Question", days=30)
        # Make sure to add the comma at the end of the touple; otherwise, pyhton 
        # will not read it as a tuple, giving you undesired results.
        url = reverse("polls:detail", args=(future_question.id,))
        # Sending http GET requst to the detail.html page.
        response = self.client.get(url)
        # Asserting that the status code of the response equals to 404.
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date from the past 
        displays the question's text.
        """
        # Creating a past question.
        past_question = create_question(question_text="Past Question", days=-30)
        # Sending http GET requst to the detail.html page.
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        # Asserting that the status code of the response equals to 200.
        self.assertEqual(response.status_code, 200)
        # Asserting that the response has a message equal to
        # the question_text of past_question.
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):

    def test_text_of_past_questions(self):
        """
        If there is a past question, the results view should display the 
        the text of the past question.
        """
        # Creating a past question and 2 choices for the valid question.
        past_question = create_question(question_text="Past Question", days=-30)
        choice1 = past_question.choice_set.get(pk=1)
        choice2 = past_question.choice_set.get(pk=2)
        # Sending http GET request to the results.html page
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        # Asserting that the status code of the response equals to 200.
        self.assertEqual(response.status_code, 200)
        # Asserting that the past questions' text is displayed.
        self.assertContains(response, past_question.question_text)

    def test_votes_for_past_questions(self):
        """
        If there is a past question, the results view should display the 
        number of votes for each choice belonging to that question.
        """
        # Creating a past question and 2 choices for the valid question.
        past_question = create_question(question_text="Past Question", days=-30)
        choice1 = past_question.choice_set.get(pk=1)
        choice2 = past_question.choice_set.get(pk=2)
        # Sending http GET request to the results.html page
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        # Asserting that the past questions' choices and 
        # their respective votes are being displayed.
        self.assertContains(response, f'{choice1.choice_text} -- {choice1.votes} vote')
        self.assertContains(response, f'{choice2.choice_text} -- {choice2.votes} votes')
        # Asserting that the "You didn't pick a choice" message is not displayed.
        self.assertNotContains(response, "You didn't pick a choice")

    def test_votes_for_future_questions(self):
        """
        If there is a future question, display an 404 error message.
        """
        # Creating a future question and 2 choices for the future question.
        future_question = create_question(question_text="Future Question", days=30)
        choice1 = future_question.choice_set.get(pk=1)
        choice2 = future_question.choice_set.get(pk=2)
        # Sending http GET request to the results.html page
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        # Asserting that the status code of the response equals to 404.
        self.assertEqual(response.status_code, 404)

    def test_question_does_not_exist(self):
        """ 
        If there is a no question, display an 404 error message.
        """
        # Sending http GET request to the results.html page
        url = reverse("polls:results", kwargs={'pk':1})
        response = self.client.get(url)
        # Asserting that the status code of the response equals to 404.
        self.assertEqual(response.status_code, 404)        


class ChoiceModelTests(TestCase):

    def test_question_with_no_choices(self):
        """
        Questions created with no choices will raise an error.
        """
        # Creating a future question.
        question = create_question(question_text="Question with no choices", days=-30)
        # Asserting that saving the qestion raises a ValueError.
        with self.assertRaises(ValueError): question.save()


        