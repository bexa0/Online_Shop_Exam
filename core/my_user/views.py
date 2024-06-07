from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from my_user.forms import RegisterForm


# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import RegisterSerializer


# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#
#         refresh = RefreshToken.for_user(user)
#         response_data = {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }
#         return Response(response_data, status=status.HTTP_201_CREATED)


class SignUpView(CreateView):
    template_name = 'my_user/sign_up.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('log_in')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('start_page')

        return super().get(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = 'my_user/log_in.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('start_page')


class UserLogoutView(LogoutView):
    template_name = 'my_user/log_out.html'
    next_page = reverse_lazy('start_page')


def profile_view(request):
    user = request.user
    context = {'user': user}

    return render(request, 'my_user/profile.html', context)

