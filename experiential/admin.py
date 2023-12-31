from django.contrib import admin
from experiential.models import ExperientialFrame, Experience, AuthenticImmersiveExperience, LessonLearned


# Register your models here.

class ExperientialFrameAdmin(admin.ModelAdmin):
    pass

class ExperienceAdmin(admin.ModelAdmin):
    pass

class AuthenticImmersiveExperienceAdmin(admin.ModelAdmin):
    pass

class LessonLearnedAdmin(admin.ModelAdmin):
    pass


admin.site.register(ExperientialFrame, ExperientialFrameAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(AuthenticImmersiveExperience, AuthenticImmersiveExperienceAdmin)
admin.site.register(LessonLearned, LessonLearnedAdmin)
