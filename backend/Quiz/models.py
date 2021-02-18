#import jwt

from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

# === Models for Quiz App ===

# === Question Model ===


class Questions(models.Model):
    """
    The Question class defines the main storage point for questions.
    Each question has twelve fields:

    - **_id**: Stores the unique identifier of a question.
    - **prompt**: Stores the prompt of the question.
    - **shuffleOption**: Used to control if the answers choices are shuffled.
    - **learningOutCome**: Stores a list of learning outcome associated with the question.
    - **typeName**: Used to control the amount of answer choices are allowed to be selected.
    - **topic**: Stores the topic associated with the question.
    - **username**: Stores the username who created the question.
    - **choices**: Stores the choices for a question.
    - **choiceanswers**: Stores the correctness of the choices.
    - **feedback**: Stores the feedback for each choice.
    - **draft**: Used to control if the question will appear in quizzes.
    - **hidden**: Used to control if the question is displayed to users.
    """

    _id = models.TextField(primary_key=True, null=False)
    prompt = models.TextField(null=False)
    shuffleoption = models.BooleanField(null=False, default=False)
    choices = ArrayField(models.TextField())
    choiceanswers = ArrayField(models.BooleanField(default=False))
    typename = models.TextField()
    topic = models.ForeignKey('Topics', on_delete=models.PROTECT)
    username = models.ForeignKey('Users', on_delete=models.PROTECT)
    learningoutcome = ArrayField(models.TextField(null=False))
    feedback = ArrayField(models.TextField(null=True), null=True)
    draft = models.BooleanField(null=False)
    hidden = models.BooleanField(null=False)
    # comments = ArrayField(models.TextField())

    class Meta:
        db_table = "questions"


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, student=False, professor=False):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('Users must have a password')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.contributor = True
        user.student = student
        user.professor = professor
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('User requires password')

        user = self.create_user(username, email, password)
        user.admin = True
        user.save()

        return user


class Users(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address', unique=True, db_index=True)
    username = models.TextField(primary_key=True)
    active = models.BooleanField(default=True)
    student = models.BooleanField(default=False)
    salt = models.TextField()
    contributor = models.BooleanField(default=True)
    professor = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):

        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    # TODO
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_student(self):
        return self.student

    @property
    def is_professor(self):
        return self.professor

    @property
    def is_admin(self):
        return self.admin

    def is_active(self):
        return self.active

    class Meta:
        db_table = 'users'


"""
Model for Tags table in db
tag: text field is used as primary key
"""

# === Tag Model ===


class Tags(models.Model):
    """
    The Tag class defines the main storage point for tags.
    Tags are used to tag topics.

    Each tag has one field:

    - **tag**: Stores the text of a tag.
    """
    tag = models.TextField(primary_key=True)

    class Meta:
        db_table = 'tags'

# === Topic Model ===


class Topics(models.Model):
    """
    The Topic class defines the main storage point for topics.

    Each topic has four fields:

    - **name**: Stores the unique name of a topic.
    - **creator_id**: Stores the user who created the topic.
    - **learningOutcomes**: Stores an array of learning outcomes in a topic.
    - **tags**: Stores an array of tags associated to the topic.
    """
    name = models.TextField(primary_key=True, null=False)
    creator_id = models.ForeignKey('Users', on_delete=models.PROTECT)
    learningoutcomes = ArrayField(models.TextField(null=False))
    tags = ArrayField(models.TextField())
    hidden = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'topics'

# === Review Quiz Model ===


class ReviewQuiz(models.Model):
    """
    The Review Quiz class defines the main storage point for completed
    quizzes that are generated by Students

    Each review quiz has eight fields:

    - **_id**: Stores the unique idenfier of a completed quiz.
    - **questions**: Stores an array of question IDs.
    - **answers**: Stores an array of answers selected by the Student.
    - **correct**: Stores an integer of the amount of question the Student got correct in the quiz.
    - **total**: Stores an integer of the amount of questions in the quiz.
    - **username**: Stores the username who took the quiz.
    - **topic**: Stores the topic associated with the quiz.
    - **correctness**: Stores an array of correctness of each question in the quiz.
    """

    _id = models.TextField(primary_key=True)
    questions = ArrayField(models.TextField())
    answers = ArrayField(models.TextField())
    correct = models.IntegerField(null=False, default=1)
    total = models.IntegerField(null=False)
    username = models.ForeignKey('Users', on_delete=models.PROTECT)
    topic = models.ForeignKey('Topics', on_delete=models.PROTECT)
    correctness = ArrayField(models.TextField())

    class Meta:
        db_table = 'quizzes'


# === Question Tag Model ===

class QuestionTags(models.Model):
    """
    Model for QuestionTags table in db

    - qid: question id tag, foreign key
    - tag: tag, foreign key
    """
    qid = models.ForeignKey('Questions', on_delete=models.PROTECT)
    tag = models.TextField(null=False)

    class Meta:
        db_table = 'questiontags'

# === Question Learning Outcome Model ===


class QuestionLearningOutCome(models.Model):
    """
    Model for QuestionLearningOutcome table in db

    - qid: question id tag, foreign key
    - learningOutcome: learning outcome associated with question
    - topic: topic assossciated with question
    """
    qid = models.ForeignKey(Questions, on_delete=models.PROTECT)
    learningoutcome = models.TextField()

    class Meta:
        db_table = 'questionlearningoutcome'

# === Topic and Learning Outcome Model


class TopicLearningOutcome(models.Model):

    topic = models.ForeignKey('Topics', on_delete=models.PROTECT)
    learningoutcome = models.TextField(null=False)

    class Meta:
        db_table = 'topiclearningoutcome'

# === TopComment Model ===


class TopComment(models.Model):
    """
    The TopComment class defines the main storage point for the top comments for questions.
    Each TopComment has five fields:

    - **parentid**: Stores the question ID associated with a comment.
    - **commentid**: Stores the unique idenfier of a comment.
    - **comment**: Stores the text comment of the comment.
    - **user**: Stores the username who created the comment.
    - **date**: Stores the creation data of the comment.
    """
    parentid = models.ForeignKey('Questions', on_delete=models.CASCADE)
    commentid = models.TextField(primary_key=True)
    comment = models.TextField(null=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        db_table = 'topcomment'

# === ChildComment Model ===


class ChildComment(models.Model):
    """
    The ChildComment class defines the main storage point for the child comments as TopComments.
    Each TopComment has five fields:

    - **parentid**: Stores the topComment ID associated with the child comment.
    - **id**: Stores the unique idenfier of a child comment.
    - **comment**: Stores the text comment of the child comment.
    - **user**: Stores the username who created the child comment.
    - **date**: Stores the creation data of the child comment.
    """
    parentid = models.ForeignKey('TopComment', on_delete=models.CASCADE)
    id = models.TextField(primary_key=True)
    comment = models.TextField(null=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        db_table = 'childcomment'

# === QuestionRating Model ===


class QuestionRatings(models.Model):
    """
    The QuestionRating class defines the main storage point for ratings for a question.
    Each QuestionRating has three fields:

    - **qid**: Stores the question ID associated with the rating.
    - **username**: Stores the username who created the rating.
    - **rating**: Stores an integer indicating the rating (0 - 5).
    """
    qid = models.ForeignKey(Questions, on_delete=models.PROTECT)
    username = models.ForeignKey(Users, on_delete=models.PROTECT)
    rating = models.IntegerField()

    class Meta:
        db_table = 'questionratings'
        unique_together = (("qid", "username"),)
