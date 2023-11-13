from django.conf import settings


def blogcp(request):
    return {
        'title': settings.TITLE,
    }