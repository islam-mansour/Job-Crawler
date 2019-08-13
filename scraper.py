import scrapy

class IndeedSpider(scrapy.Spider):
	name = "brickset_spider"
	start_urls = ['https://www.indeed.ch/jobs?q=software%20developer&l&vjk=20b5339b35deba3e']

	def parse(self, response):

		for nextPage in response.css('div.pagination > a:last-child'):
			yield response.follow(nextPage, self.parse)

		for job in response.css('div.jobsearch-SerpJobCard > div.title > a.jobtitle'):
			yield response.follow(job, self.parse)

			
		for b in response.css('div.jobsearch-JobComponent'):	
			job_title = response.css('h3.jobsearch-JobInfoHeader-title ::text').extract_first()
			employer = response.css('div.jobsearch-JobInfoHeader-subtitle ::text').extract_first()
			website = response.css('#viewJobButtonLinkContainer > div > a ::attr(href)').extract_first()
			job_description = ','.join(response.css('#jobDescriptionText ::text').extract())
			
			yield {
				'job-title': job_title,
				'employer': employer,
				'website': website,
				'job-description': job_description,
			}