# Keyword suggester built upon Keywordtool.io API

## What does it do?

The keyword suggester is a simple python script that makes calls to Keywordtool.io API in order to retrieve keyword suggestions from Google Web Search.

You can feed it with a .csv file containing a list of keywords - one per line - and it will produce a new file in .xlsx format with all the suggestions for those keywords, together with their monthly search volume.

## Get started

To make the script work, you need to install two dependencies, namely Pandas and requests.


        $ pip install pandas
        
        $ pip install requests
        
You will need an API key to use the script, which you can get at https://keywordtool.io - automatic!


## API limits and settings

Please refer to the API docs at https://keywordtool.io - automatic! to know about API limits and settings.
