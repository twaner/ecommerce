from django.db import models

# Create your models here.


class MarketingMessageQueryset(models.QuerySet):
    def active(self):
        """
        Gets active MarketingMessages.
        :return: Active MarketingMessages.
        """
        return self.filter(active=True)

    def featured(self):
        """
        Gets featured MarketingMessages.
        :return: Featured MarketingMessages.
        """
        return self.filter(featured=True)


class MarketingMessageManager(models.Manager):
    def get_queryset(self):
        """
        Gets a queryset of MarketingMessages.
        :return: a queryset of MarketingMessages.
        """
        return MarketingMessageQueryset(self.model, using=self.db)

    def all(self):
        """
        Gets a queryset of all active MarketingMessages.
        :return: a queryset of all active MarketingMessages.
        """
        return self.get_queryset().active()

    def featured(self):
        """
        Gets and returns a queryset of MarketingMessages that are active and featured.
        :return: queryset of active and featured MarketingMessages.
        """
        return self.get_queryset().active().featured()

    def get_featured(self):
        """
        Gets the first featured MarketingMessage or returns None if no MarketingMessages are active.
        :return: A featured MarketingMessage or None
        """
        try:
            return self.featured().order_by("-start_date")[0]
        except:
            return None


class MarketingMessage(models.Model):
    message = models.CharField(max_length=120, blank=False, null=False)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    objects = MarketingMessageManager()
    # messages = MarketingMessageManager()

    def __str__(self):
        return str(self.message[:12])