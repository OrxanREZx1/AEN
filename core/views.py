from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.conf import settings
from .forms import FeedbackForm
import logging

logger = logging.getLogger(__name__)

def home(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            
            try:
                send_mail(
                    subject="New AEN Feedback",
                    message=f"Name: {feedback.name}\nEmail: {feedback.email}\nMessage: {feedback.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.FEEDBACK_RECEIVER_EMAIL],
                    fail_silently=False
                )
            except Exception as e:
                print("EMAIL ERROR:", e)

            messages.success(request, _('Your message has been sent successfully!'))
            return redirect('core:home')
        else:
            messages.error(request, _('There was an error with your submission. Please check the form.'))
    else:
        form = FeedbackForm()
    
    return render(request, 'home.html', {'form': form})
