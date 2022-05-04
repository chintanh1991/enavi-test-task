from django.shortcuts import render
import requests
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect as redc
from .models import installer,product_detailmst
from django.core.paginator import Paginator
from decouple import config


API_KEY = config('API_KEY')
SHARED_SECRET = config('SHARED_SECRET')
API_VERSION = config('API_VERSION') 
SCOPES = config('SCOPES')
APP_URL = config('APP_URL')

# Create your views here.
shop = ""
get_tkn = ""

@xframe_options_exempt
@csrf_exempt 
def search_product_list(request):
    if request.method == "POST":
        sl_product_list = list()
        sl_product_dict = dict()
        product_name = request.POST['get_product']
        if product_name:
            get_products= product_detailmst.objects.filter(shop=shop,product_title__contains = product_name)
            if get_products:
                li_srnumber = 0
                shop_name = get_products[0].shop
                for m in get_products:
                    batch_code = ''
                    document_link = ''
                    chake_document = product_detailmst.objects.filter(id = m.id)
                    if chake_document:
                        li_srnumber += 1 
                        sub_dict = {
                            'shop' : m.shop,
                            'variant_id' : m.variant_id,
                            'product_id' : m.product_id,
                            'product_title' : m.product_title,
                            'product_img' : m.product_img,
                            'status' : m.status,
                            'sr_number' :li_srnumber,
                        }
                        sl_product_list.append(sub_dict)
                    sl_product_dict['search_product_doc'] = sl_product_list
                    paginator = Paginator(sl_product_dict['search_product_doc'],10)
                    page = request.GET.get('page')
                    pr_detail = paginator.get_page(page)   
                return render(request, 'base.html',{"product":pr_detail,"search_term":product_name})
            else:
                return HttpResponseRedirect('products_list')
        else:
            return HttpResponseRedirect('products_list')



@xframe_options_exempt
def products_list(request):
    if request.method == "GET":
        product_list = list()
        product_dict = dict()
        
        from .apis import APIS
        product_detail = APIS.get_products(shop=shop, token=get_tkn)
        count=0
        # print(product_detail)
        for p in product_detail['products']:
            for x in p:
                image_link = ""
                var_title = ""
                for y in x['variants']:
                    check_product_variants = product_detailmst.objects.filter(shop=shop,variant_id =y['id'])
                    if check_product_variants:
                        continue
                    else:
                        if (x['image'] != '' and x['image'] is not None):
                            image_link = x['image']['src']
                        else:
                            image_link = "https://3itest8.pagekite.me/media/noimage-available.jpg"
                        if y['title'] == "Default Title":
                            var_title = " "
                        else:
                            var_title = " - " + y['title']
                        product_detailmst.objects.create(shop=shop,product_img=str(image_link),variant_id =y['id'],product_id=x['id'],status= x['status'],product_title=x['title'])
                        break
        sr_number = 0            
        product_dtail = product_detailmst.objects.all()
        if product_dtail:
            chake_detail = product_detailmst.objects.filter(shop=shop)
            for z in chake_detail:
                sr_number += 1
                sub_dict = {
                    'shop' : z.shop,
                    'variant_id' : z.variant_id,
                    'product_id' : z.product_id,
                    'product_title' : z.product_title,
                    'product_img' : str(z.product_img),
                    'status' : z.status,
                    'sr_number' :sr_number,
                }
                product_list.append(sub_dict)
        product_dict['product_doc'] = product_list
        paginator = Paginator(product_dict['product_doc'],10)
        page = request.GET.get('page')
        pr_detail = paginator.get_page(page)          
        return render(request, 'base.html',{'product':pr_detail})


# login page view functional code start (display template while go to main page) #
def login(request):
    return render(request, 'login.html')
# login page view functional code end #

# generate token functional code start #
def token(code, shop):
    ''' GENERATE ACCESS_TOKEN '''
    ur = "https://" + shop + "/admin/oauth/access_token"

    s = {
        "client_id": API_KEY,
        "client_secret": SHARED_SECRET,
        "code": code
    }
    r = requests.post(url=ur, json=s)
    x = json.loads(r.text)
    return x
# generate token functional code end #
@csrf_exempt
def get_installation(url):
    s_url = url.strip('/')
    if ("https://" in s_url) or ("http://" in s_url):
        f_url = s_url
        api_key = API_KEY   
        link = '%s/admin/oauth/authorize?client_id=%s&redirect_uri=https://%s/final&scope=%s' % (f_url, api_key,APP_URL,SCOPES)
        li = link.strip("/")
        redirect = HttpResponseRedirect(f'{li}')
    else: 
        f_url = "https://"+s_url
        api_key = API_KEY   
        link = '%s/admin/oauth/authorize?client_id=%s&redirect_uri=https://%s/final&scope=%s' % (f_url, api_key,APP_URL,SCOPES)
        li = link.strip("/")
        redirect = HttpResponseRedirect(f'{li}')
    return redirect


