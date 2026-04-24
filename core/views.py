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
            
            # Send Email
            try:
                subject = "New AEN Feedback Submission"
                message_body = (
                    f"New feedback received on AEN Landing Page.\n\n"
                    f"Name: {feedback.name or 'Not Provided'}\n"
                    f"Email: {feedback.email or 'Not Provided'}\n"
                    f"Message:\n{feedback.message}\n\n"
                    f"Submitted at: {feedback.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                send_mail(
                    subject,
                    message_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.FEEDBACK_RECEIVER_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Failed to send feedback email: {e}")

            messages.success(request, _('Your message has been sent successfully!'))
            return redirect('core:home')
        else:
            messages.error(request, _('There was an error with your submission. Please check the form.'))
    else:
        form = FeedbackForm()
    
    return render(request, 'home.html', {'form': form})
