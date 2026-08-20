from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ProfileForm


@login_required
def settings_view(request):

    user = request.user

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your profile has been updated successfully!"
            )

            return redirect("settings")

    else:

        form = ProfileForm(
            instance=user
        )

    return render(
        request,
        "user_settings/settings.html",
        {
            "form": form,
            "user": user,
        }
    )