from django.contrib import messages as _messages
from django.contrib.messages import constants
from django.utils.encoding import force_unicode
from django.utils.safestring import SafeData  # noqa


def add_message(request, level, message, extra_tags='', fail_silently=False):
    """Attempts to add a message to the request using the 'messages' app."""
    if request.is_ajax():
        tag = constants.DEFAULT_TAGS[level]
        # if message is marked as safe, pass "safe" tag as extra_tags so that
        # client can skip HTML escape for the message when rendering
        if isinstance(message, SafeData):
            extra_tags = extra_tags + ' safe'
        request.horizon['async_messages'].append([tag,
                                                  force_unicode(message),
                                                  extra_tags])
    else:
        return _messages.add_message(request, level, message,
                                     extra_tags, fail_silently)


def debug(request, message, extra_tags='', fail_silently=False):
    """Adds a message with the ``DEBUG`` level."""
    add_message(request, constants.DEBUG, message, extra_tags=extra_tags,
                fail_silently=fail_silently)


def info(request, message, extra_tags='', fail_silently=False):
    """Adds a message with the ``INFO`` level."""
    add_message(request, constants.INFO, message, extra_tags=extra_tags,
                fail_silently=fail_silently)


def success(request, message, extra_tags='', fail_silently=False):
    """Adds a message with the ``SUCCESS`` level."""
    add_message(request, constants.SUCCESS, message, extra_tags=extra_tags,
                fail_silently=fail_silently)


def warning(request, message, extra_tags='', fail_silently=False):
    """Adds a message with the ``WARNING`` level."""
    add_message(request, constants.WARNING, message, extra_tags=extra_tags,
                fail_silently=fail_silently)


def error(request, message, extra_tags='', fail_silently=False):
    """Adds a message with the ``ERROR`` level."""
    add_message(request, constants.ERROR, message, extra_tags=extra_tags,
                fail_silently=fail_silently)