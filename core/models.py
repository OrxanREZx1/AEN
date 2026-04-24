from django.db import models
from django.utils.translation import gettext_lazy as _

class Feedback(models.Model):
    name = models.CharField(_("Name"), max_length=150, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    message = models.TextField(_("Message"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name or _('Anonymous')} - {self.email or _('No email')}"
