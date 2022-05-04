import requests
import json



API_VERSION = "2022-04"
doc_product_list = list()
all_data = dict()


class APIS:
    
    @staticmethod
    def get_prodoct_from_url(c, shop, token,url,headers, limit):
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            c = json.loads(r.text)    
            doc_product_list.append(c['products'])
            all_data['products']= doc_product_list
            
            if len(c['products']) == limit:
                since_id = c['products'][-1]['id']
                print(since_id)
                url = "https://%s/admin/api/%s/products.json?limit=%s&since_id=%s" % (shop, API_VERSION,limit,since_id)
                APIS.get_prodoct_from_url(c, shop, token, url, headers, limit)
            return all_data
        else:
            return all_data

    @staticmethod
    def get_products(shop, token):
        c = ''
        print("in api")
        limit = 50
        url = "https://%s/admin/api/%s/products.json?limit=%s" % (shop, API_VERSION,limit)

        headers = {
            "X-Shopify-Access-Token": token
        }
        d = APIS.get_prodoct_from_url(c, shop, token, url, headers, limit)
        return d