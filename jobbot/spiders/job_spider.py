import scrapy
from bs4 import BeautifulSoup  
from jobbot.items import JobItem
from nltk import word_tokenize, sent_tokenize, PorterStemmer, FreqDist
from nltk.corpus import stopwords

class JobSpider(scrapy.Spider):
    name = "statjobs"
    allowed_domains = ["www.stat.ufl.edu"]

    # Seem to always be 10 pages of jobs
    start_urls = ["http://www.stat.ufl.edu/jobs/?page=" + str(i) for i in range(1,11)]

    def __init__(self):
        self.metadata = {}

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        jobs = soup.select('.joblist tr')
        for job in jobs:
            
            jobels = job.select('td')
            if len(jobels)==3:
                link = jobels[0].find('a').get('href')        
                jobid = link.split("=")[1]
                title = jobels[1].get_text()
                date = jobels[2].get_text()
                org = jobels[0].get_text()
                self.metadata[jobid] = {'title':title, 'date':date, 'organization':org}

                desc_url = "http://www.stat.ufl.edu/jobs/" + link
                yield(scrapy.Request(desc_url, callback=self.parseDescription))

    # returns a bag of words (FreqDist) representation of the content
    def processContent(self, content):
        stemmer = PorterStemmer()
        tokens = word_tokenize(content)
        tokens = filter(lambda x: len(x) < 20 and x.isalnum(), tokens)
        tokens = [stemmer.stem(token.lower()) for token in tokens]
        tokens = filter(lambda x: x not in stopwords.words('english'), tokens)
        tokens = [str(token) for token in tokens]      
        bow = FreqDist(tokens)
        return(bow)

    def parseDescription(self, response):
        url = response.url
        jobid = url.split("=")[1]

        soup = BeautifulSoup(response.body)
        content = soup.select('#content')
        if len(content)==1:
            content_text = content[0].get_text()
            item = JobItem()
            item['jobid'] = jobid
            item['description'] = self.processContent(content_text)
            if jobid in self.metadata:
                item['title'] = self.metadata[jobid]['title']
                item['organization'] = self.metadata[jobid]['organization']
                item['date'] = self.metadata[jobid]['date']
            yield(item)

