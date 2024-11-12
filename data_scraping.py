from bs4 import BeautifulSoup as bs
import pandas as pd
import requests as req

def scraping_job(position, location):
    position = position.lower().replace(' ', '-')
    location = location.lower().replace(' ', '-')
    base_url = f'https://id.jobstreet.com/id/{position}-jobs/in-{location}'

    response = req.get(base_url)
    soup = bs(response.text, 'html.parser')

    jobs = [] #akan di isi job title, link, company

    for job_card in soup.find_all('article',{'data-testid':'job-card'}):
        try:
            job_title = job_card.find('a', {'data-testid':'job-card-title'}).text.strip()
            company = job_card.find('a', {'data-type':'company'}).text.strip()
            job_link = job_card.find('a', {'data-testid':'job-card-title'})['href']

            jobs.append({
                'Title':job_title,
                'Company':company,
                'Link':'https://id.jobstreet.com'+job_link
            })
        except AttributeError:
            continue
    
    return jobs

input_job_position = input("Posisi yg dicari: ")
input_job_location = input("Lokasi yg dicari: ")

data_job = scraping_job(input_job_position, input_job_location)

# print(data_job)

data_frame = pd.DataFrame(data_job)

data_frame.to_excel('Lowongan Kerja.xlsx', index=False)

print("Finish")


