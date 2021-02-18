"""
All the views for our Quiz application.

Currently we support the following views:

1. **Questions** - Called to *get* and *add* questions.
2. **QuestionMod** - Called to *get*, *update* and *delete* a specific question.
3. **Topics** - Called to *get* and *add* topics.
4. **TopicMod** - Called to *get*, *update* and *delete* a specific topic.
5. **GenerateQuiz** - Called to *get* a set of questions.
6. **Quiz** - Called to *get* and *add* quizzes.
7. **Comment** - Called to *get* and *add* comments.
8. **MyQuestionRatings** - Called to *get* ratings for a question.
9. **StatsByTopic** - Called to *get* statistics per topic.

Views are built with [Generic Views](https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview) from the Django REST framework.

"""

from .models import *
from .serializers import *

# Python Libraries
import json
import random
import hashlib

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
import django_filters.rest_framework
from rest_framework import pagination

# -----

# === Users Views ===


class UsersViewSet(generics.ListCreateAPIView):
    serializer_class = UsersSerializer
    querset = []

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username is None:
            queryset = Users.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save()

# -----

# === Custom Pagination ===


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        current = self.request.build_absolute_uri()
        current_num = self.page.number
        next_page = None
        if self.page.has_next():
            next_page = replace_query_param(
                current, self.page_query_param, current_num+1)
        previous = None
        if current_num > 1:
            previous = replace_query_param(
                current, self.page_query_param, current_num-1)
        return Response({

            'next': next_page,  # self.get_next_link(),
            'previous': previous,  # self.get_previous_link(),

            'total_pages': int(self.page.paginator.count/int(self.page_size)),
            'page_size': int(self.page_size),
            'page': self.page.number,
            'results': data,
        })

# -----

# === Question View ===


class QuestionViewSet(generics.ListCreateAPIView):
    """
    The QuestionViewSet class defines the Questions endpoint that allows
    the user to get questions from the system and add questions to the system.
    """
    serializer_class = QuestionSerializer
    queryset = []

    def get_queryset(self):
        """
        Depending on the given parameters, this function returns a set of
        questions in the system either with pagination or without it.

        The optional parameters are:

        - **username**: Username who created the question.
        """

        username = self.request.query_params.get('username', None)

        if username is None:
            queryset = Questions.objects.all()

        queryset = Questions.objects.exclude(hidden=True)
        return queryset

    def perform_create(self, serializer):
        """
        Add a Question

        The function encrypts the prompt of a question to generate a unique ID
        for the question. If the question does not exist, the question will be
        added to the system. If it does, the question will not be added and
        the user will be prompted an error message.
        """
        prompt = self.request.data.get('prompt', None)
        id = hashlib.sha224(prompt.encode("utf-8")).hexdigest()
        queryset = Questions.objects.filter(_id=id)

        # Checks if the a question with a same question id exists
        if queryset.exists():
            raise ValidationError('This question already exists.')

        serializer.save(_id=id)

# -----

# === QuestionMod View ===


class QuestionModViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
    The QuestionModViewSet class defines the QuestionMod endpoint that allows
    the user to get, update and delete a specific question in the system.
    """
    serializer_class = QuestionSerializer
    lookup_field = '_id'
    queryset = []

    def get_queryset(self):
        """
        If required parameters are met, this function returns a specific
        question in the system.

        The required parameters are:

        - **id**: Question ID.
        """
        id = self.kwargs['_id']
        queryset = Questions.objects.filter(_id=id)
        return queryset

    def perform_update(self, serializer):
        """
        If required parameters are met, this function updates a specific
        question in the system.
        """
        serializer.save()

    """
    Remove a Question

    Uses the default DestroyAPIView implementation.
    """

# -----

# === MyQuestionRatings View ===


class QuestionRatingsViewSet(generics.ListCreateAPIView):
    """
    The QuestionRatingsViewSet class defines the MyQuestionRatings endpoint
    that allows the user to get and add ratings for a specific question
    in the system.
    """
    serializer_class = QuestionRatingsSerializer

    def get(self, request, *args, **kwargs):
        """
        If required parameters are met, this function returns a set of ratings
        associated with the question in the system.

        The required parameters are:

        - **qid**: Question ID.
        """
        qid = self.request.query_params.get('qid', None)
        queryset = QuestionRatings.objects.filter(qid=qid).values()
        rating = 0
        ratingCount = 0
        for item in queryset:
            rating += item['rating']

        total = len(queryset)
        if total == 0:
            ratingDec = None
        else:
            ratingDec = rating/ratingCount

        obj = {'qid': qid, 'rating': ratingDec,
               'Number of ratings': ratingCount}

        response = Response(obj)
        return response

    def perform_create(self, serializer):
        """
        If required parameters are met, this function adds a rating
        associated with a question in the system.
        """
        serializer.save()


# -----

# === Question by X Views ===



class QuestionByIDViewSet(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        id = self.request.query_params.get('qID', None)
        queryset = Questions.objects.filter(_id=id)
        return queryset

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class QuestionIDByTopic(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        topic = self.request.query_params.get('topic', None)
        number = self.request.query_params.get('numQuestions', None)

        queryset = Questions.objects.filter(
            topic=topic, typename="multipleChoice")

        if number is not None:
            queryset = random.sample(list(queryset), int(number))

        return queryset


class QuestionByLearningOutcome(generics.ListCreateAPIView):
    serializer_class = QuestionLearningOutComeSerializer

    def get_queryset(self):
        topic = self.request.query_params.get('topic', None)
        learningoutcome = self.request.query_params.get(
            'learningoutcome', None)
        learningoutcome = learningoutcome.split(",")

        # Gets the list of queries that need to be checked for learning outcome
        queries = []
        querysetquery = []
        for item in learningoutcome:
            queryset = QuestionLearningOutCome.objects.filter(
                topic=topic, learningoutcome=item)
            queryval = queryset.values()
            queries.append(queryval)
            querysetquery.append(queryset)
        accepted = {}

        # counts to see if the question matches the number of times a learning outcome is shown
        for item in queries:
            for q in item:
                if q['qid'] not in accepted:
                    accepted[q['qid']] = 1
                else:
                    accepted[q['qid']] += 1
        send = []

        # This is some nasty ass code maybe I'll fix it later
        # Anyway what it does its check to see if a question has a learningoutcome for each request one
        # then it finds the index of the actual query item and adds it to a list
        for item in accepted:
            if accepted[item] == len(queries):
                for i in range(len(queries)):
                    for j in range(len(queries[i])):
                        if item == queries[i][j]['qid']:
                            send.append(querysetquery[i][j])

        return send

# -----

# === Quiz Views ===


class ReviewQuizViewSet(generics.ListCreateAPIView):
    """
    The ReviewQuizViewSet class defines the Quiz endpoint that allows
    the user to get and add quizzes in the system.
    """
    serializer_class = ReviewQuizSerializer

    def get_queryset(self):
        """
        If required parameters are met, this function returns a set of quizzes
        in the system.

        The optional parameters are:

        - **_id**: Quiz ID.
        - **username**: Username who made the quiz.
        """
        id = self.request.query_params.get("_id", None)
        username = self.request.query_params.get("username", None)

        if id is None and username is None:
            queryset = ReviewQuiz.objects.all()
        else:
            if id is not None:
                queryset = ReviewQuiz.objects.filter(_id=id)
            if username is not None:
                queryset = ReviewQuiz.objects.filter(username=username)

        return queryset

    def perform_create(self, serializer):
        """
        If required parameters are met, this function adds a quiz
        to the system.
        """
        serializer.save()

# -----

# === Topic Views ===


class TopicViewSet(generics.ListCreateAPIView):
    """
    The TopicViewSet class defines the Topics endpoint that allows
    the user to get and add topics in the system.
    """
    serializer_class = TopicsSerializer
    queryset = []

    def get_queryset(self):
        """
        If required parameters are met, this function returns a set of topics
        in the system.

        The optional parameters are:

        - **name**: Topic name.
        """
        topic = self.request.query_params.get('name', None)

        if topic is not None:
            queryset = Topics.objects.filter(name=topic, hidden=False)
        else:
            queryset = Topics.objects.all().filter(hidden=False)

        return queryset

    def perform_create(self, serializer):
        """
        If required parameters are met, this function add a topic
        to the system.
        """
        serializer.save()


class TopicLearningOutcomeViewSet(generics.ListCreateAPIView):
    serializer_class = TopicLearningOutcomeSerializer

    def get_queryset(self):
        topic = self.request.query_params.get('topic', None)
        if topic is not None:
            queryset = TopicLearningOutcome.objects.filter(topic=topic, hidden=False)
        else:
            queryset = TopicLearningOutcome.objects.all()
        return queryset

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TopicModViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
    The TopicModViewSet class defines the TopicMod endpoint that allows
    the user to get, update and delete a specific topic in the system.
    """
    serializer_class = TopicsSerializer
    lookup_field = 'name'
    queryset = []

    def get_queryset(self):
        """
        If required parameters are met, this function returns a specified topic
        in the system.

        The required parameters are:

        - **name**: Topic name.
        """
        name = self.kwargs['name']
        queryset = Topics.objects.filter(name=name, hidden=False)
        return queryset

    def perform_update(self, serializer):
        """
        If required parameters are met, this function updates a specified topic
        in the system.

        The required parameters are:

        - **name**: Topic name.
        """
        instance = serializer.save()

    """
    Remove a topic from the system.

    Uses the default DestroyAPIView implementation.
    """

