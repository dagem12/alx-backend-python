#!/usr/bin/env python3
"""View for deleting user account."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def delete_user(request):
    """
    Allows a logged-in user to delete their own account.
    """
    user = request.user
    user.delete()
    return redirect('home')  # or any URL you prefer