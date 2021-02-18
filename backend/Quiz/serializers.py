from .models import *
from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField


class QuestionSerializer(serializers.ModelSerializer):
    #topcomment_listing = serializers.HyperlinkedIdentityField(view_name='topcomment-list')
    class Meta:
        model = Questions

        fields = ['_id', 'prompt', 'shuffleoption', 'choices', 'choiceanswers',
                  'typename', 'topic', 'username', 'learningoutcome', 'feedback', 'draft', 'hidden']
        lookup_field = '_id'


'''

class QuestionTagSerializer(serializers.HyperlinkedModelSerializer):
    qid = serializers.HyperlinkedIdentityField(view_name="Quiz:QuestionByLearningOutcome-detail")
    class Meta:
        model = QuestionTags
        fields = ['qid', 'tag']
'''


class UsersSerializer(serializers.ModelSerializer):
    #topcomment_listing = serializers.HyperlinkedIdentityField(view_name='topcomment-list')
    class Meta:
        model = Users
        # , 'topcomment_listing']
        fields = ['email', 'username', 'password', 'created_at', 'contributor', 'student', 'professor', 'admin']
        lookup_field = 'username'


class ReviewQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewQuiz
        fields = ['_id', 'questions', 'answers', 'correct',
                  'total', 'username', 'topic', 'correctness']


class TopicsSerializer(serializers.ModelSerializer):
    learningoutcomes = serializers.ListField(child=serializers.CharField())
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Topics
        fields = ['name', 'creator_id', 'tags', 'learningoutcomes']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['tag']


class QuestionLearningOutComeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionLearningOutCome
        fields = ['qid', 'learningoutcome', 'topic']


class TopicLearningOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicLearningOutcome
        fields = ['topic', 'learningoutcome']


class QuestionCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['_id', 'username']
        lookup_field = '_id'


class TopCommentSerializer(serializers.ModelSerializer):
    #parentid = QuestionCommentSerializer()
    #parentid = serializers.HyperlinkedRelatedField(queryset=Questions.objects.all(), view_name='question-detail', lookup_field='_id')
    #user = serializers.HyperlinkedRelatedField(view_name='users-detail',read_only=True, lookup_field='username')
    class Meta:
        model = TopComment
        fields = ['parentid', 'commentid', 'comment', 'user', 'date']
        lookup_field = 'commentid'


class ChildCommentSerializer(serializers.ModelSerializer):
    #topcommentid = serializers.HyperlinkedRelatedField(view_name='topcomment-detail',read_only=True, lookup_field='commentid')
    #user = serializers.HyperlinkedRelatedField(view_name='users-detail',read_only=True, lookup_field='username')
    class Meta:
        model = ChildComment
        fields = ['parentid', 'id', 'comment', 'user', 'date']


class QuestionRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionRatings
        fields = ['qid', 'username', 'rating']