# -----

# === Comment Views ===


class TopCommentViewSet(generics.ListCreateAPIView):
    """
    The TopCommentViewSet class defines the Comment endpoint that allows
    the user to get and add comments for a question in the system.
    """
    serializer_class = TopCommentSerializer
    lookup_field = "_id"

    def get_queryset(self):
        """
        If required parameters are met, this function returns a set of comments
        for a question in the system.

        The optional parameters are:

        - **questionID**: Question ID.
        """
        questionId = self.request.query_params.get('questionID', None)
        queryset = TopComment.objects.filter(parentid_id=questionId)
        return queryset

    def perform_create(self, serializer):
        """
        If required parameters are met, this function add a comment
        for a question in the system.
        """
        comment = self.request.data.get('comment', None)
        topcommentid = hashlib.sha224(comment.encode("utf-8")).hexdigest()
        parentid = self.request.data.get('parentid', None)
        parentid = hashlib.sha224(parentid.encode("utf-8")).hexdigest()
        finalid = topcommentid[:12] + parentid[12:]
        queryset = TopComment.objects.filter(commentid=finalid)
        if queryset.exists():
            raise ValidationError('CommentID already Exists')
        serializer.save(commentid=finalid)


class TopCommentUpdateViewSet(generics.UpdateAPIView):
    serializer_class = TopCommentSerializer

    def perform_update(self, serializer):
        serializer.save()


class ChildCommentViewSet(generics.ListCreateAPIView):
    serializer_class = ChildCommentSerializer

    def get_queryset(self):
        parentid = self.request.query_params.get('parentid', None)
        queryset = ChildComment.objects.filter(parentid=parentid)
        return queryset

    def perform_create(self, serializer):
        parentid = self.request.data.get('parentid', None)
        parentid = hashlib.sha224(parentid.encode("utf-8")).hexdigest()
        comment = self.request.data.get('comment', None)
        id = hashlib.sha224(id.encode("utf-8")).hexdigest()
        finalId = parentid[:12] + id[12:]
        queryset = ChildComment.objects.filter(id=finalId)
        if queryset.exists():
            raise ValidationError('Comment already Exists')
        serializer.save(id=finalId)


class ChildCommentUpdateViewSet(generics.UpdateAPIView):
    serializer_class = ChildCommentSerializer

    def perform_update(self, serializer):
        serializer.save()


"""
----------------------------------------------------------------------------
Statistics Views
----------------------------------------------------------------------------
"""


class StatisticsByTopicViewSet(generics.ListCreateAPIView):
    """
    The StatisticsByTopicViewSet defines the endpoint that allows for
    the user to obtain statistics on quizzes for topics.
    It returns the topic and how many right/wrong answers there are.
    The GET can take two arguments:
    - **userId**: the id of the user you want statistics on (optional)
    - **topicId**: the topic you want statistics on (optional)
    If both are provided, it will return stats on a specific user for a specific topic,
    if no user is provided, but a topic is, it will return stats on all users for the given topic,
    if a topic is not given, but a user is, it will return the stats on all topics for that user,
    if neither is given, it will return all stats on all quizzes that have been taken.
    """
    serializer_class = ReviewQuizSerializer

    def get(self, request, *args, **kwargs):
        topicId = self.request.query_params.get('topic', None)
        userId = self.request.query_params.get('username', None)


        # Case 1: User and Topic provided
        if userId != None and topicId != None:
            queryset = ReviewQuiz.objects.filter(
                topic=topicId, username=userId)
        # Case 2: Only Topic provided
        elif topicId != None:
            queryset = ReviewQuiz.objects.filter(topic=topicId)
        # Case 3: Only User provided
        elif userId != None:
            queryset = ReviewQuiz.objects.filter(username=userId)
        # Case 4: Nothing provided

        else:
            queryset = ReviewQuiz.objects.all()

        retdict = {}
        for item in queryset.values():
            # Add to dict
            if item['topic_id'] not in retdict:
                retdict[item['topic_id']] = {'topic': 0, 'correct': 0}
            # Increase count by total and correct for that quiz
            retdict[item['topic_id']]['topic'] += item['total']
            retdict[item['topic_id']]['correct'] += item['correct']

        response = Response(retdict)

        return response


