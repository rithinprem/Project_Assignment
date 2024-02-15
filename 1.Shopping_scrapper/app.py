from flask import Flask,jsonify,render_template,request
import requests
from bs4 import BeautifulSoup
import json
import time

app = Flask(__name__)


    
#amazon website

def amazon(search_term):
    search = search_term
    print(search)
    params = {"k":search}
    url = "https://www.amazon.in/s"
    headers_={"authority":"www.amazon.in",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language":"en-US,en;q=0.9",
    "cache-control":"max-age=0",
    "cookie":"session-id=261-8899712-9270921; i18n-prefs=INR; ubid-acbin=258-3009957-1207162; s_cc=true; s_vnum=2138694198424%26vn%3D1; s_ppv=18; s_nr=1706694204691-New; s_dslv=1706694204694; s_sq=acsin-prod%3D%2526pid%253DGSUNWNFT2ALMPR3L%2526pidt%253D1%2526oid%253DGo%2526oidt%253D3%2526ot%253DSUBMIT; session-id-time=2082787201l; session-token=0y5PdF1inX7SdGXRm/Ozis+YAfjoVEF3mnMHa4fhibpIpjb+3YWGIzcXHOITsalWYpC+AVqVcaOJnLgYqkX+m2u7MTnMvVpyD1Twrct5EnmLpv2ju7J16NahsIjFD4kT6ZIxDhlGvxigTVEmuXlLIDscBwV3f36DgQR+0D3qQwKpCBeKT0Yjj7B9DaPjNJS3OIK4R2YgJZP4fpdVJsbo2QoTQwELsLHJlwK+ZvmfJGWWMe0NB4BNDsc4r48M2yuyH+7OP/2jAc7AMzWeeZrLYgwQ66KM/fJ9CNnhr/jBMMNsVMUKQyL8DKicvHGo5gBU1hTIyUULzQQFaudyE4/Gh+w/7s30IkPQ; csm-hit=tb:SJ4CTQM8TB6XR2X280CP+s-SJ4CTQM8TB6XR2X280CP|1706696228971&t:1706696228971&adb:adblk_no",
    "device-memory":"8",
    "downlink":"9.75",
    "dpr":"1",
    "ect":"4g",
    "referer":"https://www.google.com/",
    "rtt":"100",
    "sec-ch-device-memory":"8",
    "sec-ch-dpr":"1",
    "sec-ch-ua-mobile":"?0",
    "sec-ch-ua-platform":"Windows",
    "sec-ch-ua-platform-version":"10.0.0",
    "sec-ch-viewport-width":"1366",
    "sec-fetch-dest":"document",
    "sec-fetch-mode":"navigate",
    "sec-fetch-site":"same-origin",
    "sec-fetch-user":"?1",
    "upgrade-insecure-requests":"1",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "viewport-width":"1366"
    }

    response = requests.get(url,params=params,headers=headers_)
    soup = BeautifulSoup(response.text,'html.parser')

    with open('amazon_product_html.html', 'w', encoding='utf-8') as file:
                file.write(soup.prettify())

    data=[]
    json_data = {}
    json_data['status']='error'
    json_data['data'] = data

    #for vertical cards
    card_soup = soup.find_all('div',{'class':'puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-vw0goty2ahaky2ds8ppx5s5mhw s-latency-cf-section puis-card-border'})
    if  card_soup:
        print("hi")
        for i in card_soup:
            
            json_data['status']='success'
            dic={}
            
            heading=i.find('span',{'class':'a-size-medium a-color-base a-text-normal'})
            if heading:
                heading=heading.get_text()

            
            price = i.find('span',{'class':'a-offscreen'})
            if price:
                price=price.get_text()
                
            image = i.find('img')
            if image:
                image=image.get('src')

            link = i.find('a',{'class':'a-link-normal s-no-outline'})
            if link:
                link = link.get('href')
            
        
            dic["Product_Description"]=heading 
            dic["Product_Price"]=price
            dic["Product_link"]="https://www.amazon.in"+ link if link else ''
            dic["Product_Image"]=image
            data.append(dic)
            
        
    #for horizontal cards
    else:    
        card_soup = soup.find_all('div',{'class':'a-section a-spacing-base a-text-center'})
        if  card_soup:
            for i in card_soup:

                json_data['status']='success'
                dic={}

                heading=i.find('span',{'class':'a-size-base-plus a-color-base'})
                if heading:
                    heading=heading.get_text()


                name = i.find('span',{'class':'a-size-base-plus a-color-base a-text-normal'})
                if name:
                    name=name.get_text()

                price = i.find('span',{'class':'a-price-whole'})
                if price:
                    price=price.get_text()

                image = i.find('img')
                if image:
                    image=image.get('src')

                link = i.find('a',{'class':'a-link-normal s-no-outline'})
                if link:
                    link = link.get('href')


                dic["Product_Description"]=heading + " " +name
                dic["Product_Price"]=price
                dic["Product_link"]="https://www.amazon.in"+ link if link else ''
                dic["Product_Image"]=image
                data.append(dic)


    
    #convert dic to json     
    json_data_ = json.dumps(json_data) 

    #convert json string to json object
    json_data = json.loads(json_data_)
    return json_data

def greateasternretail(search_term):
    search = search_term
    url = f"https://www.greateasternretail.com/search/{search}/"
    response = requests.get(url,verify=False)
    soup = BeautifulSoup(response.text,'html.parser')
    products = soup.find_all('li',{'class':"col-6 col-sm-4 col-lg-3"})

    data=[]
    json_data = {}
    json_data['status']='error'
    json_data['data'] = data


    if products:
        for prod in products:

            json_data['status']='success'
            dic={}

            heading = prod.find('h5',{'class':'mb-1 product-item__title'})

            if heading:
                link =  heading.find('a').get('href')

                heading = heading.find('a').get_text()

            price = prod.find('ins')
            if price:
                price = price.get_text().strip()

            image = prod.find('img',{'class':'img-fluid lazy'})
            if image:
                image=image.get('data-src')

            dic["Product_Description"]=heading 
            dic["Product_Price"]=price
            dic["Product_link"]="https://www.greateasternretail.com"+ link if link else ''
            dic["Product_Image"]=image
            data.append(dic)

    #convert dic to json        
    json_data_ = json.dumps(json_data) 

    #convert json string to json object
    json_data = json.loads(json_data_)

    return json_data

@app.route("/", methods=["GET"])
def amazon_search():
    search_term = request.args.get("search", default="laptop", type=str)
    amazon_data = amazon(search_term)
    greateasternretail_data = greateasternretail(search_term)

    return render_template("result.html", amazon_data=amazon_data,greateasternretail_data=greateasternretail_data)


if __name__=="__main__":
    app.run(host="0.0.0.0",port = 5002)
