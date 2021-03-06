from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View

from recipes.mixins import MainMixin
from recipes.models import Recipe

from .forms import ProfileForm, SignUpForm
from .models import get_user_model


class ProfileView(MainMixin, View):
    template = 'profile.html'
    tab = 'profile'
    profile = True

    def get(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        self.title = user.get_full_name()
        self.queryset = Recipe.objects.filter(author=user)
        return super().get(request)


class EditProfileView(MainMixin, View):
    template = 'profile_form.html'

    def get(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        if request.user != user:
            return redirect('profile', user)
        form = ProfileForm(instance=user)
        return render(request, 'edit_profile.html', context={'form': form})

    def post(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        if request.user != user:
            return redirect('profile', user)
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user)
        return render(request, 'edit_profile.html', context={'form': form})


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
