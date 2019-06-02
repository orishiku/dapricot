import hmac
import requests
import os
import stat

from ipaddress import ip_address, ip_network
from hashlib import sha1

from django.http import HttpResponse, HttpResponseForbidden,HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils.encoding import force_bytes

from django.core.management import call_command
import subprocess

@require_POST
@csrf_exempt
def hello(request):
    # Verify if request came from GitHub
    forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR'))
    client_ip_address = ip_address(forwarded_for)
    whitelist = requests.get('https://api.github.com/meta').json()['hooks']

    for valid_ip in whitelist:
        if client_ip_address in ip_network(valid_ip):
            break
    else:
        return HttpResponseForbidden('Permission denied.')
    
# Verify the request signature
    header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    if header_signature is None:
        return HttpResponseForbidden('Permission denied.')

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        return HttpResponseServerError('Operation not supported.', status=501)

    mac = hmac.new(force_bytes(settings.GITHUB_WEBHOOK_KEY), msg=force_bytes(request.body), digestmod=sha1)
    if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
        return HttpResponseForbidden('Permission denied.')
    
    # Process the GitHub events
    event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')
    '''
    if event == 'ping':
        return HttpResponse('pong')
    elif event == 'push':
        update_script = os.path.join(os.path.dirname(settings.ROOT_DIR),'update.sh')
            
        subprocess.Popen("sh {0} -p {1} -a {2}".format(update_script,
                                                    settings.ROOT_DIR,
                                                    'release/alpha'),
                        stdout=subprocess.PIPE, 
                        shell=True, 
                        stderr=subprocess.STDOUT)
        
        return HttpResponse('success')
        '''

    # In case we receive an event that's neither a ping or push
    return HttpResponse(status=204)