# -*- coding: utf-8 -*-

import base64
import binascii
import datetime
import hashlib
import json
import logging
import os
import random
import subprocess
import time
import uuid
import zipfile

from django.conf import settings
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from .forms import KeyForm, KeyCreateForm
from .models import ActivationKey, Version

from keymanager import messages
from utils.exceptions import KeyHasBeenUsed, IllegalKey


LOG = logging.getLogger(__name__)
STANDARD_VERSION = 64
ENTERPRISE_VERSION = 96
PACKAGE_VERSION = 384
CODE_MAP = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
            'y', 'z', '0', '1', '2', '3', '4', '5',
            '6', '7', '8', '9', 'A', 'B', 'C', 'D',
            'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']


def index(request):
    template_name = 'keys/index.html'
    msg = ""
    messages.error(request, "123467456")
    try:
        if request.user.is_superuser:
            keys = ActivationKey.objects.all()
        else:
            query = {'deleted': 0,
                     'user_id': request.user.id}

            keys = ActivationKey.objects.filter(**query)
    except:
        keys = []
        msg = _("Unable to list keys")
        LOG.error("Unable to list keys")

    for key in keys:
        version_name = key.version
        if version_name == "standard":
            key.version = _("Standard")
        elif version_name == "enterprise":
            key.version = _("Enterprise")
        elif version_name == "package":
            key.version = _("Package")
        elif version_name == "package_enhanced":
            key.version = _("Package Enhanced")
        else:
            key.version = _("Unknown")

    paginator = Paginator(keys, settings.PAGE_SIZE)
    page = request.GET.get('page')
    try:
        keys = paginator.page(page)
    except PageNotAnInteger:
        keys = paginator.page(1)
    except EmptyPage:
        keys = paginator.page(paginator.num_pages)

    return render(request,
                  template_name,
                  {"keys": keys, "message": msg})


def generate_key(version, srv_limit, cpu_limit, company="N/A", user=None):
    # version_obj = Version.objects.get(id=version)
    if version.find("package") >= 0:
        srv_limit = 3
        cpu_limit = 6

    now = time.time()
    key = hashlib.sha224(str(now) +
             "".join(random.sample(CODE_MAP, 4))).hexdigest()[:40]
    check_field = str(binascii.crc32(key))[1:9]
    key = "%s%s" % (key, check_field)

    a_key = ActivationKey(id=str(uuid.uuid4()),
                          key=key,
                          version=version,
                          srv_limit=srv_limit,
                          cpu_limit=cpu_limit,
                          company=company,
                          user=user,
                          generation_time=datetime.datetime.utcnow())
    a_key.save()

    return key


def generate_keys(request):
    template_name = 'keys/generate_keys.html'
    keys = []
    key_form = KeyCreateForm()

    if request.method == "POST":
        key_form = KeyCreateForm(request.POST)
        if key_form.is_valid():
            version = request.POST['version']
            try:
                srv_limit = int(request.POST['srv_limit'].encode('utf-8'))
                cpu_limit = int(request.POST['cpu_limit'].encode('utf-8'))
            except:
                srv_limit = 3
                cpu_limit = 6
            company = request.POST['company']
            count = int(request.POST['count'].encode("utf-8"))

            for c in range(count):
                keys.append(generate_key(version,
                                         srv_limit,
                                         cpu_limit,
                                         company,
                                         request.user))

    return render(request, template_name, {"keys": keys,
                                           "key_form": key_form})


# not used
def edit_version(request, key_id):
    template_name = 'keys/update_key.html'
    msg = ""

    try:
        key_obj = ActivationKey.objects.get(id=key_id)
    except:
        msg = _("Unable to get key(%s)") % key_id
    key_form = KeyForm(initial={"version": key_obj.version.id,
                                "company": key_obj.company})

    if request.method == "POST":
        key_form = KeyForm(request.POST)
        if key_form.is_valid():
            key_obj.version = Version.objects.get(id=request.POST['version'])
            key_obj.company = request.POST['company']
            key_obj.save()
            msg = _("Successfully update key.")
            LOG.info("Successfully update key.")

    return render(request, template_name, {"key_id":key_id,
                                           "key_form": key_form,
                                           "message": msg})


