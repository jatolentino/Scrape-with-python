# Scrape-with-python
Based on superhero code (https://gist.github.com/scrapehero/352286d0f9dee87990cd45c3f979e7cb)

Scrape and output urls bypassing certain pages that have a particular string.
For instances :
Input a jobx in the search pan, then visit all the urls like the list below.
glassgoor-jobx-company1.com
glassgoor-jobx-company2.com
glassgoor-jobx-company3.com

Analize whether there is a specific string included in all the text of that website and avoid the site if there is a word which is not meant to be found.
For instances.
"Join our company, we provide health insurance and other type of ..."

- It is required that the phrase "health insurance" is present in the website, but what if there is something like "we don't provide health insurance"
So the string "don't" must be detected in a range of strings close to the phrase "health insurance", consequently the algorythm will discard this website if it finds that they don't provide self insurance, and will output a website that does provide that insurance.