class QuestionsForTopicAndLOCViewSet(generics.ListCreateAPIView):
    """
    The QuestionsForTopicAndLOCViewSet defines the endpoint that allows for
    the user to see how many questions exist for a given topic or learningoutcome
    There are two arguments that may be passed to this function:
    - **topic**: the topic you want information on (optional)
    - **learningOutcome**: the learning Outcome you want information on (optional)
    If only a topic is provided, it will return stats on that topic, if a learningoutcome is 
    also specified, it will return informatin on the topic and only that learning outcome
    if neither is specified, it will return info on all topics.
    """
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        topic = self.request.query_params.get('topic', None)
        learningOutcome = self.request.query_params.get(
            'learningOutcome', None)

        if topic != None:
            querysetTopic = Questions.objects.filter(topic=topic).values()
        else:
            querysetTopic = Questions.objects.all().values()

        retdict = {}
        # If a topic was given, get size, else find total topics
        if topic != None:
            retdict[topic] = {'total': len(querysetTopic)}
            # Gets LOC if provided
            if learningOutcome != None:
                for item in querysetTopic:
                    if learningOutcome in item['learningoutcome']:
                        if learningOutcome not in retdict[item['topic_id']]:
                            retdict[item['topic_id']][learningOutcome] = 1
                        else:
                            retdict[item['topic_id']][learningOutcome] += 1

            else:
                for item in querysetTopic:
                    for val in item['learningoutcome']:
                        if val not in retdict[item['topic_id']]:
                            retdict[item['topic_id']][val] = 1
                        else:
                            retdict[item['topic_id']][val] += 1

        else:
            for item in querysetTopic:

                # Get number of questions

                if item['topic_id'] not in retdict:
                    retdict[item['topic_id']] = {'Total': 1}
                else:
                    retdict[item['topic_id']]['Total'] += 1

                # Gets LOC if provided
                for val in item['learningoutcome']:
                    if val not in retdict[item['topic_id']]:
                        retdict[item['topic_id']][val] = 1
                    else:
                        retdict[item['topic_id']][val] += 1

        response = Response(retdict)
        return response


class UserMadeQuestionRatingsViewSet(generics.ListCreateAPIView):
    """
    The UserMadeQuestionRatingsViewSet defines the endpoint that allows a user to see the ratings of their questions
    it takes two parameters:
    - **username**: the username of the person you want statistics on (optional)
    - **qid**: the question id you want information on (optional)
    if you want to see how all questions are rated for a user, you can provide their username, if you want to specifically see one
    question, you can provide the question id.

    Note that at least one of them MUST be provided
    """
    serializer_class = QuestionRatingsSerializer

    def get(self, request, *args, **kwargs):
        username = self.request.query_params.get('username', None)
        qid = self.request.query_params.get('qid', None)

        queryset = None
        # qid for specific
        # user for generic all my qs
        if qid != None:
            queryset = QuestionRatings.objects.filter(qid=qid).values()
        if username != None:
            questions = Questions.objects.filter(username=username).values()
            queryset = []
            for item in questions:
                items = QuestionRatings.objects.filter(
                    qid=item['_id']).values()
                for val in items:
                    queryset.append(val)

        if queryset == None:
            return Response("Error: you need to provide a qid or username")

        obj = {}
        count = {}
        for item in queryset:
            if item['qid_id'] not in obj:
                obj[item['qid_id']] = item['rating']
                count[item['qid_id']] = 1
            else:
                obj[item['qid_id']] += item['rating']
                count[item['qid_id']] += 1
        for item in obj:
            obj[item] = obj[item]/count[item]
        response = Response(obj)
        return response

    def perform_create(self, serializer):
        """
        If required parameters are met, this function adds a rating
        to the system.
        """
        serializer.save()
