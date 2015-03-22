__author__ = 'taiowawaner'
import datetime
from django.utils import timezone
from .models import MarketingMessage


class DisplayMarketingMessage():
    def process_request(self, request):
        print(timezone.now() + datetime.timedelta(hours=8))
        print(timezone.now())
        try:
            request.session['marketing_message'] = MarketingMessage.objects.get_featured().message
            # print("DisplayMarketingMessage {0}".format(MarketingMessage.objects.get_featured().message))
        except:
            # print("DisplayMarketingMessage EXCEPT")
            request.session['marketing_message'] = False
