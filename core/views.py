from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from .forms import FeedbackForm
import os
import resend
import logging

logger = logging.getLogger(__name__)

def home(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            
            try:
                resend.api_key = os.getenv("RESEND_API_KEY")
                resend.Emails.send({
                    "from": os.getenv("DEFAULT_FROM_EMAIL"),
                    "to": [os.getenv("FEEDBACK_RECEIVER_EMAIL")],
                    "subject": "New AEN Feedback",
                    "html": f"""
                        <p><strong>Name:</strong> {feedback.name}</p>
                        <p><strong>Email:</strong> {feedback.email}</p>
                        <p><strong>Message:</strong> {feedback.message}</p>
                    """
                })
            except Exception as e:
                print("RESEND ERROR:", e)

            messages.success(request, _('Your message has been sent successfully!'))
            return redirect('core:home')
        else:
            messages.error(request, _('There was an error with your submission. Please check the form.'))
    else:
        form = FeedbackForm()
    
    return render(request, 'home.html', {'form': form})