# installation process functional code start #
@csrf_exempt
def installation(request):
    if request.method == "POST":        # check request is post #
        url = request.POST['shop']  
        s_url = url.strip('/')
        if ("https://" in s_url) or ("http://" in s_url):
            f_url = s_url
            api_key = API_KEY   
            link = '%s/admin/oauth/authorize?client_id=%s&redirect_uri=https://%s/final&scope=%s' % (f_url, api_key,APP_URL,SCOPES)
            li = link.strip("/")
            redirect = HttpResponseRedirect(f'{li}')
        else: 
            f_url = "https://"+s_url
            api_key = API_KEY   
            link = '%s/admin/oauth/authorize?client_id=%s&redirect_uri=https://%s/final&scope=%s' % (f_url, api_key,APP_URL,SCOPES)
            li = link.strip("/")
            redirect = HttpResponseRedirect(f'{li}')
    return redirect
# installation process functional code end #


# redirect to app fucntional code start (while successfully installed redirect to app) #
def redirect(request):
    if request.GET.get('shop') is not None:     # check request data is not none #
        shop = request.GET.get('shop')
        redir = HttpResponseRedirect(redirect_to='https://' + shop + '/admin/apps/testingapp-146')
    return redir
# redirect to app fucntional code end #


# Uninstall Webhook functional code start (to create webhook) #
def unistaller_second(request):
    if len(shop) != 0:              # check the length of shop #
        webrec = installer.objects.filter(shop=shop)        # filter installer data by shop#
        if webrec:
            token = webrec[0].access_token
            hmac_data = webrec[0].hmac
        else:
            HttpResponse("Invalid shop detail")

        url = "https://" + shop + "/admin/api/2020-07/webhooks.json"

        headers = {
            'X-Shopify-Access-Token': token,
            'X-Shopify-Topic': 'app/uninstalled',
            'X-Shopify-Hmac-Sha256': hmac_data,
            'X-Shopify-Shop-Domain': shop,
            'X-Shopify-API-Version': API_VERSION
        } 

        my = {
            "webhook": {
                "topic": "app/uninstalled",
                "address": 'https://%s/uninstall' %(APP_URL),  # uninstall process data send on the address #
                "format": "json"
            }
        }
    
        r = requests.post(url=url, json=my, headers=headers)
        c = json.loads(r.text)
        return HttpResponse(json.dumps(c), content_type="application/json")
# Uninstall Webhook functional code start

# app install final step functional code start (to add shop data into database) #
@xframe_options_exempt
def final(request):
    my_dict = dict()
    if request.GET.get('hmac') is not None:         # check hmac is not none #
        hmac = request.GET.get('hmac')
        global shop
        shop = request.GET.get('shop')
        
        # charge_id = request.GET.get('charge_id')
        # if charge_id is not None and charge_id != "":
        #     plan_charges.objects.filter(application_charge_id=charge_id).update(status="active")
        # else:
        #     pass
        if request.GET.get('code') is not None:     # check code is not none #
            code = request.GET.get('code')
            if len(code) != 0:              # check length of code #
                record = installer.objects.filter(shop=shop)    # filter installer data by shop #
                if record:
                    get_code = record[0].code
                    get_access_token = record[0].access_token
                    return redirect(request=request)
                else:
                    accesstoken = token(code=code, shop=shop)       # call token function to generate access_token #
                    rec = installer()           # call installer to add record #
                    rec.shop = shop
                    rec.code = code
                    rec.hmac = hmac
                    rec.access_token = accesstoken['access_token']
                    rec.save()      # save data in installer table #

                    tokn = accesstoken['access_token']
                    

                    
                    
                    unistaller_second(request=request)          # call 'unistaller_second' to create webhook #
                    return redirect(request=request)            # redirect to app #
                return redirect(request=request)
        else:
            record = installer.objects.filter(shop=shop)        # filter installer data by shop #    
            if record:
                getaccess = record[0].access_token
                getshop = record[0].shop
                global get_tkn
                get_tkn = getaccess
                return HttpResponseRedirect("products_list")
            else:
                return get_installation(shop)
    else:
        return render(request, 'login.html')
# app install final step functional code end #
