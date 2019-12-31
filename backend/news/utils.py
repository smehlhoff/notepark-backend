import datetime
import re

import math
from django.utils.html import strip_tags


def get_word_count(html_string):
    word_string = strip_tags(html_string)
    count = len(re.findall(r'\w+', word_string))

    return count


# Based on the average reading speed of an adult (roughly 275 WPM)
def get_read_time(html_string):
    count = get_word_count(html_string)
    read_time_min = math.ceil((count / 275.0))
    read_time = str(datetime.timedelta(minutes=read_time_min))

    return read_time
