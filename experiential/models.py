from django.db import models
from accounts.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.conf import settings


# Create your models here.
class ExperientialFrame(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # Default to current time

    def __str__(self):
        return self.name

    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(ExperientialFrame, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('experiential:frame_detail', kwargs={'slug': self.slug})


class Experience(models.Model):
    experiential_frame = models.ForeignKey(ExperientialFrame, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # Default to current time

    def __str__(self):
        return self.title


class AuthenticImmersiveExperience(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, null=True, blank=True)

    aie_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)  # Default to current time

    def __str__(self):
        return self.aie_name


class LessonLearned(models.Model):  # What can this be called? 'Expy'? Null? Why does it need a name?
    # Let it be without a name.
    experiential_frame = models.ForeignKey(ExperientialFrame, on_delete=models.CASCADE, null=True, blank=True)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, null=True, blank=True)
    aie_name = models.ForeignKey(AuthenticImmersiveExperience, on_delete=models.CASCADE, null=True, blank=True)
    takeaway = models.TextField()  # To be named: Takeaway
    learning_statement = models.TextField()  # To be named: Insight
    value_statement = models.TextField()  # To be named: Value
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)  # Default to current time

    def __str__(self):
        return (f"Takeaway: {self.takeaway}, \nLearning Statement: {self.learning_statement}, "
                f"\nValue Statement: {self.value_statement}, \nCreated by: {self.user},"
                f"\nCreated at: {self.created_at}")

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'experiential_frame', 'experience', 'aie_name', 'takeaway', 'learning_statement',
                           'value_statement']
