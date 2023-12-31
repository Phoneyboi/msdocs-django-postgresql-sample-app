from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserCreateForm
from django.contrib.auth.decorators import login_required
from experiential import models


# Create your views here.

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

@login_required
def profile(request):
    user_lessons = models.LessonLearned.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'user': request.user, 'user_lessons': user_lessons})
