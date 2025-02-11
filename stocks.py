"""
File name: stocks.py

Author: Rachel Newman

Student ID: 2562294

Purpose: The purpose of this assignment is to demonstrate an understanding of how to interact with web APIs, processing real-world
financial data, and implementing error handling with try-except blocks.

Resources: For this assignment, I was able to create my function 'stock_prices' without any references whatsoever. In my 
'download_data' function, I first copied the information that was provided in the assignment instructions and then tried to create
my try-except block to handle errors in network connectivity or APIs by myself. I figured out that I needed send an HTTP Get request
to the Nasdaq API and write the JSON information into a Python dictionary, but I could not figure out what kinds of errors I would 
encounter. To assist me with this, I had ChatGPT help me write the 'except' block in this function. Given that I haven't worked with
JSON documents much, I wasn't sure how to write data into one, so I looked at this website for assistance: 
'https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/'. I also used ChatGPT to help me  in the main function to
implement argv so that the user can provide the stock ticker symbols of the stocks they are looking at.
"""
import requests
import json
import sys
import statistics
from datetime import date

# function that retrieves historical stock data
def download_data(ticker: str) -> dict: 
    """ A function that retrieves historical stock data from Nasdaq
    
    Args: 
        ticker (str): The stock ticker symbol for a company (e.g., 'AAPL' for Apple).
        
    Returns:
        dict: Returns a dictionary containing a company's ticker symbol and a list of
        closing prices. 
        Returns None if data retrieval fails.
    """
    # copied these next five lines from assignment instructions! 
    ticker = ticker.upper() # converts ticker symbol to uppercase to match standard API format
    today = date.today() # collects the current date
    start = str(today.replace(year = today.year - 5)) # calculates the start date to pull stock prices
    base_url = "https://api.nasdaq.com" 
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"

    url = base_url + path

    # this sets the request headers to mimic a web browser and prevent request blocking
    headers = {"User-Agent": "Mozilla/5.0"}  # avoids request blocking

    # implementing a try-except block to handle errors retrieving the API
    try:
        response = requests.get(url, headers = headers) # this sends an HTTP GET request to the NAsdaq API
        response.raise_for_status()  # raise error for bad responses (4xx, 5xx)
        data = response.json() # writes the JSON response into a dictionary

        # this if statement checks if the required data fields exist in the response
        if "data" in data and "tradesTable" in data["data"]:
            # the line below removes the '$' and ',' from the prices and converts the string to a float
            prices = [float(entry["close"].replace("$", "").replace(",", "")) for entry in data["data"]["tradesTable"]["rows"]]
            return {"ticker": ticker, "prices": prices} # returns a dictionary with the ticker symbol and prices
        else:
            # if no data is found for the ticker a message is printed and None is returned
            print(f"No data found for {ticker}")
            return None

    except requests.exceptions.RequestException as e:
        # handling any network or API errors
        print(f"Error fetching data for {ticker}: {e}")
        return None

# function to analyze stock prices for different tickers  
def stock_prices(prices: list, ticker: str) -> dict:
    """A function that computes basic statistics (min, max, mean, median) of historical
     stock prices.
    
     Args: 
        prices (list): A list of closing prices for a stock.
        ticker (str): The stock ticker symbol for a company (e.g., 'AAPL' for Apple).
      
    Returns: 
        dict: Returns a dictionary of basic statistics and the stock ticker symbol.
        Returns None if there is no price data """
    if not prices:  # checking if the list is empty
        print(f"No price data available for {ticker}.")
        return None  # avoids division by zero
    
    return {
        "min" : min(prices),
        "max" : max(prices),
        "avg" : sum(prices) / len(prices), # returns the mean
        "medium" : statistics.median(prices),
        "ticker" : ticker
    }

# main function to write stock data into a JSON file
def main():
    if len(sys.argv) < 2:
        print("Instructions: python stocks.py TICKER1 TICKER2 ...\n") #prints instructions for how to compile code
        sys.exit(1)

    tickers = sys.argv[1:] # extracts ticker symbols from the command-line arguments put in by user
    results = [] # creates an empty list to store results for each stock

    # looping through each ticker provided in the command-line
    for ticker in tickers:
        stock_data = download_data(ticker) # fetches historical stock data for the ticker
        if stock_data and stock_data["prices"]: 
            stats = stock_prices(stock_data["prices"], ticker) # analyzes stock price and computes basic statistics
            if stats:  
                results.append(stats) # appends stats to results list if they are successfully computed
        else:
            print(f"Skipping {ticker} due to missing data.") # skips the ticker if there is no data

    # saving the results in a JSON file if they are retrieved successfully
    if results:
        try:
            with open("stocks.json", "w") as f:
                # opens JSON document in write mode so I can write the stock data into it
                json.dump(results, f, indent = 4) 
            print("Data successfully saved to stocks.json")
        except Exception as e:
            print(f"Error saving file: {e}")

if __name__ == "__main__":
    main()