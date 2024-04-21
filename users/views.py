import secrets
import random

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, FormView, UpdateView
from django.urls import reverse_lazy, reverse
from django.conf import settings

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register_form.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        url = self.request.build_absolute_uri(reverse('users:email-confirm', kwargs={'token': token}))
        send_mail(
            subject="Подтверждение почты",
            message=f"Здравствуйте.\nДля подтверждения почты перейдите по ссылке ниже:\n{url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class EmailForm(forms.Form):
    email = forms.EmailField(label='Email')


class PasswordResetView(FormView):
    template_name = 'users/password_reset.html'
    form_class = EmailForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        new_password = ''.join(random.choices(settings.PASSWORD_CHARS, k=settings.PASSWORD_LENGTH))

        user = get_user_model().objects.get(email=email)
        user.password = make_password(new_password)
        user.save()

        send_mail(
            'Восстановление пароля',
            f'Ваш новый пароль: {new_password}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user
