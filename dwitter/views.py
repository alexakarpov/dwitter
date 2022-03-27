# dwitter/views.py

from django.shortcuts import render, redirect
from .models import Profile
from .forms import DweetForm

def dashboard(request):
  form = DweetForm(request.POST or None)
  if request.method == "POST":
    if form.is_valid():
      print("form is valid")
      dweet = form.save(commit=False)
      dweet.user = request.user
      dweet.save()
      return redirect("dwitter:dashboard")
    else:
      print("form not valid")

  follows = request.user.profile.follows.all()
  sorted_dweets = []
  for f in follows:
    sorted_dweets.extend(list(f.user.dweets.all()))
  sorted_dweets.sort(key=lambda d: d.created_at, reverse=True)
  return render(request,
                "dwitter/dashboard.html",
                {
                 'dweets': sorted_dweets,
                 'form': form
                })

def profiles(request):
  profiles = Profile.objects.exclude(user=request.user)
  return render(request, "dwitter/profiles.html", {"profiles": profiles})

def profile(request, pk):
  if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

  profile = Profile.objects.get(pk=pk)

  if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()

  return render(request, "dwitter/profile.html", {"profile": profile})
