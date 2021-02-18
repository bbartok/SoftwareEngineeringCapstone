import json

from rest_framework.test import RequestsClient
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import *
from .serializers import *


# initialize the APIClient app
client = Client()


class GetUsersTest(TestCase):
    """
    This test case checks that we can correctly return the users
    """

    def setUp(self):
        """
        This is the setup method for tests, it creates all the objects we need
        """
        Users.objects.create(
            email='bbartok@ualberta.ca', username='bartok',
            password='blahblah', salt='salty')
        Users.objects.create(
            email='kbartok@ualberta.ca', username='kbartok',
            password='blahblah', salt='salty')
        Users.objects.create(
            email='abartok@ualberta.ca', username='abartok',
            password='blahblah', salt='salty')

    def test_get_all_users(self):
        response = client.get(reverse('get_post_users'))
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewUserTest(TestCase):
    """
    This test case checks that a user is created properly
    """

    def setUp(self):

        self.valid_payload = {
            'email': 'bbartok@ualberta.ca',
            'username': 'bartok',
            'password': 'blahblah',
            'salt': 'salty'
        }
        self.invalid_payload_1 = {
            'email': '',
            'username': 'bartok',
            'password': 'blahblah',
            'salt': 'salty'
        }
        self.invalid_payload_2 = {
            'email': 'bbartok@ualberta.ca',
            'username': '',
            'password': 'blahblah',
            'salt': 'salty'
        }

    def test_create_valid_users(self):
        """
        Test to see if a valid user is created properly
        """
        response = client.post(
            reverse('get_post_users'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_users(self):
        """
        Test to see if an invalid user is not created
        """
        response = client.post(
            reverse('get_post_users'),
            data=json.dumps(self.invalid_payload_1),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_users_2(self):
        """
        Test to see if an invalid user is not created
        """
        response = client.post(
            reverse('get_post_users'),
            data=json.dumps(self.invalid_payload_2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetAllTopicsTest(TestCase):
    """
    This test is to see if we can correctly get all the topics.
    """

    def setUp(self):
        user1 = Users.objects.create(
            email='tbartok@ualberta.ca', username='tbartok',
            password='blahblah', salt='salty')
        user2 = Users.objects.create(
            email='abartok@ualberta.ca', username='abartok',
            password='blahblah', salt='salty')
        user3 = Users.objects.create(
            email='bbartok@ualberta.ca', username='bartok',
            password='blahblah', salt='salty')
        # user1 = UsersSerializer(instance=user1)
        # user2 = UsersSerializer(instance=user2)
        # user3 = UsersSerializer(instance=user3)

        Topics.objects.create(
            name="Topic A", creator_id=user1, tags=["sample_tag"],
            learningoutcomes=["LO 1", "LO 2"])
        Topics.objects.create(
            name="Topic B", creator_id=user2, tags=["sample_tag"],
            learningoutcomes=["LO 1", "LO 2"])
        Topics.objects.create(
            name="Topic C", creator_id=user3, tags=["sample_tag"],
            learningoutcomes=["LO 1", "LO 2"])

    def test_get_all_topics(self):
        # Get API Response
        response = client.get(reverse('get_post_topics'))
        # Get data from DB
        topics = Topics.objects.all()
        serializer = TopicsSerializer(topics, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewTopicTest(TestCase):
    """ Test Module for Inserting a new Topic """

    def setUp(self):

        user1 = Users.objects.create(
            email='bbartok@ulaberta.ca', username='bartok',
            password='blahblah', salt='salty')
        '''self.user = Topics.objects.create(
            name = 'Topic A',
            creator_id = user1,
            tags = ["sample_tag"],
            learningoutcomes=["LO 1", "LO 2"]
        )'''
        self.valid_payload = {
            'name': 'Topic A',
            'creator_id': 'bartok',
            'tags': ["sample_tag"],
            'learningoutcomes': ["LO 1", "LO 2"]
        }
        self.invalid_payload_1 = {
            'name': '',

            'creator_id': 'bartok',

            'tags': ["sample_tag"],
            'learningoutcomes': ["LO 1", "LO 2"]
        }
        self.invalid_payload_2 = {
            'name': 'Topic A',
            'creator_id': '',
            'tags': ["sample_tag"],
            'learningoutcomes': ["LO 1", "LO 2"]
        }
        self.invalid_payload_3 = {
            'name': 'Topic A',

            'creator_id': 'bartok',

            'tags': '',
            'learningoutcomes': ["LO 1", "LO 2"]
        }
        self.invalid_payload_4 = {
            'name': 'Topic A',

            'creator_id': 'bartok',

            'tags': ["sample_tag"],
            'learningoutcomes': ''
        }

    def test_create_valid_topic(self):
        response = client.post(
            reverse('get_post_topics'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_topic_1(self):
        response = client.post(
            reverse('get_post_topics'),
            data=json.dumps(self.invalid_payload_1),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_topic_2(self):
        response = client.post(
            reverse('get_post_topics'),
            data=json.dumps(self.invalid_payload_2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_topic_3(self):
        response = client.post(
            reverse('get_post_topics'),
            data=json.dumps(self.invalid_payload_3),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_topic_4(self):
        response = client.post(
            reverse('get_post_topics'),
            data=json.dumps(self.invalid_payload_4),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateTopicTest(TestCase):
    """ Test Module for Updating a Topic """

    def setUp(self):
        user1 = Users.objects.create(
            email='bbartok@ualberta.ca', username='bartok',
            password='blahblah', salt='salty')
        # user1 = Users.objects.get(username='bartok').username
        # user1 = UsersSerializer(instance=user1)
        '''self.user = Users.objects.create(
            email = 'bbartok@ualberta.ca'
            username = 'bartok',
            password = 'blahblah'
            salt = 'salty'
        )'''
        self.user = Topics.objects.create(
            name="Topic Test",
            creator_id=user1,
            learningoutcomes=['LO 1'],
            tags=["Test Tag"]
        )
        self.valid_payload = {
            "name": "Topic Test",
            "creator_id": 'bartok',
            "learningoutcomes": ["LO 1", "LO 2"],
            "tags": ["Test Tag", "Test Tag 2"]
        }
        self.invalid_payload = {
            "name": "Topic Test",
            "creator_id": '',
            "learningoutcomes": ["LO 1"],
            "tags": ["Test Tag"]
        }

    def test_update_valid_topic(self):
        response = client.put(
            reverse('get_delete_update_topics', kwargs={
                    'name': getattr(self.user, 'name')}),
            data=self.valid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_topic(self):
        response = client.put(
            reverse('get_delete_update_topics', kwargs={
                'name': getattr(self.user, 'name')}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteTopicTest(TestCase):
    """ Test Module for Deleting a Topic """

    def setUp(self):
        user1 = Users.objects.create(
            email='bbartok@ualberta.ca', username='bartok',
            password='blahblah', salt='salty')
        # user1 = UsersSerializer(instance=user1)
        self.user = Topics.objects.create(
            name="Topic Test",
            creator_id=user1,
            learningoutcomes=["LO 1"],
            tags=["Test Tag"]
        )

    def test_delete_valid_topic(self):
        response = client.delete(
            reverse('get_delete_update_topics', kwargs={
                    'name': getattr(self.user, 'name')}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_topic(self):
        response = client.delete(
            reverse('get_delete_update_topics', kwargs={
                    'name': 'wrong name'}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetQuestionTest(TestCase):
    """ Test Module for Getting the user's questions """

    def setUp(self):

        user1 = Users.objects.create(
            email='bbartok@ualberta.ca', username='bbartok',
            password='blahblah', salt='salty')
        user2 = Users.objects.create(
            email='notme@ualberta.ca', username='notme',
            password='blahblah', salt='salty1')
        topicA = Topics.objects.create(
            name='Containerization', creator_id=user1,
            learningoutcomes=["LO 1"], tags=["some"])
        topicB = Topics.objects.create(
            name='UML', creator_id=user1,
            learningoutcomes=["LO 1"], tags=["other"])

        self.user_1 = Questions.objects.create(
            _id="someID1",
            prompt="This is a test question A.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="multipleChoice",

            topic=topicA,
            username=user1,
            learningoutcome=["LO 1"],
            feedback=["Feedback A", "Feedback B",
                      "Feedback C", "Feedback D"],
            hidden = False,
            draft= False

        )
        self.user_1 = Questions.objects.create(
            _id="someID2",
            prompt="This is a test question B.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="multipleChoice",

            topic=topicA,
            username=user1,
            learningoutcome=["LO 1"],
            feedback=["Feedback A", "Feedback B",
                      "Feedback C", "Feedback D"],
            hidden = False,
            draft= False

        )
        self.not_user_1 = Questions.objects.create(
            _id="someID3",
            prompt="This is a test question C.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="multipleChoice",

            topic=topicB,
            username=user2,
            learningoutcome=["LO 1"],
            feedback=["Feedback A", "Feedback B",
                      "Feedback C", "Feedback D"],
            hidden = False,
            draft= False

        )
        self.not_user_2 = Questions.objects.create(
            _id="someID4",
            prompt="This is a test question D.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="multipleChoice",

            topic=topicB,
            username=user2,
            learningoutcome=["LO 1"],
            feedback=["Feedback A", "Feedback B",
                      "Feedback C", "Feedback D"],
            hidden = False,
            draft= False

        )

    def test_get_all_questions(self):
        # Get API Response
        response = client.get(reverse('get_post_question'))
        # Get data from DB
        topics = Questions.objects.all()
        serializer = QuestionSerializer(topics, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_questions(self):
        # Get API Response
        response = client.get(
            reverse('get_post_question'),
            {'username': getattr(self.user_1, 'username'), 'self': 'true'})
        # Get data from DB
        topics = Questions.objects.filter(username="test user")
        serializer = QuestionSerializer(topics, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_users_questions(self):
        # Get API Response
        response = client.get(reverse('get_post_question'), {
                              'username': getattr(self.user_1, 'username')})
        # Get data from DB
        topics = Questions.objects.exclude(username="test user")
        serializer = QuestionSerializer(topics, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewQuestionTest(TestCase):
    """ Test Module for Creating a Question """

    def setUp(self):

        user1 = Users.objects.create(
            email='kbartok@ualberta.ca', username='kbartok',
            password='blahblah', salt='salty')
        topicA = Topics.objects.create(
            name='Containerization', creator_id=user1,
            learningoutcomes=["LO 1"], tags=["some"])
        # user1 = UsersSerializer(instance=user1)
        # topicA = TopicsSerializer(instance=topicA)
        self.valid_payload = {
            "_id": "someID1",
            "prompt": "This is a test question A.",
            "shuffleoption": False,
            "choices": ["A", "B", "C", "D"],
            "choiceanswers": [True, False, False, False],
            "typename": "multipleChoice",
            "topic": 'Containerization',
            "username": 'kbartok',
            "learningoutcome": ["LO 1"],
            "feedback": ["Feedback A", "Feedback B",
                         "Feedback C", "Feedback D"],
            "draft": False,
            "hidden": False

        }
        self.invalid_payload_1 = {
            "_id": '',
            "prompt": "This is a test question A.",
            "shuffleoption": False,
            "choices": ["A", "B", "C", "D"],
            "choiceanswers": [True, False, False, False],
            "typename": "multipleChoice",

            "topic": 'Containerization',
            "username": 'kbartok',
            "learningoutcome": ["LO 1"],
            "feedback": ["Feedback A", "Feedback B",
                         "Feedback C", "Feedback D"],
            "draft": False,
            "hidden": False

        }
        self.invalid_payload_2 = {
            "_id": "someID1",
            "prompt": '',
            "shuffleoption": False,
            "choices": ["A", "B", "C", "D"],
            "choiceanswers": [True, False, False, False],
            "typename": "multipleChoice",

            "topic": 'Containerization',
            "username": 'kbartok',
            "learningoutcome": ["LO 1"],
            "feedback": ["Feedback A", "Feedback B",
                         "Feedback C", "Feedback D"],
            "draft": False,
            "hidden": False

        }
        self.invalid_payload_3 = {
            "_id": "someID1",
            "prompt": "This is a test question A.",
            "shuffleoption": '',
            "choices": ["A", "B", "C", "D"],
            "choiceanswers": [True, False, False, False],
            "typename": "multipleChoice",

            "topic": 'Containerization',
            "username": 'kbartok',
            "learningoutcome": ["LO 1"],
            "feedback": ["Feedback A", "Feedback B",
                         "Feedback C", "Feedback D"],
            "draft": False,
            "hidden": False

        }
        self.invalid_payload_4 = {
            "_id": "someID1",
            "prompt": "This is a test question A.",
            "shuffleoption": False,
            "choices": '',
            "choiceanswers": [True, False, False, False],
            "typename": "multipleChoice",

            "topic": 'Containerization',
            "username": 'kbartok',
            "learningoutcome": ["LO 1"],
            "feedback": ["Feedback A", "Feedback B",
                         "Feedback C", "Feedback D"],
            "draft": False,
            "hidden": False
        }
        self.invalid_payload_5 = {
            "_id": "someID1",
            "prompt": "This is a test question A.",
            "shuffleoption": False,
            "choices": ["A", "B", "C", "D"],
            "choiceanswers": '',
            "typename": "multipleChoice",

            "topic": 'Containerization',
            "username": 'kbartok',
            "learningoutcome": ["LO 1"],
            "feedback": ["Feedback A", "Feedback B",
                         "Feedback C", "Feedback D"],
            "draft": False,
            "hidden": False
        }
        self.invalid_payload_6 = {
            "_id": "someID1",
            "prompt": "This is a test question A.",
            "shuffleoption": False,
            "choices": ["A", "B", "C", "D"],
            "choiceanswers": [True, False, False, False],
            "typename": '',

            "topic": 'Containerization',
            "username": 'kbartok',
            "learningoutcome": ["LO 1"],
            "feedback": ["Feedback A", "Feedback B",
                         "Feedback C", "Feedback D"],
            "draft": False,
            "hidden": False
        }
        self.invalid_payload_7 = {
            "_id": "someID1",
            "prompt": "This is a test question A.",
            "shuffleoption": False,
            "choices": ["A", "B", "C", "D"],
            "choiceanswers": [True, False, False, False],
            "typename": "multipleChoice",
            "topic": "",
            "username": 'kbartok',
            "learningoutcome": ["LO 1"],
            "feedback": ["Feedback A", "Feedback B",
                         "Feedback C", "Feedback D"],
            "draft": False,
            "hidden": False
                        

        }
        self.invalid_payload_8 = {
            "_id": "someID1",
            "prompt": "This is a test question A.",
            "shuffleoption": False,
            "choices": ["A", "B", "C", "D"],
            "choiceanswers": [True, False, False, False],
            "typename": "multipleChoice",

            "topic": 'Containerization',
            "username": '',
            "learningoutcome": ["LO 1"],
            "feedback": ["Feedback A", "Feedback B",
                         "Feedback C", "Feedback D"],
            "draft": False,
            "hidden": False
        }
        self.invalid_payload_9 = {
            "_id": "someID1",
            "prompt": "This is a test question A.",
            "shuffleoption": False,
            "choices": ["A", "B", "C", "D"],
            "choiceanswers": [True, False, False, False],
            "typename": "multipleChoice",
            "topic": 'Containerization',
            "username": 'kbartok',
            "learningoutcome": ["LO 1"],
            "feedback": '',
            'hidden': False,
            'draft': False
        }
        self.invalid_payload_10 = {
            "_id": "someID1",
            "prompt": "This is a test question A.",
            "shuffleoption": False,
            "choices": ["A", "B", "C", "D"],
            "choiceanswers": [True, False, False, False],
            "typename": "multipleChoice",
            "topic": 'Containerization',
            "username": 'kbartok',
            "learningoutcome": '',
            "feedback": ["Feedback A", "Feedback B",
                         "Feedback C", "Feedback D"],
            'hidden': False,
            'draft': False
        }

    def test_create_valid_question(self):
        response = client.post(
            reverse('get_post_question'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_question_1(self):
        response = client.post(
            reverse('get_post_question'),
            data=json.dumps(self.invalid_payload_1),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_question_2(self):
        response = client.post(
            reverse('get_post_question'),
            data=json.dumps(self.invalid_payload_2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_question_3(self):
        response = client.post(
            reverse('get_post_question'),
            data=json.dumps(self.invalid_payload_3),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_question_4(self):
        response = client.post(
            reverse('get_post_question'),
            data=json.dumps(self.invalid_payload_4),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_question_5(self):
        response = client.post(
            reverse('get_post_question'),
            data=json.dumps(self.invalid_payload_5),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_question_6(self):
        response = client.post(
            reverse('get_post_question'),
            data=json.dumps(self.invalid_payload_6),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_question_7(self):
        response = client.post(
            reverse('get_post_question'),
            data=json.dumps(self.invalid_payload_7),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_question_8(self):
        response = client.post(
            reverse('get_post_question'),
            data=json.dumps(self.invalid_payload_8),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_question_9(self):
        response = client.post(
            reverse('get_post_question'),
            data=json.dumps(self.invalid_payload_9),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_question_10(self):
        response = client.post(
            reverse('get_post_question'),
            data=json.dumps(self.invalid_payload_10),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateQuestionTest(TestCase):
    """ Test Module for Updating a Question """

    def setUp(self):

        user1 = Users.objects.create(
            email='kbartok@ualberta.ca', username='kbartok',
            password='blahblah', salt='salty')
        topicA = Topics.objects.create(
            name='Containerization', creator_id=user1,
            learningoutcomes=["LO 1"], tags=["some"])
        #user1 = UsersSerializer(instance=user1)
        #topicA = TopicsSerializer(instance=topicA)

        self.user = Questions.objects.create(
            _id="someID1",
            prompt="This is a test question A.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="multipleChoice",

            topic=topicA,
            username=user1,
            learningoutcome=["LO 1"],
            feedback=["Feedback A", "Feedback B", "Feedback C", "Feedback D"],
            draft = False,
            hidden=False
        )
        self.valid_payload = {
            "_id": "someID1",
            "prompt": "This is a test question AAAA.",
            "shuffleoption": False,
            "choices": ["A", "B", "C", "D"],
            "choiceanswers": [True, False, False, False],
            "typename": "multipleChoice",
            "topic": 'Containerization',
            "username": 'kbartok',
            "learningoutcome": ["LO 1"],
            'hidden': False,
            'draft': False
        }
        self.invalid_payload = {
            "_id": '',
            "prompt": "",
            "shuffleoption": False,
            "choices": ["A", "B", "C", "D"],
            "choiceanswers": [True, False, False, False],
            "typename": "multipleChoice",
            "topic": 'Containerization',
            "username": 'kbartok',
            "learningoutcome": ["LO 1"],
            "feedback": ["Feedback A", "Feedback B", "Feedback C", "Feedback D"],
            'hidden': False,
            'draft': False
        }

    def test_update_valid_question(self):
        response = client.put(
            reverse('get_delete_update_questions', kwargs={
                    '_id': getattr(self.user, '_id')}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_question(self):
        response = client.put(
            reverse('get_delete_update_questions', kwargs={
                    '_id': getattr(self.user, '_id')}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteQuestionTest(TestCase):

    """ Test Module for Deleting a Question """

    def setUp(self):
        user1 = Users.objects.create(
            email='kbartok@ualberta.ca', username='kbartok',
            password='blahblah', salt='salty')
        topicA = Topics.objects.create(
            name='Containerization', creator_id=user1,
            learningoutcomes=["LO 1"], tags=["some"])
        # user1 = UsersSerializer(instance=user1)
        # topicA = TopicsSerializer(instance=topicA)

        self.user = Questions.objects.create(
            _id="someID1",
            prompt="This is a test question A.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="multipleChoice",

            topic=topicA,
            username=user1,
            learningoutcome=["LO 1"],
            feedback=["Feedback A", "Feedback B", "Feedback C", "Feedback D"],
            hidden = False,
            draft= False
        )

    def test_delete_valid_question(self):

        response = client.delete(
            reverse('get_delete_update_questions', kwargs={
                    '_id': getattr(self.user, '_id')}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_valid_question2(self):

        response = client.delete(
            reverse('get_delete_update_questions', kwargs={'_id': 'wrong_id'}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


'''
class GetLearningOutcomeforTopicTest(TestCase):
    """ Test Module for Getting Learning Outcome of a Topic """

    def setUp(self):

        user1 = Users.objects.create(
            email='bbartok@ualberta.ca', username='bartok', 
            password='blahblah', salt='salty')
        topicA = Topics.objects.create(
            name="Topic A", creator_id=user1, tags=["LO 1", "LO 2"])

        TopicLearningOutcome.objects.create(
            topic=topicA, learningoutcome="LO 1"
        )
        TopicLearningOutcome.objects.create(
            topic=topicA, learningoutcome="LO 2"
        )

    def test_get_all_topics(self):
        # Get API Response
        response = client.get(reverse("get_post_learningoutcome"))
        # Get data from DB
        topiclearningoutcome = TopicLearningOutcome.objects.all()
        serializer = TopicLearningOutcomeSerializer(
            topiclearningoutcome, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GenerateNewQuizTest(TestCase):
    # Test Module for Generating a Quiz

    def setUp(self):
        user1 = Users.objects.create(
            email='bbartok@ualberta.ca', username='bartok', 
            password='blahblah', salt='salty')
        topicA = Topics.objects.create(
            name = "Topic A", creator_id=user1, tags=["LO1", "LO 2"])
        Questions.objects.create(
            _id="1",

            prompt="This is a prompt 1.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="mcq",
            ismc=True,

            topic=topicA
        )
        Questions.objects.create(
            _id="2",

            prompt="This is a prompt 2.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="mcq",
            ismc=True,

            topic=topicA

        )

    def test_generate_quiz(self):
        # Get API Response
        response = client.get(reverse('get_questions'))
        # Get data from DB
        questions = Questions.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
'''



class StatisticsQuizTest(TestCase):
    """
    Test module to check if we are correctly getting the statistics from quizzes back
    """
    def setUp(self):
        user1 = Users.objects.create(
            email='tbartok@ualberta.ca', username='tbartok',
            password='blahblah', salt='salty')

        topic1 = Topics.objects.create(
            name="Topic A", creator_id=user1, tags=["sample_tag"],
            learningoutcomes=["LO 1", "LO 2"])
        topic2 = Topics.objects.create(
            name="Topic B", creator_id=user1, tags=["sample_tag"],
            learningoutcomes=["LO 1", "LO 2"])
        topic3 = Topics.objects.create(
            name="Topic C", creator_id=user1, tags=["sample_tag"],
            learningoutcomes=["LO 1", "LO 2"])

        ReviewQuiz.objects.create(
            _id = 'abc',
            questions = ['abcd', 'lmno'],
            answers = ['yes', 'no'],
            correct = 2,
            total = 2,
            username = user1,
            topic = topic1,
            correctness = []
        )
        ReviewQuiz.objects.create(
            _id = 'abcd',
            questions = ['abcd', 'lmno'],
            answers = ['yes', 'no'],
            correct = 2,
            total = 2,
            username = user1,
            topic = topic1,
            correctness = []
        )
        ReviewQuiz.objects.create(
            _id = 'abcde',
            questions = ['abcd', 'lmno'],
            answers = ['yes', 'no'],
            correct = 2,
            total = 2,
            username = user1,
            topic = topic2,
            correctness = []
        )
        ReviewQuiz.objects.create(
            _id = 'abcdefg',
            questions = ['abcd', 'lmno'],
            answers = ['yes', 'no'],
            correct = 2,
            total = 2,
            username = user1,
            topic = topic3,
            correctness = []
        )

    def test_username_topic(self):
        response = client.get(reverse('get_quiz_stats'))
        for _, val in response.data.items():
            self.assertGreater(val['topic'], 0)
        
class QuestionsForTopic(TestCase):
    """
    Test moduel to check if we are correctly getting the information on questions per topic back
    """
    def setUp(self):
        user1 = Users.objects.create(
            email='tbartok@ualberta.ca', username='tbartok',
            password='blahblah', salt='salty')
        topic1 = Topics.objects.create(
            name="Topic A", creator_id=user1, tags=["sample_tag"],
            learningoutcomes=["LO 1", "LO 2"])
        topic2 = Topics.objects.create(
            name="Topic B", creator_id=user1, tags=["sample_tag"],
            learningoutcomes=["LO 1", "LO 2"])
        topic3 = Topics.objects.create(
            name="Topic C", creator_id=user1, tags=["sample_tag"],
            learningoutcomes=["LO 1", "LO 2"])
        Questions.objects.create(
            _id="someID1",
            prompt="This is a test question A.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="multipleChoice",

            topic=topic1,
            username=user1,
            learningoutcome=["LO 1"],
            feedback=["Feedback A", "Feedback B",
                      "Feedback C", "Feedback D"],
            hidden = False,
            draft= False
        )
        Questions.objects.create(
            _id="someID2",
            prompt="This is a test question A.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="multipleChoice",

            topic=topic1,
            username=user1,
            learningoutcome=["LO 1"],
            feedback=["Feedback A", "Feedback B",
                      "Feedback C", "Feedback D"],
            hidden = False,
            draft= False
        )
        Questions.objects.create(
            _id="someID3",
            prompt="This is a test question A.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="multipleChoice",

            topic=topic1,
            username=user1,
            learningoutcome=["LO 1"],
            feedback=["Feedback A", "Feedback B",
                      "Feedback C", "Feedback D"],
            hidden = False,
            draft= False
        )
        Questions.objects.create(
            _id="someID4",
            prompt="This is a test question A.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="multipleChoice",

            topic=topic2,
            username=user1,
            learningoutcome=["LO 1"],
            feedback=["Feedback A", "Feedback B",
                      "Feedback C", "Feedback D"],
            hidden = False,
            draft= False
        )

    def test_number_of_questions(self):
        response = client.get(reverse('get_question_stats'))
        data = response.data.keys()
        data2 = response.data
        value = {'Total': 3, 'LO 1':3}
        for key in data:
            self.assertEqual(data2[key], value )
            break



class RatingsTest(TestCase):
    """
    Test module to check if we are correctly posting ratings and if the api is returning the correct info when ratings are made
    """
    def setUp(self):
        user1 = Users.objects.create(
            email='tbartok@ualberta.ca', username='tbartok',
            password='blahblah', salt='salty')
        user2 = Users.objects.create(
            email='tbartok1@ualberta.ca', username='tbartok2',
            password='blahblah', salt='salty')
        user3 = Users.objects.create(
            email='tbartok11111@ualberta.ca', username='tbartok3',
            password='blahblah', salt='salty')
        topic = Topics.objects.create(
            name="Topic A", creator_id=user1, tags=["sample_tag"],
            learningoutcomes=["LO 1", "LO 2"])
        qid = Questions.objects.create(
            _id="someID1",
            prompt="This is a test question A.",
            shuffleoption=False,
            choices=["A", "B", "C", "D"],
            choiceanswers=[True, False, False, False],
            typename="multipleChoice",

            topic=topic,
            username=user1,
            learningoutcome=["LO 1"],
            feedback=["Feedback A", "Feedback B",
                      "Feedback C", "Feedback D"],
            hidden=False,
            draft=False
        )

        QuestionRatings.objects.create(
            qid=qid,
            username=user1,
            rating=4
        )

        QuestionRatings.objects.create(
            qid=qid,
            username=user3,
            rating=3
        )
        self.valid_payload = {
            'qid': "someID1",
            'username': 'tbartok2',
            'rating': 3
        }
        self.invalid_payload = {
            'qid': 'someID100',
            'username': 'tbartok2',
            'rating': 3
        }


    def test_post_rating(self):
        response = client.post(
            reverse('get_ratings'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_rating_invalid(self):
        response = client.post(
            reverse('get_ratings'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_return(self):
        response = client.get(reverse('get_ratings'), {'username':'tbartok'})
        key = response.data.keys()
        for i in key:
            self.assertEqual(i, 'someID1')
        #self.assertEqual(val, 3.5)