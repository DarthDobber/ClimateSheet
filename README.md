# ClimateSheet

A script that will scrape climate data from the Minnesota Department of Natural Resources and 
put that data into a google sheet.  The script loops through the google sheet and matches the date
in the sheet to the date of the climate data.

This is the sheet I tested with:

https://docs.google.com/spreadsheets/d/1cGFbQwt9TjDduoB8nCT3GH6JFC-9WGf7SsN-eXfiPKA

Installation
============

1. Download the repository and extract it to a folder you have rights to
2. Open a command prompt and browse to the "repository folder"\venv\Scripts
3. Run 'activate' from the command prompt, this will activate the virtual environment
4. Move up two directories to the root of the repository folder
5. Run the command 'python climatesheet.py' You should be able to see spreadsheet being updated in real time.


Requirements
============

ClimateSheet requires python 3.5 or later


The pip requirements.txt script will install the following packages on your system
* cssselect==1.0.3
* gspread==0.6.2
* lxml==4.1.1
* oauth2client==4.1.2
* requests==2.18.4

License
=======


```
    Copyright (C) 2016 Robert McDougal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
