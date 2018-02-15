# Importing the dependencies
# This is needed to create a lxml object that uses the css selector
from lxml.etree import fromstring
  
# The requests library
import requests

# The gspread library for working with sheets
import gspread

#The authentication client
from oauth2client.service_account import ServiceAccountCredentials 

#Custom Class to hold the AJAX results returned from the server
class ClimateData:
    
    data = {}

    def __init__(self, input):        
        for i in input:
            self.data[i[0]] = {'max':i[1][0], 'min':i[2][0], 'precip':i[3][0], 'snow':i[4][0], 'depth':i[5][0]}
    
    def get_info(self, date):
        print(self.data[date])
        

class ClimateScraper:
  
    API_url = 'http://data.rcc-acis.org/StnData'
    scraped_data = []

    def get_data(self):
     
        # This is the only data required by the api 
        # To send back the climate info you needed
        # If you wanted to get a different date range
        # simply change the 'sdate' value to something
        # else
        data = {
        'params': '{"sid":"mspthr","sdate":"2018-01-01","edate":"por","elems":[{"name":"maxt","interval":"dly","duration":"dly","add":"t"},{"name":"mint","interval":"dly","duration":"dly","add":"t"},{"name":"pcpn","interval":"dly","duration":"dly","add":"t"},{"name":"snow","interval":"dly","duration":"dly","add":"t"},{"name":"snwd","interval":"dly","duration":"dly","add":"t"}]}'
        }
        # Making the post request
        response = requests.post(self.API_url, data=data)
 
        # This returns a list containing all the data you want
        return response.json()['data']

    def parse_data(self, data):
        results = ClimateData(data)
        return results

    def run(self):
        data = self.get_data()
        test = self.parse_data(data)
        test.get_info('2018-02-06')          

#Authorizing connection to google sheets, you need to create a project on Google's 
#API Manager
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

#Open a worksheet
book = client.open_by_url('https://docs.google.com/spreadsheets/d/1cGFbQwt9TjDduoB8nCT3GH6JFC-9WGf7SsN-eXfiPKA')

#Get the State
worksheet = book.get_worksheet(0)

#The main execution
if __name__ == '__main__':
    scraper = ClimateScraper()
    scraper.run()