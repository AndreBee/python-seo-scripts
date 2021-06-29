import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# settings
input_tags = 'initial_tags.xls'

def get_tags_from_url(url):
    # TO DO: case when tags are completely removed from page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    data = {
        'Address': response.url,
    }
    
    try:

        title = soup.title
        
        if title:
            data['Title'] = title.string
            
        description = soup.find('meta', attrs={'name':'description'})
        
        if description:
            data['Meta Description'] = description.get('content')
            
        robots = soup.find('meta', attrs={'name':'robots'})
        
        if robots:
            data['Meta Robots'] = robots.get('content')

        canonical = soup.find('link', attrs={'rel':'canonical'})
        
        if canonical:
            data['Canonical'] = canonical.get('href')
         
        return data
        
    except Exception as e:

        print(e)


def send_email(dataframe):  

    #The mail addresses and password
    sender_address = 'SENDER_EMAIL' 
    sender_pass = 'SENDER_PASSWORD' 
    receiver_address = 'RECEIVER_EMAIL' 
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = 'The Mighty Tag Checker'
    message['To'] = receiver_address
    message["Subject"] = "🚨 Changes in the tags detected! - The Mighty Tag Checker🚨"
    mail_text = '''
    
    Hello,
    
    
    This is the Mighty Tag Checker. I have detected changes in the tags for some URLs you are monitoring. Was it you?
    
    You can find a detailed report below.
    
    Remember to update the input Excel file if the changes were intentional.
    
    '''
    mail_html = """\
            <html>
              <head></head>
              <body>
                {0}
              </body>
            </html>
            """.format(dataframe.to_html())
    
    html = MIMEText(mail_html, 'html')
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_text, 'plain'))
    message.attach(html)
    
    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls(context=context) #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    except Exception as e:
        # Print any error messages to stdout
        print(e)

def check_tags():
    
    # accepts a report from the "Internal" tab in Screaming Frog in xls format
    initial_tags = pd.read_excel('initial_tags.xls', usecols=[
                                                            'Address', 
                                                            'Title 1',
                                                            'Meta Description 1',
                                                            'Meta Robots 1',
                                                            'Canonical Link Element 1'
                                                    ])

    # rename columns for user friendlyness
    initial_tags = initial_tags.rename(columns={
        "Title 1": "Title", 
        "Meta Description 1": "Meta Description",
        'Meta Robots 1': 'Meta Robots',
        'Canonical Link Element 1': 'Canonical'
    })

    initial_tags = initial_tags.fillna("")
    
    latest_tags = pd.DataFrame(columns=[
                                'Address',
                                'Title', 
                                'Meta Description',
                                'Meta Robots', 
                                'Canonical'
                                ])

    for url in initial_tags['Address']:
        url_recent_tags = get_tags_from_url(url)
        latest_tags = latest_tags.append(url_recent_tags, ignore_index=True)


    latest_tags = latest_tags.fillna("")
    

    # set urls as index to display them in the differences dataframe
    initial_tags = initial_tags.set_index('Address')
    
    latest_tags = latest_tags.set_index('Address')

    differences = initial_tags.compare(latest_tags, keep_equal=False)

    differences = differences.fillna("")

    differences = differences.rename(columns={"self": "Initial", "other": "Latest"})

    send_email(differences)

    differences.to_excel('diff.xlsx')
    print('ok')


if __name__ == '__main__':
    check_tags()
