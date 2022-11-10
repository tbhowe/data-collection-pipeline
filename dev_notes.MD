
# DEV notes 
- my notes on the project, delete from repo at end

## implementing reverse lat,long lookup in geopy

https://towardsdatascience.com/things-to-do-with-latitude-longitude-data-using-geopy-python-1d356ed1ae30

We can use this approach to turn the lat/long data scraped from the property cards into a full address and postcode.

## implementing CAGR from price history:

CAGR = (Price/IAP)^(1/N_Years)-1

this is a good measure of the performance of the property as an investment

## implementing IAP

- inflation-adjusted prices give a better asessment of real value change in the sale price history.

- choosing a source for inflation adjustment could get interesting - CPI is heavily politicised and widely criticised. Could use Truflation metric instead.  https://app.truflation.com/