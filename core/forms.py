from django import forms
from .models import Feedback
from django.utils.translation import gettext_lazy as _

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-outline-variant/30 bg-transparent px-5 py-4 placeholder:text-on-surface-variant/60 focus:border-primary focus:ring-1 focus:ring-primary transition-colors mb-2', 
                'placeholder': _('Your Name (Optional)')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full rounded-xl border border-outline-variant/30 bg-transparent px-5 py-4 placeholder:text-on-surface-variant/60 focus:border-primary focus:ring-1 focus:ring-primary transition-colors mb-2', 
                'placeholder': _('Your Email (Optional)')
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full rounded-xl border border-outline-variant/30 bg-transparent px-5 py-4 placeholder:text-on-surface-variant/60 focus:border-primary focus:ring-1 focus:ring-primary transition-colors min-h-[120px]', 
                'placeholder': _('Your Message *'), 
                'required': 'required'
            }),
        }
        labels = {
            'name': '',
            'email': '',
            'message': '',
        }
