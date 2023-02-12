from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib import messages
from .forms import LoginForm, UserCreateForm
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

User = get_user_model()


class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        # Deactivate account till it is confirmed
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        subject = 'Activate Your SocialApp account'
        message = render_to_string(
            'accounts/account_activation_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            }
        )
        user.email_user(subject, message)

        messages.success(self.request, 'Please Confirm your email to complete registration.')

        return super().form_valid(form)


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            print(uid)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            print('shit')

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_verified = True
            user.save()
            login(request, user)
            messages.success(request, 'Your account has been verified')
            return redirect('home')
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly it has already been used')
            return redirect('home')
