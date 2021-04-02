## Begins superhero code https://gist.github.com/scrapehero/352286d0f9dee87990cd45c3f979e7cb 
from lxml import html, etree
from bs4 import BeautifulSoup
import requests
import re
import os
import sys
import unicodecsv as csv
import argparse
import json
import urllib.request
## try this proxies to avoid being blocked
proxy = {
 "http": "http://80.187.140.26.53:8080",
 "https": "http://80.187.140.26:8080",
}
def parse(keyword, place):

	headers = {	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'accept-encoding': 'gzip, deflate, sdch, br',
				'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
				'referer': 'https://www.glassdoor.com/',
				'upgrade-insecure-requests': '1',
				#'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                                'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
				'Cache-Control': 'no-cache',
				'Connection': 'keep-alive'
	}

	location_headers = {
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.01',
		'accept-encoding': 'gzip, deflate, sdch, br',
		'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
		'referer': 'https://www.glassdoor.com/',
		'upgrade-insecure-requests': '1',
		#'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive'
	}
	data = {"term": place,
			"maxLocationsToReturn": 10}

	location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"
	try:
		# Getting location id for search location
		print("Fetching location details")
		location_response = requests.post(location_url,  proxies=proxy, headers=location_headers, data=data).json()
		place_id = location_response[0]['locationId']
		job_litsting_url = 'https://www.glassdoor.com/Job/jobs.htm'
		# Form data to get job results
		data = {
			'clickSource': 'searchBtn',
			'sc.keyword': keyword,
			'locT': 'C',
			'locId': place_id,
			'jobType': ''
		}
		job_listings = []
		if place_id:
			response = requests.post(job_litsting_url, proxies=proxy, headers=headers, data=data)
			# extracting data from
			# https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=true&clickSource=searchBtn&typedKeyword=andr&sc.keyword=android+developer&locT=C&locId=1146821&jobType=
			parser = html.fromstring(response.text)
			# Making absolute url 
			base_url = "https://www.glassdoor.com"
			parser.make_links_absolute(base_url)

			XPATH_ALL_JOB = '//li[@class="jl"]'
			XPATH_NAME = './/a/text()'
			XPATH_JOB_URL = './/a/@href'
			XPATH_LOC = './/span[@class="subtle loc"]/text()'
			XPATH_COMPANY = './/div[@class="flexbox empLoc"]/div/text()'
			XPATH_SALARY = './/span[@class="green small"]/text()'

			listings = parser.xpath(XPATH_ALL_JOB)
			for job in listings:
				raw_job_name = job.xpath(XPATH_NAME)
				raw_job_url = job.xpath(XPATH_JOB_URL)
				raw_lob_loc = job.xpath(XPATH_LOC)
				raw_company = job.xpath(XPATH_COMPANY)
				raw_salary = job.xpath(XPATH_SALARY)

				# Cleaning data
				job_name = ''.join(raw_job_name).strip('–') if raw_job_name else None
				job_location = ''.join(raw_lob_loc) if raw_lob_loc else None
				raw_state = re.findall(",\s?(.*)\s?", job_location)
				state = ''.join(raw_state).strip()
				raw_city = job_location.replace(state, '')
				city = raw_city.replace(',', '').strip()
				company = ''.join(raw_company).replace('–','')
				salary = ''.join(raw_salary).strip()
				job_url = raw_job_url[0] if raw_job_url else None

				jobs = {
					"Name": job_name,
					"Company": company,
					"State": state,
					"City": city,
					"Salary": salary,
					"Location": job_location,
					"Url": job_url
				}
				job_listings.append(jobs)

			return job_listings
		else:
			print("location id not available")

	except:
		print("Failed to load locations")

if __name__ == "__main__":

	''' eg-:python 1934_glassdoor.py "Android developer", "new york" '''

	argparser = argparse.ArgumentParser()
	argparser.add_argument('keyword', help='job name', type=str)
	argparser.add_argument('place', help='job location', type=str)
	args = argparser.parse_args()
	keyword = args.keyword
	place = args.place
	print("Fetching job details")
	scraped_data = parse(keyword, place)
	print("Writing data to output file")
        #print(scraped_data)
	
	with open('%s-%s-job-results.csv' % (keyword, place), 'wb')as csvfile:
		fieldnames = ['Name', 'Company', 'State', 'City', 'Salary', 'Location', 'Url']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
		writer.writeheader()

		for it in range(0,len(scraped_data)):
                        ur=scraped_data[it] # lista 1
                        webur=ur.get("Url") # direccion url-esima
                        #req = urllib.request.Request(webur,proxies=proxy,data=None,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
                        req = urllib.request.Request(webur,data=None,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'})
                        sauce = urllib.request.urlopen(req).read()
                        soup=BeautifulSoup(sauce,'html.parser')
# Ends superhero code
			# Begins algorythm to count words
                        pattern=re.compile(r'sponsorship?[\S]',re.IGNORECASE)#'Sponsorship', 'sponsorship.', 'sponsorship'  but NOT 'sponsorships'
                        no_of_words=6
                        for elem in soup(text=pattern):
                                str=elem.parent.text
                                list=str.split(' ')
                                list_indices=[i for i,x in enumerate(list) if re.match(pattern,x.strip()+' ')]
                                for index in list_indices:
                                        start=index-no_of_words
                                        end=index+no_of_words+1
                                        if start<0:
                                                start=0
                                        varstri = ' '.join(list[start:end]).strip()
					
					# Skip words like unable, not, without...
										
                                        if re.compile(r'no[\.| ] |unable|no|not[\.| ] | without[\.| ] |without|not|requiring|don\'t| don\'t[\.| ]',re.IGNORECASE).search(varstri):
                                                #None#print('yes')
                                                '''if scraped_data:
                                                        for data in scraped_data:
                                                                scraped_data.remove(data)
								
                                                else: '''
                                                None
                                        else:
                                                print(webur)#print(varstri)
                        
                                                if scraped_data:
                                                        for data in scraped_data:
                                                                writer.writerow(data)
                                                else:
                                                        print("Your search for %s, in %s does not match any jobs"%(keyword,place))
#print(scraped_data.get("Url"))
