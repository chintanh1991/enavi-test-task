import requests
import json
import hashlib
import base64
from .models import installer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hmac
import datetime
from decouple import config

API_KEY = config('API_KEY')
SHARED_SECRET = config('SHARED_SECRET')
API_VERSION = config('API_VERSION') 
SCOPES = config('SCOPES')
APP_URL = config('APP_URL')



class WebhookApi(object):
    # shopify Uninstalling app webhook  functional code start #
    @csrf_exempt
    def webhook_uninstall(request):
        if request.method == 'POST':        # check that the request method is POST or not #
            if ((request.body != "") and (request.headers.get('X-Shopify-Hmac-Sha256') != "")):     # check 'request.body' and  'request.headers.get('X-Shopify-Hmac-Sha256')' is not blank #
                data = request.body
                tkn = ''
                shop_url = ''
                hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
                digest = hmac.new(SHARED_SECRET.encode('utf-8'), data, hashlib.sha256).digest() # create new hmac from gethered data (data, hashlib.sha256 and shared_secret) #
                computed_hmac = base64.b64encode(digest)    # encoded hmac that create above #

                if computed_hmac == hmac_header.encode('utf-8'):    # match hmac_header and computed_hmac then get the topic and shop_url #
                    topic = request.headers.get('X-Shopify-Topic')
                    shop_url = request.headers.get('X-Shopify-Shop-Domain')
                    if shop_url != "":      # check the 'shop_url' is not blank #
                        uninstallap = installer.objects.filter(shop=str(shop_url))  # 'installer' table data filter by 'shop_url' #
                        if uninstallap: # get the record then #
                                                   
                            uninstallap.delete()            # delete record from 'installer' table while 'shop_url' is match in data #    
                    else:
                        return HttpResponse("NO shop domain")
                else:
                    return HttpResponse("FALSE")
        return HttpResponse('Success')
    