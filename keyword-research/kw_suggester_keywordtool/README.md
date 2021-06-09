# Google keyword suggester powered by Keywordtool.io API

## What does it do?

The keyword suggester is a simple python script that makes calls to Keywordtool.io API in order to retrieve keyword suggestions from Google Web Search.

You can feed it with a .csv file containing a list of keywords - one per line - and it will produce a new file in .xlsx format with all the suggestions for those keywords, together with their monthly search volume.



## Get started

To make the script work, you need to install two dependencies, namely Pandas and requests.


        $ pip install pandas
        
        $ pip install requests
        
You will need an API key to use the script, which you can get at https://keywordtool.io

Note that you can use the sandbox endpoint while testing, so that you don't waste API credits. Just uncomment the test endpoint and comment the production one.

## How to use the script

Once you have downloaded the script and installed the dependencies you can do the following:

1) Create a new .csv file with a list of keywords to get suggestions for, one keyword per line. Save the file and include the path in the script.
2) On the terminal, just run:

                python keywordtool_google_suggester.py
                
3) Follow the progress on the screen until the output file is generated.

## API limits and settings

Please refer to the API docs at https://keywordtool.io to know about API limits and settings.
