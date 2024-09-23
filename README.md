# Countries Data

## Purpose

This script gathers data about all countries listed in REST Countries API. This includes each country's capital, population, area, region, subregion, languages spoken, curriences, and male and female life expectancy. 

This data could have many different uses depending on what the user needs. For example, this could be a way to get general information about multiple countries without needing to spend time researching each individual country. The data here can also be used to investigate correlations that might be candidates for future study if interesting

## How It Works

The script gets a list of all countries in REST Countries API. Then using each country given, it will request REST Countries API for data on capital, population, area, region, subregion, languages, and curriences. It then goes to that countries respective BBC country profile and scrapes the page for the male and female life expectancy of said country.

### API Selection: REST Countries API

### Website Selection: BBC Country Profiles (ex: https://www.bbc.com/news/world-latin-america-18909529 leads to Brazil's profile)

This website was chosen due to the presence of the life expectancy information in addition to the fact that there was not an accessible API that addressed the country profiles.

## How to Run

1. Clone the Repository
git clone https://github.com/AZ0324/all_about_countries

2. Install Dependencies
Create a virtual environment and install the required packages:

3. Run the Script
The script will automatically compile data from all countries listed on REST Countries API and their respective BBC country profiles