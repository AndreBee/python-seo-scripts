# Google Trends bulk checkers

A set of tools to get data in bulk from Google Trends. They are built on top of the unofficial API https://pypi.org/project/pytrends/


# Get started

In order to make these scripts work, you need to install two dependencies, as follows:


        $ pip install pytrends
        
        $ pip install pandas
        

# How the scripts work

Both the rising_kws and the interest_over_time scripts accept a .csv file as an input with a list of seed keywords, one per line.
Then, the scripts get data from Google Trends and generate a unique final .xlsx file with the output.

Note: if you check a lot of keywords in bulk you might reach the limit and won't be able to retrieve data as the scripts are not handling rate limit at the moment.
