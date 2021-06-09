import json
import csv
import requests
import pandas as pd
import time


endpoint = "https://api.keywordtool.io/v2/search/suggestions/google"
# Use the endpoint below for testing to not waste API credits.
#endpoint = "https://api.keywordtool.io/v2-sandbox/search/suggestions/google" 



# settings
api_key = 'YOUR_API_KEY'
input_doc = 'keywords.csv' # a csv file with one keyword per line
exclude_kws = [] # list of keywords to exclude from suggestions
country = 'IT' # for country and location codes check API docs
location = 2380 
language = 'it' 
currency = 'EUR'

def check_api_quota(api_key):
    ''' Returns a DataFrame with API quota '''
    
    apiquota = f'https://api.keywordtool.io/v2/quota?apikey={api_key}'
    response = requests.post(apiquota)
    # receiving results in a dictionary
    dic = response.json()

    # remove the results key from the dictionary
    dic = dic.pop("limits", None)

    # convert dictionary to dataframe
    data = pd.DataFrame.from_dict(dic, orient='index')

    return data



def get_suggestions(api_key, settings):
    ''' Accepts an API key and a dictionary of settings. 
    Returns a list of keywords with search volume in a pandas DataFrame'''

    
    try:
        
        response = requests.get(endpoint, params=settings)
        json_response = json.loads(response.text)
        
        if "error" in json_response:
            raise Exception(f"There was an error with code {json_response['error']['code']}. Please check API doc!")

        
        
        kw_suggestions_df = pd.DataFrame(columns=['keyword', 'volume'])

        for seed_kw in json_response['results']:
            suggestions = json_response['results'][seed_kw]
            

            for suggestion in suggestions:

                data = {
                    'keyword': suggestion['string'],
                    'volume': suggestion['volume']
                }

                kw_suggestions_df = kw_suggestions_df.append(data, ignore_index=True).drop_duplicates(subset=['keyword']).sort_values(by=['volume'], ascending=False)
        return kw_suggestions_df
    

    except requests.ConnectionError:
            print("There was a connection error while trying to call the API. Please try again") 

        

def check_suggestions():
    print("** Reading input file ** ")
    final_df = pd.DataFrame()
    with open(input_doc, newline='') as csvfile:
        for kw in csvfile:
            # check remaining quota
            quota = check_api_quota(api_key)

            if quota.iloc[1]['remaining'] > 0:
                print(f"> Remaining requests today: {quota.iloc[1]['remaining']}")
                print(f">> Checking suggestions for keyword: {kw}")
                
                settings = {
                    "apikey": api_key,
                    "keyword": kw,
                    "category": "web",
                    "country": country,
                    "language": language,
                    "type": "suggestions",
                    "exclude": [],
                    "metrics": 'true',
                    "metrics_location": location,
                    "metrics_language": language,
                    "metrics_network": "googlesearchnetwork",
                    "metrics_currency": currency,
                    "output": "json"
                }
                
                df = get_suggestions(api_key, settings)
                final_df = final_df.append(df)

                # make a request every 7 seconds (due to API limits)
                time.sleep(7)

            else:
                raise Exception("Your daily quota is 0. Please try again tomorrow")
                
    
    filename = f"kw_suggestions_{time.strftime('%Y%m%d-%H%M%S')}.xlsx"
    final_df.to_excel(filename)
    print(f"** Results saved to Excel file: {filename} ** ")


if __name__ == '__main__':
    
    check_suggestions()






