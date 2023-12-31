from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from .models import ExperientialFrame, Experience, AuthenticImmersiveExperience, LessonLearned
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import IntegrityError, transaction
from .forms import LessonLearnedForm


# Example ListView for Frame model
class FrameListView(ListView):
    model = ExperientialFrame
    template_name = 'experiential/frames_list.html'  # This warning is a lie. Pay no attention.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frames'] = ExperientialFrame.objects.all()
        return context


# Example DetailView for Frame model
class FrameDetailView(DetailView):
    model = ExperientialFrame
    template_name = 'experiential/frame_detail.html'  # This warning is a lie. Pay no attention.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the current frame from the context
        frame = context['object']
        # Query the related experiences
        context['experiences'] = Experience.objects.filter(experiential_frame=frame)
        return context


class ExperienceDetailView(DetailView):
    model = Experience
    template_name = 'experiential/experience_detail.html'  # This warning is a lie. Pay no attention.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the current experience from the context
        experience = context['object']
        # Query the related authentic immersive experiences
        context['authentic_immersive_experiences'] = AuthenticImmersiveExperience.objects.filter(experience=experience)
        return context


class AuthenticImmersiveExperienceDetailView(DetailView):
    model = AuthenticImmersiveExperience
    template_name = 'experiential/authentic_immersive_experience_detail.html'  # This warning is a lie. Pay no attention.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aie = self.get_object()  # This will get the current AuthenticImmersiveExperience instance
        experience = aie.experience
        frame = experience.experiential_frame

        context['aie'] = aie  # Explicitly set aie
        context['experience'] = experience
        context['frame'] = frame
        context['lessons_learned'] = LessonLearned.objects.filter(aie_name=aie)

        return context


class AddLessonLearnedView(LoginRequiredMixin, CreateView):
    model = LessonLearned
    form_class = LessonLearnedForm
    template_name = 'experiential/add_lesson_learned.html'

    def form_valid(self, form):
        try:
            # Manually save the form to avoid trying to save twice
            self.object = form.save(commit=False)
            self.object.user = self.request.user

            # Set the associations
            self.object.experiential_frame = form.cleaned_data.get('experiential_frame')
            self.object.experience = form.cleaned_data.get('experience')
            self.object.aie_name = form.cleaned_data.get('aie_name')

            self.object.save()
            form.save_m2m()
            print('form validated')
            return redirect(self.get_success_url())
        except IntegrityError:
            form.add_error(None, "You can't submit the same lesson twice.")
            return self.form_invalid(form)

    def get_success_url(self):
        # Redirect to the detail view of the associated AuthenticImmersiveExperience
        return reverse_lazy('experiential:authentic_immersive_experience_detail',
                            kwargs={'pk': self.object.aie_name.pk})

    def get_form_kwargs(self):
        # This method is used to provide initial data and form options
        print('get_form_kwargs function initiated')
        kwargs = super(AddLessonLearnedView, self).get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            # Update the form's data with the POST data, which includes the selected experiential_frame
            kwargs['data'] = self.request.POST
        return kwargs

    def get_initial(self):
        print('get_initial function initiated')
        initial = super().get_initial()
        frame_id = self.kwargs.get('frame_id')
        experience_id = self.kwargs.get('experience_id')
        aie_id = self.kwargs.get('aie_id')

        if frame_id:
            initial['experiential_frame'] = frame_id
        if experience_id:
            initial['experience'] = experience_id
        if aie_id:
            initial['aie_name'] = aie_id

        return initial
