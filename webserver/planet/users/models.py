from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django import forms
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for The Planet."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

class Team(models.Model):
    name = models.CharField(max_length=255)

class TeamMember(models.Model):
    team = models.ForeignKey(Team , on_delete=models.CASCADE)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

class Problem(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    category = forms.ChoiceField(choices=[
        (1, _("Environment")),
        (2, _("Politics"))
    ])

    prize = models.CharField(max_length=30)
    allow_attachment = forms.ChoiceField(choices=[
        (1, _("No")),
        (2, _("1 File")),
        (3, _("2 File")),
        (4, _("3 File")),
    ])

    created = models.DateTimeField(auto_now_add=True, blank=True)
    deadline = models.DateTimeField(blank=True)

class Solution(models.Model):
    solver_member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    solver_team = models.ForeignKey(Team, on_delete=models.PROTECT, null=True, blank=True)
    body = models.TextField()
    general_attachment = forms.FileField(required=False)
    metrics_attachment = forms.FileField(required=False)

class SolutionEvaluation(models.Model):
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    cost = models.IntegerField()
    income = models.IntegerField()
    violence = models.IntegerField()
    human_loss = models.IntegerField()
    non_human_loss = models.IntegerField()
    future_opportunities = models.IntegerField()
    future_loss = models.IntegerField()
    used_politics = models.IntegerField()
    used_science = models.IntegerField()
    cited_science = models.IntegerField()
    extra_scale_1 = models.IntegerField(default=0)
    extra_scale_1_title = models.CharField(max_length=255, default="")
    extra_scale_2 = models.IntegerField(default=0)
    extra_scale_2_title = models.CharField(max_length=255, default="")
    extra_scale_3 = models.IntegerField(default=0)
    extra_scale_3_title = models.CharField(max_length=255, default="")


class SolutionRating(models.Model):
    solution = models.ForeignKey(Solution, on_delete = models.PROTECT)
    rater = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    rating = models.IntegerField()