def download_key_file(request, key_id):
    template_name = 'keys/download_key.html'
    msg = ""

    if request.method == "POST":
        src_hd_info = request.POST['hd_info'].strip()
        act_key = ActivationKey.objects.get(id=key_id)

        version = act_key.version
        if version == "standard":
            vmemory_limit = STANDARD_VERSION * act_key.cpu_limit
        elif version == "enterprise":
            vmemory_limit = ENTERPRISE_VERSION * act_key.cpu_limit
        elif version.find("package") >= 0:
            vmemory_limit = PACKAGE_VERSION
        else:
            vmemory_limit = 0

        key = act_key.key
        version_name = "".join(random.sample(CODE_MAP, 15)) + \
                       base64.b64encode(act_key.version) + \
                       "".join(random.sample(CODE_MAP, 10))
        version_sv = "".join(random.sample(CODE_MAP, 15)) + \
                     base64.b64encode(str(act_key.srv_limit)) + \
                     "".join(random.sample(CODE_MAP, 10))
        version_vl = "".join(random.sample(CODE_MAP, 15)) + \
                     base64.b64encode(str(vmemory_limit*1024)) + \
                     "".join(random.sample(CODE_MAP, 10))
        hd_info = hashlib.sha224(src_hd_info).hexdigest()

        key_info = os.linesep.join([hd_info, version_name,
                                    version_sv, version_vl, key])
        check_sum = str(binascii.crc32(key_info))
        key_info = os.linesep.join([key_info,
                                    hashlib.sha224(check_sum).hexdigest()])
        key_begin = "===================== LICENSE BEGIN ===================="
        key_end = "====================== LICENSE END ====================="
        key_info = os.linesep.join([key_begin, key_info, key_end])
        # temp_file_path = "/tmp/%s.zip" % "".join(random.sample(CODE_MAP, 10))

        try:
            # write key to zip file,  zipfile cannot set password
            # act_file = zipfile.ZipFile(temp_file_path,
            #                            'w',
            #                            zipfile.ZIP_DEFLATED)
            # act_file.writestr('.key', key_info)
            # act_file.setpassword(str(binascii.crc32(src_hd_info)))
            # act_file.close()

            # write key to zip file , use 7z to set password
            # subprocess.call('echo "%s" | 7z a %s -tgzip -p%s -y -si.key' %
            #                 (key_info, temp_file_path,
            #                  str(binascii.crc32(src_hd_info))), shell=True)

            # create temp folder & files
            hd_checksum = str(binascii.crc32(src_hd_info))
            temp_folder = "/tmp/.%s%s" % \
                          (hd_checksum, "".join(random.sample(CODE_MAP, 5)))
            os.mkdir(temp_folder)
            temp_key_file = "%s/.key" % temp_folder
            temp_file_path = "%s/temp_key.zip" % temp_folder

            with open(temp_key_file, 'w') as f:
                f.write(key_info)

            subprocess.call("7z a %s -tzip -p%s -y %s" %
                            (temp_file_path, hd_checksum, temp_key_file), shell=True)

            with open(temp_file_path, 'rb') as f:
                content = f.read()

            # remove temp files
            os.remove(temp_key_file)
            os.remove(temp_file_path)
            os.rmdir(temp_folder)

            # update database
            act_key.used += 1
            act_key.machine_code = src_hd_info
            act_key.activation_time = datetime.datetime.now()
            act_key.save()

            response = HttpResponse()
            response['Content-Disposition'] = 'attachment; filename="key.data"'
            response['Content-Type'] = 'application/octet-stream'
            response.write(content)

            return response
        except:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            msg = "Unable to download activation file."
            LOG.error(msg)

    return render(request, template_name, {"key_id":key_id,
                                           "message": msg})

def delete(request, key_id):
    try:
        act_key = ActivationKey.objects.get(id=key_id)
        if request.user.is_superuser:
            act_key.delete()
        elif request.user.id == act_key.user.id:
            act_key.deleted = 1
            act_key.save()
        else:
            return render(request, "403.html")
        return redirect(reverse('keys:index'))
    except:
        msg = "Unable to delete key(%s)" % key_id.encode("utf-8")
        LOG.error(msg)
        return redirect(reverse('keys:index'))


