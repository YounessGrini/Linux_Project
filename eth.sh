#!/bin/bash

# Fetch the web page HTML
site=$(curl -s https://www.coingecko.com/en/coins/ethereum)


# Extract the Ethereum Price
price=$(echo "$site" | grep -Po '^\$[\d,]+\.\d{2}$' | tail -n 1)


# Get the current time 
time=$(date +"%Y-%m-%d %H:%M:%S")


# Save the result to a file
echo " $price" >> eth.txt
echo " $time" >> date.txt
