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
            
            import threading

            def send_feedback_email_bg(fb):
                try:
                    subject = "New AEN Feedback Submission"
                    message_body = (
                        f"New feedback received on AEN Landing Page.\n\n"
                        f"Name: {fb.name or 'Not Provided'}\n"
                        f"Email: {fb.email or 'Not Provided'}\n"
                        f"Message:\n{fb.message}\n\n"
                        f"Submitted at: {fb.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    send_mail(
                        subject,
                        message_body,
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.FEEDBACK_RECEIVER_EMAIL],
                        fail_silently=True,
                    )
                except Exception as e:
                    logger.error(f"Failed to send feedback email: {e}")

            # Send Email in background to prevent Railway worker timeout
            threading.Thread(target=send_feedback_email_bg, args=(feedback,)).start()

            messages.success(request, _('Your message has been sent successfully!'))
            return redirect('core:home')
        else:
            messages.error(request, _('There was an error with your submission. Please check the form.'))
    else:
        form = FeedbackForm()
    
    return render(request, 'home.html', {'form': form})
