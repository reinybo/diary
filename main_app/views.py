from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Entry, Photo
import uuid
import boto3
import os



def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')

@login_required
def entries_index(request):
    entries = Entry.objects.filter(user=request.user)
    return render(request,'entries/index.html', { 'entries': entries })

class EntryCreate(LoginRequiredMixin, CreateView):
    model = Entry
    fields = ['title', 'date', 'content']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



@login_required
def entry_detail(request, entry_id):
  entry = Entry.objects.get(id=entry_id)
  return render(request, 'entries/detail.html', { 'entry': entry })


class EntryUpdate(LoginRequiredMixin, UpdateView):
  model = Entry
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['title', 'date', 'content']

class EntryDelete(LoginRequiredMixin, DeleteView):
  model = Entry
  success_url = '/entries/'




def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)



import os
import environ

env = environ.Env()
environ.Env.read_env()


BUCKET = os.environ['S3_BUCKET']
S3_BASE_URL = os.environ['S3_BASE_URL']

@login_required
def add_photo(request, entry_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, entry_id=entry_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', entry_id=entry_id)