def reuse(request, key_id):
    try:
        key_obj = ActivationKey.objects.get(id=key_id)
        if key_obj.used > 0:
            key_obj.used -= 1
            key_obj.save()
            LOG.info("reuse key(%s) ,current usage count %s." %
                     (key_id, key_obj.used))
    except:
        msg = _("Unable to get key(%s)") % key_id
        LOG.error(msg)

    return redirect(reverse('keys:index'))


def use_key(request):
    key = request.GET.get('activation_key', "")
    host = request.META.get("REMOTE_ADDR", "unknown")

    try:
        real_key = base64.b64decode(key[1:])
    except:
        msg = 'key"%(key)s" at host"%(host)s" : Illegal key' % \
              {"key": key, "host": host}
        LOG.error(msg)
        return HttpResponse("error")

    try:
        key_obj = ActivationKey.objects.get(key=real_key)
        if key_obj:
            key_obj.used += 1
            key_obj.activation_time = datetime.datetime.now()
            key_obj.save()
            LOG.info("use key(%s) from host (%s),current usage count %s." %
                     (real_key, host, key_obj.used))
            return HttpResponse("ok")

        return HttpResponse("error")
    except:
        return HttpResponse("error")


def key_available(request):
    key = request.GET.get('activation_key', "")
    host = request.META.get("REMOTE_ADDR", "unknown")

    try:
        real_key = base64.b64decode(key[1:])
    except:
        msg = 'key"%(key)s" at host"%(host)s" : Illegal key' % \
              {"key": key, "host": host}
        LOG.error(msg)
        return HttpResponse(json.dumps({"available": "N",
                                        "message": "Illegal Key"}))

    try:
        key_obj = ActivationKey.objects.filter(key=real_key)
        if key_obj:
            key_obj = key_obj[0]
            if key_obj.used == 0:
                version = key_obj.version
                ky = random.choice(CODE_MAP) + \
                     base64.b64encode(version.name.encode("utf-8"))
                vl = random.choice(CODE_MAP) + \
                     base64.b64encode(str(version.vmemory_limit))
                sl = random.choice(CODE_MAP) + \
                     base64.b64encode(str(version.server_limit))

                LOG.info("available key(%s) from host(%s)." %
                         (real_key, host))
                return HttpResponse(json.dumps({"available": "Y",
                                                "used": "0",
                                                "vn": {
                                                    "ky": ky,
                                                    "vl": vl,
                                                    "sl": sl},
                                                "message": "OK"}))
            raise KeyHasBeenUsed
        raise IllegalKey
    except KeyHasBeenUsed:
        msg = 'key"%(key)s" at host"%(host)s" : Key has been used.' % \
              {"key": key, "host": host}
        LOG.error(msg)
        return HttpResponse(json.dumps({"available": "Y",
                                        "used": "Y",
                                        "message": "Key has been used"}))
    except IllegalKey:
        msg = 'key"%(key)s" at host"%(host)s" : Unable to find' \
              ' the corresponding records from the database.' % \
              {"key": key, "host": host}
        LOG.error(msg)
        return HttpResponse(json.dumps({"available": "N",
                                        "message": "Key not found"}))
    except:
        msg = 'key"%(key)s" at host"%(host)s" : Unknown error' % \
              {"key": key, "host": host}
        LOG.error(msg)
        return HttpResponse(json.dumps({"available": "N",
                                        "message": "Unknown error"}))


def deactivate(request):
    key = request.GET.get('activation_key', "")
    host = request.META.get("REMOTE_ADDR", "unknown")

    try:
        real_key = base64.b64decode(key[1:])
    except:
        msg = 'key"%(key)s" at host"%(host)s" : Illegal key' % \
              {"key": key, "host": host}
        LOG.error(msg)
        return HttpResponse("error")

    try:
        key_obj = ActivationKey.objects.get(key=real_key)
        key_obj.used = 0
        key_obj.save()
        LOG.info("deactivate key(%s) from host(%s)." % (real_key, host))
        return HttpResponse("ok")
    except:
        return HttpResponse("error")
