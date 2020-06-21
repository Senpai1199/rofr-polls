from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    """
        Model for managing the fields for a Poll made by admin
    """

    title = models.CharField(max_length=200, blank=True)
    attempted_count = models.PositiveIntegerField(default=0) # no. of users who took the poll
    min_age = models.SmallIntegerField(default=0)
    max_age = models.SmallIntegerField(default=0)
    min_income = models.SmallIntegerField(default=0)
    max_income = models.SmallIntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.id, self.title)

class Question(models.Model):
    """
        Model for managing the details of a question that belongs to a certain Poll
    """

    QUESTION_TYPES = (
        ('MCSO', 'Multi Choice Single Option'),
        ('MCMO', 'Multi Choice Multi Option'),
        ('OWNI', 'One Word or Number Input'),
        ('S', 'Scale input (1-5)'),
        ('E', 'Emoticon Input'),
    )

    title = models.CharField(max_length=200, blank=True)
    optional = models.BooleanField(default=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="questions", null=True)
    category = models.CharField(choices=QUESTION_TYPES, null=False, max_length=4, default='OWNI')

    def __str__(self):
        return "{} - {}".format(self.id, self.title)

class UserProfile(models.Model):
    '''
        Model for managing the users registering on the polls app.
        Email and first, last names are stored in the Django User model.
    '''
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )

    auth_user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, unique=True, related_name="profile") #related_name for getting
                                                                                                                      # the profile of a user instance
    gender = models.CharField(choices=GENDERS, null=True, max_length=1)
    age = models.PositiveIntegerField()
    income = models.PositiveIntegerField()
    location = models.CharField(max_length=200, blank=False)
    attempted_polls = models.ManyToManyField(Poll, related_name="users_attempted", blank=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        indexes = [models.Index(fields=['id'])]

    def __str__(self):
        return "{} - {}".format(self.id, self.auth_user.email)

class UserResponse(models.Model):
    """
        Handles the details of a user's response to a particular poll
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="responses", null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses", null=True)
    response = models.CharField(max_length=200, blank=False)
    poll_taker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.response)



