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
class googSheets:

    # Setting up variables needed to connect to Google sheets.
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # The URL for the spreadsheet you want to work with, Make
    # sure that you have created credentials using the Google
    # API manager and shared the worksheet with the email address
    # of the API credentials you created
    sheet_url = 'https://docs.google.com/spreadsheets/d/1cGFbQwt9TjDduoB8nCT3GH6JFC-9WGf7SsN-eXfiPKA'
    book = ''
    worksheet = ''

    # These two variables point to where the date information
    # begins in your spreadsheet, on mine it is A2 or (2, 1)
    start_row = 2
    start_col = 1

    # This variable is the column where you want to start inputing
    # the climate data.  On mine I am just starting in the B column
    # or rather 2.
    write_col = 2

    def __init__(self):
        # Open a workbook
        self.book = self.client.open_by_url(self.sheet_url)
        # Gets the first worksheet, index begins at 0
        self.worksheet = self.book.get_worksheet(0)

    def find_in_sheet(self, query):
        cell = self.worksheet.find(query)
        return cell
    
    def update_cell(self, row, col, new_value):
        self.worksheet.update_cell(row, col, new_value)
    
    def update_sheet(self, data):
        row = self.start_row
        col = self.start_col
        w_col = self.write_col

        while self.worksheet.cell(row, col) != '':
            date = self.worksheet.cell(row, col)
            print(date.value)
            data_set = data.get_info(date.value)            
            print(data_set)
            self.update_cell(row, w_col, data_set['max'])
            self.update_cell(row, w_col+1, data_set['min'])
            self.update_cell(row, w_col+2, data_set['precip'])
            self.update_cell(row, w_col+3, data_set['snow'])
            self.update_cell(row, w_col+4, data_set['depth'])
            row = row + 1

        
class ClimateData:
    
    data = {}

    def __init__(self, input):        
        for i in input:
            if not None:
                self.data[i[0]] = {'max':i[1][0], 'min':i[2][0], 'precip':i[3][0], 'snow':i[4][0], 'depth':i[5][0]}
    
    def get_info(self, date):
        return self.data[date]
    
    def pprint(self):
        print(self.data)
        

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

    # Taking the raw data and converting it into a custom class
    # that organizes the data into a dictionary, making it easier
    # to work with.
    def parse_data(self, data):
        results = ClimateData(data)
        return results

    # What to do when the script is run.
    def run(self):
        data = self.get_data()
        parsed_data = self.parse_data(data)
        return parsed_data    

#The main execution
if __name__ == '__main__':
    scraper = ClimateScraper()
    google_sheet = googSheets()
    data = scraper.run()
    google_sheet.update_sheet(data)
    
