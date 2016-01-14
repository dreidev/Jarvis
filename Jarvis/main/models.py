from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
import os
from Jarvis import settings


class NameModel(models.Model):
    """
    Base model for name and slug.
    Author: Aly Yakan
    """
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(NameModel, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return str(super(NameModel))

    class Meta:
        abstract = True


class Profile(models.Model):
    """
    User's profile
    Author: Aly Yakan
    """
    user = models.OneToOneField(User)

    photo = models.ImageField(upload_to='profile/', null=True, blank=True)
    about = RichTextField()
    slug = models.CharField(max_length=256)

    def experience(self):
        """
        Returns all experience entries for a user.
        Author: Aly Yakan
        """
        return Experience.objects.filter(user=self.user, accepted=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username


class Project(NameModel):
    """
    A single Project entry.
    Author: Aly Yakan
    """
    collaborators = models.ManyToManyField(User, related_name='projects')
    description = RichTextField()
    done = models.BooleanField(
        default=False)  # False: in progress,True: Done
    link = models.URLField(null=True, blank=True, max_length=1024)


class ProjectImage(models.Model):
    """
    A single ProjectImage Entry belonging to a certain Project.
    Author: Aly Yakan
    """
    project = models.ForeignKey(Project)

    image = models.ImageField(upload_to='profile/')

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.photo.name))
        super(ProjectImage, self).delete(*args, **kwargs)


class ExperienceCategory(NameModel):
    """
    Categories for Experience Points
    Author: Aly Yakan
    """
    pass


class Experience(models.Model):
    """
    Experience points for user <user> working on project <project>
    Author: Aly Yakan
    """
    user = models.ForeignKey(Profile)
    project = models.ForeignKey(Project)
    category = models.ForeignKey(ExperienceCategory)

    points = models.IntegerField(null=False)
    accepted = models.BooleanField(default=False)

    def __unicode__(self):
        return "pts: %s, usr: %s, accepted: %s, prjct: %s" % (
            self.points, self.user.username, self.accepted, self.project)


class Trophy(NameModel):
    """
    A single instance of a trophy.
    Author: Aly Yakan
    """
    user = models.ManyToManyField(User, related_name="trophies")

    type = models.CharField(max_length=256)
    badge = models.ImageField(upload_to='trophy/', null=True, blank=True)
    points = models.IntegerField()


class Coffee(NameModel):
    """
    A single Coffee Entry by a user in a project.
    Author: Aly Yakan
    """
    project = models.ForeignKey(Project, blank=True, null=True)
    user = models.ForeignKey(User)

    cups = models.IntegerField(default=1)
