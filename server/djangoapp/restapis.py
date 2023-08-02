import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    # If argument contain API KEY
    print("GET from {} ".format(url))
    try:
        if "api_key" in kwargs:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]

            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    response = requests.post(url, json=json_payload, **kwargs)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers=json_result      
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    print('json_result from line 54',json_result)

    if json_result:
        dealers = json_result
        
    
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
    return dealer_obj

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs['kwargs']
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    if json_result:
        data = json_result['data']
        reviews = data['docs']
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"])
            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]
            
            sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/e3225b6c-2683-402e-81ab-0e613194f5ca"
    api_key = "41ZqrQiOQeSfPH-o4J3MgjGI_0A9O36Ral_vFd6_MlFm"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    
    return(label)

#def post_request(url, payload, **kwargs):
#    status_code = None
#    print(kwargs)
#    print("POST to {} ".format(url))
#    print(payload)
#    try:
#        response = requests.post(url, params=kwargs, json=payload, headers={'Content-Type': 'application/json'},
#                                    auth=HTTPBasicAuth('apikey','api_key'))
#    except:
#        status_code = response.status_code
#    print("With status {} ".format(status_code))
#    json_data = json.loads(response.text)
#    return json_data

def get_single_dealers(**kwargs):
    results = {}
    # Call get_request with a URL parameter
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/4faf8dbd-d6b2-4192-af16-f96ff1a3f43f/dealership-package/get-dealership"
    if 'dealer_id' in kwargs:
        json_result = get_request(url, id=kwargs["dealer_id"])
    else:
        json_result = get_request(url)
    if json_result:
        dealers = json_result[0]
        # Creates a dealer Object from the JSON result
        dealer_obj = CarDealer(address=dealers["address"], city=dealers["city"], full_name=dealers["full_name"],
                                id=dealers["id"], lat=dealers["lat"], long=dealers["long"],
                                short_name=dealers["short_name"],
                                st=dealers["st"], zip=dealers["zip"])
        results["dealer"] = dealer_obj
    return results