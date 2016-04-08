import logging
import random
import uuid

from django.conf import settings
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from .forms import VersionForm
from .models import Version
from utils.filters import require_superuser

from managers.keys.views import CODE_MAP


LOG = logging.getLogger(__name__)


@require_superuser
def index(request):
    template_name = "versions/index.html"
    msg = ""

    try:
        versions = Version.objects.filter(deleted=0)
    except:
        msg = _("Unable to list versions")
        LOG.error("Unable to list versions")

    paginator = Paginator(versions, settings.PAGE_SIZE)
    page = request.GET.get('page')

    try:
        versions = paginator.page(page)
    except PageNotAnInteger:
        versions = paginator.page(1)
    except EmptyPage:
        versions = paginator.page(paginator.num_pages)

    return render(request, template_name, {"versions": versions,
                                           "message": msg})


@require_superuser
def create(request):
    template_name = "versions/create.html"
    msg = ""
    version_form = VersionForm()

    if request.method == "POST":
        version_form = VersionForm(request.POST)
        if version_form.is_valid():
            try:
                version = Version(id=str(uuid.uuid4()),
                                  key="".join(random.sample(CODE_MAP, 2)),
                                  name=request.POST['name'],
                                  vmemory_limit=
                                    int(request.POST['vmemory_limit']) * 1024,
                                  server_limit=request.POST['server_limit'])
                version.save()
                msg = _('Success create version "%s"') % \
                      request.POST['name'].encode("utf-8")
                LOG.info('Success create version "%s"' %
                         request.POST['name'].encode("utf-8"))
            except:
                msg = _('Unable to create version.')
                LOG.error('Unable to create version.')

    return render(request, template_name, {"version_form": version_form,
                                           "message": msg})


@require_superuser
def delete(request, version_id):
    try:
        version = Version.objects.get(id=version_id)
        version.deleted = 1
        version.save()
    except:
        msg = "Unable to delete version(%s)." % version_id
        LOG.error(msg)

    return redirect(reverse('versions:index'))
