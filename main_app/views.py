from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Job, Token, JobApplication
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .jobs import jobs

class TokenGenerator(PasswordResetTokenGenerator):
    pass

account_activation_token = TokenGenerator()

class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

def delete_user_keys(dict):
    list = [
        'is_superuser',
        'password',
        'is_staff',
        'groups',
        'user_permissions'
    ]
    for key in list:
        del dict[key]
    return dict

def build_job(job):
    dict = {
        'id': None,
        'title': '',
        'company': '',
        'location': '',
        'description': '',
        'requirements': '',
        'salary': '',
        'recruiter': None
    }

    for key in model_to_dict(job):
        dict[key] = model_to_dict(job)[key]

    recruiter = User.objects.get(id=job.recruiter_id)
    dict['recruiter'] = delete_user_keys(model_to_dict(recruiter))
    return dict

def create_jobs_list(jobs):
    jobs_list = []

    for job in jobs:
        jobs_list.append(build_job(job))

    return jobs_list

def get_job_dict(job):
    return build_job(job)

def index(request):
    jobs = Job.objects.all()
    jobs_list = create_jobs_list(jobs)
    return JsonResponse({'data': jobs_list}, safe=False)

def show(request, job_id):
    job = Job.objects.get(id=job_id)
    job_dict = get_job_dict(job)
    return JsonResponse({'data': job_dict}, safe=False)

@csrf_exempt
def create_job(request, user_id):
    print(request.POST)
    job = Job.objects.create(
        title=request.POST['title'],
        company=request.POST['company'],
        location=request.POST['location'],
        description=request.POST['description'],
        requirements=request.POST['requirements'],
        salary=request.POST['salary'],
        recruiter_id=user_id
    )
    job_dict = get_job_dict(job)
    return JsonResponse({'data': job_dict}, safe=False)

@csrf_exempt
def create(request):
    for job in jobs:
        Job.objects.create(
            title=job['title'],
            company=job['company'],
            location=job['location'],
            description=job['description'],
            requirements=job['requirements'],
            salary=job['salary']
        )
    return JsonResponse({'response': 200}, safe=False)

@csrf_exempt
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = account_activation_token.make_token(user)
            Token.objects.create(user=user, key=token)
            login(request, user)
            del model_to_dict(user)['password']
            return JsonResponse({'token': token, 'user': model_to_dict(user)}, safe=False)
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    return JsonResponse({'data': error_message}, safe=False)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        token = account_activation_token.make_token(user)
        Token.objects.create(user=user, key=token)
        login(request, user)
        user = delete_user_keys(model_to_dict(user))
        return JsonResponse({'token': token, 'user': user}, safe=False)

@csrf_exempt
def logout(request, user_id):
     Token.objects.filter(user_id=user_id).delete()
     return JsonResponse({'status': 200})

def get_user_from_token(request):
    token = request.GET.get('token')
    token_obj = Token.objects.get(key=token)
    user = token_obj.user
    user = delete_user_keys(model_to_dict(user))
    return JsonResponse({'data': user}, safe=False)

@csrf_exempt
def apply_to_job(request, user_id, job_id):
    job_application = JobApplication.objects.create(
        user_id = user_id,
        job_id = job_id,
        portfolio_link = request.POST['portfolio_link'],
        github_link = request.POST['github_link'],
        deployed_link = request.POST['deployed_link']
    )
    return JsonResponse({ 'data': model_to_dict(job_application) })

def get_application(request, user_id, job_id):
    job_application = JobApplication.objects.get(user_id=user_id, job_id=job_id)
    return JsonResponse({ 'data': model_to_dict(job_application) })