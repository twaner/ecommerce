import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.


class MarketingQueryset(models.QuerySet):
    def active(self):
        """
        Gets active MarketingMessages.
        :return: Active MarketingMessages.
        """
        return self.filter(active=True)

    def featured(self):
        """
        Gets a featured MarketingMessages. Filters by start_date lt now and end_date gte now using the timezone as datetime.
        :return: Featured MarketingMessages.
        """
        return self.filter(featured=True).filter(start_date__lt=timezone.now()) \
            .filter(end_date__gte=timezone.now())


class MarketingManager(models.Manager):
    def get_queryset(self):
        """
        Gets a queryset of MarketingMessages.
        :return: a queryset of MarketingMessages.
        """
        return MarketingQueryset(self.model, using=self.db)

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
        Uses the Model's queryset featured method to get the first featured MarketingMessage that meets the criteria.
        :return: A featured MarketingMessage or None
        """
        try:
            return self.featured()[0]
        except:
            return None


class MarketingBase(models.Model):
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        abstract = True


class MarketingMessage(MarketingBase):
    message = models.CharField(max_length=120, blank=False, null=False)
    # active = models.BooleanField(default=False)
    # featured = models.BooleanField(default=False)
    # timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    # updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    # start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    # end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        ordering = ["-start_date", "-end_date"]

    objects = MarketingManager()
    # messages = MarketingManager()

    def __str__(self):
        return str(self.message[:12])


def slider_upload(instance, filename):
    return "images/slider/{0}".format(str(filename))  #can add str(instance.user)


class Slider(MarketingBase):
    image = models.ImageField(upload_to=slider_upload)
    header_text = models.CharField(max_length=120, blank=True, null=True)
    text = models.CharField(max_length=120, blank=True, null=True)
    order = models.IntegerField(default=0)
    # active = models.BooleanField(default=False)
    # featured = models.BooleanField(default=False)
    # timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    # updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    # start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    # end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        ordering = ["order", "-start_date", "-end_date"]

    objects = MarketingManager()

    def __str__(self):
        return str(self.image)

    def get_image_url(self):
        return "{0}/{1}".format(settings.MEDIA_URL, self.image)