__author__ = 'taiowawaner'
import datetime
from django.utils import timezone
from .models import MarketingMessage

time_format = "%Y-%m-%d %H:%M:%S"


def is_offset_greater(time_string_offset):
    """
    Verifies if the now() time is greater than the offset time.
    Formats time strings into datetime format that are timezone aware.
    :param time_string_offset: offset time.
    :return: Boolean
    """
    time1 = str(timezone.now())[:19] # remove extra numbers
    # time1[:time1.find('.')].replace('.','') without hardcoding
    offset_time = time_string_offset[:19]  # to remove extra numbers
    offset_time_formatted = datetime.datetime.strptime(offset_time, time_format)
    offset_time_tz_aware = timezone.make_aware(offset_time_formatted, timezone.get_default_timezone())
    now_time_formatted = datetime.datetime.strptime(time1, time_format)
    now_time_tz_aware = timezone.make_aware(now_time_formatted, timezone.get_default_timezone())
    print("nowtz {0}\noffsettz {1}\nresult {2}".format(now_time_tz_aware, offset_time_tz_aware, now_time_tz_aware > offset_time_tz_aware))
    return now_time_tz_aware > offset_time_tz_aware


class DisplayMarketingMessage():
    def process_request(self, request):
        try:
            message_offset = request.session["dismiss_message_for"] # String
        except:
            message_offset = None

        try:
            # request.session['marketing_message'] = MarketingMessage.objects.get_featured().message
            marketing_message = MarketingMessage.objects.get_featured().message

        except:
            marketing_message = False
        # if message exists, and offset is not None and greater than now()
        if message_offset is None:
            request.session['marketing_message'] = marketing_message
        elif message_offset is not None and is_offset_greater(message_offset):
            request.session['marketing_message'] = marketing_message
        else:
            try:
                del request.session['marketing_message']
            except:
                pass
