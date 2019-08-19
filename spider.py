import scrapy
import re
import requests
from urllib.parse import urlparse
import nltk
from nltk.tag.stanford import StanfordNERTagger

st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar')


class IndeedSpider(scrapy.Spider):
	name = "brickset_spider"
	start_urls = ['https://se.indeed.com/jobb?q=developer&l=', 'https://se.indeed.com/jobb?q=software+engineer&l=', '']

	def parse(self, response):

		for nextPage in response.css('div.pagination > a:last-child'):
			yield response.follow(nextPage, self.parse)

		for job in response.css('div.jobsearch-SerpJobCard > div.title > a.jobtitle'):
			yield response.follow(job, self.parse)

			
		for b in response.css('div.jobsearch-JobComponent'):	
			job_title = response.css('h3.jobsearch-JobInfoHeader-title ::text').extract_first()
			employer = response.css('div.jobsearch-JobInfoHeader-subtitle ::text').extract_first()
			res = requests.get(response.css('#viewJobButtonLinkContainer > div > a ::attr(href)').extract_first())
			website = urlparse(res.url).netloc
			job_description = ','.join(response.css('#jobDescriptionText ::text').extract())
			email = re.findall(r'[\w\.-]+@[\w\.-]+', job_description)
			phone = re.findall(r'(\(?([\d \-\)\–\+\/\(]+){6,}\)?([ .\-–\/]?)([\d]+))', job_description)

			names = []
			for sent in nltk.sent_tokenize(job_description):
				tokens = nltk.tokenize.word_tokenize(sent)
				tags = st.tag(tokens)
				for tag in tags:
					if tag[1] in ["PERSON"]:
						names.append(tag[0])
				
			yield {
				'job-title': job_title,
				'employer': employer,
				'website': website,
				'email': email,
				'phone': (phone[0][0] if len(phone)>0 else ""),
				'names': names,
				'job_description': job_description
			}