# rfc-scraper

Script for scraping Internet RFCs; updated as of 9083 

The `src` folder contains the scripts for pulling down the RFCs, associated metadata, and searching for matching terms in the RFCs (and the mapping those matches to the associated metadata). This is a mix of python and bash (with python calling bash in cases where the code was much faster to implement in bash). Scripts should be executed from within the `src` directory.

The `data` folder contains raw scraped data as well as generated output data from the scripts above.


# TODO dependencies