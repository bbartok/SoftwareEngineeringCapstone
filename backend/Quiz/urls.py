from django.urls import path
from . import views

urlpatterns = [

    # Question URLS
    path('api/Quiz/SetQuestion', views.QuestionByIDViewSet.as_view(),
         name='question-detail'),
    path('api/Quiz/QuestionByLOC', views.QuestionByLearningOutcome.as_view()),
    path('api/Quiz/Questions', views.QuestionViewSet.as_view(),
         name='get_post_question'),
    path('api/Quiz/QuestionMod/<str:_id>/',
         views.QuestionModViewSet.as_view(), name='get_delete_update_questions'),
    path('api/Quiz/GenerateQuiz',
         views.QuestionIDByTopic.as_view(), name="get_questions"),
    path('api/Quiz/QuestionRatings', views.QuestionRatingsViewSet.as_view()),

    # Topic URLS
    path('api/Quiz/Topics', views.TopicViewSet.as_view(), name='get_post_topics'),
    path('api/Quiz/TopicMod/<str:name>/', views.TopicModViewSet.as_view(),
         name='get_delete_update_topics'),
    path('api/Quiz/LearningOutcome', views.TopicLearningOutcomeViewSet.as_view()),

    # Quiz URLs
    path('api/Quiz/Quiz', views.ReviewQuizViewSet.as_view()),
    path('api/Quiz/Comment', views.TopCommentViewSet.as_view()),

  
    #stats URLS
    path('api/Quiz/StatsByTopic', views.StatisticsByTopicViewSet.as_view(), name='get_quiz_stats'),
    path('api/Quiz/NumberOfQuestions', views.QuestionsForTopicAndLOCViewSet.as_view(), name='get_question_stats'),
    path('api/Quiz/MyQuestionRatings', views.UserMadeQuestionRatingsViewSet.as_view(), name='get_ratings' ),

    #user URLS
    path('api/Quiz/Users', views.UsersViewSet.as_view(), name='get_post_users'),
]
