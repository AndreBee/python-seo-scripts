import time
import pandas as pd                        
from pytrends.request import TrendReq

pd.set_option('expand_frame_repr', False)

input_doc = 'keywords.csv' # a csv file with one keyword per line
timeframe = 'now 7-d' # Check TrendReq library for other time frames
geo = 'IT'


def get_rising_keywords(kw, timeframe, geo):
    ''' Accepts a list of seed keywords and returns a DataFrame with
    related keywods and rising value '''
    
    # initialize pytrend with keyword list and selected country + timeframe
    pytrend = TrendReq(hl='it-IT')
    pytrend.build_payload(kw_list=kw, timeframe=timeframe, geo=geo)

    # get related queries
    try:
        related_queries_dict = pytrend.related_queries()
    except:
        print("An error occured, please try again later.")

    all_related_queries = pd.DataFrame(columns=['seed_kw', 'query', 'rising (%)'])
    
    # loop through related queries and get rising value
    for query in related_queries_dict:
        related_queries = related_queries_dict[query].get('rising')
        related_queries['seed_kw'] = query
        related_queries = related_queries.rename(columns = {'value': 'rising (%)'}, inplace = False)
        all_related_queries = all_related_queries.append(related_queries)
    
    return all_related_queries


def rising():

    rising_final_df = pd.DataFrame()

    print("** Getting rising queries from seed keywords... ** ")
    with open(input_doc, newline='') as csvfile:
            for kw in csvfile:
                print(f"> Getting rising queries for seed kw: {kw}")
                related_kws = get_rising_keywords([kw], timeframe, geo)
                rising_final_df = rising_final_df.append(related_kws, ignore_index=True)



    filename = f"rising_kws_{time.strftime('%Y%m%d-%H%M%S')}.xlsx"
    rising_final_df.to_excel(filename)
    print(f"** Results saved to Excel file: {filename} ** ")

    
if __name__ == '__main__':
    rising()

