jobbot
======

jobbot is just a simple scrapy project I wrote to teach myself scrapy.  It pulls the job postings from the University of Florida's statistics jobs page.  The job descriptions are then tokenized, lower cased, stemmed, cleaned of stopwords, and represented as a frequency distribution.  This seemed sufficient for playing around with bag-of-words type techniques. 


Dependencies
------------

To run this, you'll need to install the scrapy, BeautifulSoup, and nltk packages.

Usage
-----

I find it useful to store the output in json using:

    scrapy crawl statjobs -o statjobs.json

The output file can then be loaded into R via something like:
 
    require(rjson)
    dat <- fromJSON(file="statjobs.json")


