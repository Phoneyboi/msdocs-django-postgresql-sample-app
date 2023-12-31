from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        success_url=reverse_lazy('accounts:profile')  # Correctly namespaced
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),

    path('signup/', views.SignUp.as_view(), name='signup'),

    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change_pass.html',
        success_url=reverse_lazy('accounts:password_change_done')
    ), name='change_password'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),

    path('profile/', views.profile, name='profile'),
]
