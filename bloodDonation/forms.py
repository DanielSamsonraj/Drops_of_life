# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from .models import donarDetails


# class ExtendedUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(required=True)

#     class Meta:
#         model = User
#         fields = ('username',
#                   'first_name',
#                   'email',
#                   'password1',
#                   'password2',
#                   )

#     def save(self, commit=True):
#         user = super(UserRegisterForm, self).save(commit=False)
#         user.first_name = self.cleaned_data['first_name']
#         user.email = self.cleaned_data['email']

#         if commit:
#             user.save()

#         return user
