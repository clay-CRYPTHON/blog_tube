from django.shortcuts import render

# Create your views here.

from ipware import get_client_ip
from admintion.models import AllIPs

def get_ip_info(request):
    context = {}
    ip, ip_routeble = get_client_ip(request)
    if ip is None:
        ip="0.0.0.0"
    else:
        if ip_routeble:
            ipv = "Public"
        else:
            ipv = "Private"
    context['ip'] = ip
    context['ipv'] = ipv
    try:
        if request.META['PATH_INFO']:
            context['path'] = request.META['PATH_INFO']
    except:
        pass
    try:
        if request.META['HTTP_SEC_CH_UA']:
            context['sec_ch_ua'] = request.META['HTTP_SEC_CH_UA']
    except:
        pass
    try:
        if request.META['HTTP_SEC_CH_UA_PLATFORM']:
            context['platform'] = request.META['HTTP_SEC_CH_UA_PLATFORM']
    except:
        pass
    try:
        if request.META['HTTP_USER_AGENT']:
            context['user_agent'] = request.META['HTTP_USER_AGENT']
    except:
        pass
    try:
        if request.META['HTTP_ACCEPT_LANGUAGE']:
            context['lang'] = request.META['HTTP_ACCEPT_LANGUAGE']
    except:
        pass
    try:
        if request.META['COMPUTERNAME']:
            context['comp_name'] = request.META['COMPUTERNAME']
    except:
        pass
    try:
        if request.META['PROCESSOR_ARCHITECTURE']:
            context['cpu_architecture'] = request.META['PROCESSOR_ARCHITECTURE']
    except:
        pass
    try:
        if request.META['PROCESSOR_IDENTIFIER']:
            context['cpu_identifier'] = request.META['PROCESSOR_IDENTIFIER']
    except:
        pass
    try:
        if request.META['PROCESSOR_LEVEL']:
            context['cpu_level'] = request.META['PROCESSOR_LEVEL']
    except:
        pass
    try:
        if request.META['REQUEST_METHOD']:
            context['method'] = request.META['REQUEST_METHOD']
    except:
        pass
    return context


def create_api(ip,request):
    new_ip = AllIPs.objects.create(ip=ip['ip'],ip_type=ip['ipv'])
    if ip['path']:
        new_ip.path = ip['path']
    try:
        if ip['sec_ch_ua']:
            new_ip.sec_ch_ua = ip['sec_ch_ua']
    except:
        pass
    try:
        if ip['platform']:
            new_ip.platform = ip['platform']
    except:
        pass
    try:
        if ip['user_agent']:
            new_ip.user_agent = ip['user_agent']
    except:
        pass
    try:
        if ip['lang']:
            new_ip.lang = ip['lang']
    except:
        pass
    try:
        if ip['comp_name']:
            new_ip.comp_name = ip['comp_name']
    except:
        pass
    try:
        if ip['cpu_architecture']:
            new_ip.cpu_architecture = ip['cpu_architecture']
    except:
        pass
    try:
        if ip['cpu_identifier']:
            new_ip.cpu_identifier = ip['cpu_identifier']
    except:
        pass
    try:
        if ip['cpu_level']:
            new_ip.cpu_level = ip['cpu_level']
    except:
        pass
    try:
        if ip['method']:
            new_ip.method = ip['method']
    except:
        pass
    if request.user.is_authenticated:
        new_ip.user = request.user

    new_ip.save()

def global_info(request):
    create_api(get_ip_info(request),request)
    context = { }
    return context
