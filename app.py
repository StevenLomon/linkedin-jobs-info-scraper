import time, re, requests
import pandas  as pd
import streamlit as st
from rich import print, print_json
from io import BytesIO

def get_total_number_of_results(response, max_retries=3, delay=1):
    attempts = 0
    while attempts < max_retries:
        paging = response.json().get('paging', {})

        total = None
        if paging:
            total = paging.get('total')
        
        if isinstance(total, int):
            return total
    else:
        attempts += 1
        time.sleep(delay)

# We can only fetch 100 at a time
def split_total_into_batches_of_100(total):
    batches = [(i, i + 100) for i in range(0, total, 100)]
    # Adjust the last batch to not exceed the total
    if batches:
        batches[-1] = (batches[-1][0], total)
    return batches

def get_job_posting_ids(response):
    metadata = response.json().get('metadata', {})
    jobCardPrefetchQueries = metadata.get('jobCardPrefetchQueries', [])
    job_posting_ids_list = []

    if jobCardPrefetchQueries:
        prefetchJobPostingCardUrns = jobCardPrefetchQueries[0].get('prefetchJobPostingCardUrns', {})
        for job_posting in prefetchJobPostingCardUrns:
            job_posting_id = re.search(r"\d+", job_posting).group()
            job_posting_ids_list.append(job_posting_id)

    return job_posting_ids_list

def extract_linkedin_url_and_full_name(job_posting_id, max_retries=3, delay=1):
    api_request_url = f"https://www.linkedin.com/voyager/api/voyagerHiringDashJobHiringSocialHirersCards?jobPosting=urn%3Ali%3Afsd_jobPosting%3A{job_posting_id}&q=jobPosting"
    payload = {}
    headers = {
    'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; AnalyticsSyncHistory=AQIdocYcGpv1SwAAAY50EHPdIJOXJnTMkM1IqKRCN-xjtebWOGQgAfFoubhez_GPLJtHRjCZyED3AWxvqFIYaQ; lms_ads=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lms_analytics=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19808%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1711957673%7C6%7CMCAAMB-1711957673%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711360073s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq1E28xfVI%252fAcBePtgF5Ot6DvS%252fWB%252fLpFSKQIKiRvmofK47glv4UaszkM5BnaNumC19YjDA%252bGl3u278Mr4GVIBmsfuuHdZTKno6a2sJ4rLM%252bAj0eDcO%252boYUweonHKKXHh788Zkj2SGfNAE9x8tKHwo3oYtG%252fxfgSwib%252fnm2aRhCAFhh9Fc2E7uz1O5fgWEMg2cRnKiCKqv7XwXHsq%252f%252bEEn%252bw%253d; sdsc=22%3A1%2C1711355253815%7EJAPP%2C0OEHjuDn%2F8jB%2FwUYa7uP3OdX7FUs%3D; UserMatchHistory=AQKmb6P7HRl1UwAAAY50xgSC9LUMrQMVkRLljSnCrJ90HVCsa441cRTLL9qKlX6i1O796TJSEgL8GfunfiMFakp5E4NQGpZ4V40DJ_8zY1PSKP7Uw6QRian1QRspnn4lsOnJtQfSweE_GkLslrEZAoG4kyeZoZa6iUcGEXUMykKcxaIj84oR5PSXNVgwPgbtr3ZuND98f_e4iATtvE9E8zrkGmhiHh2D1rs631QMeNCVV1AynA_ecMI9_lXkqRsuxnccHsIsFaY9bLSDQGn1YFsIhYqrDHGUOalWaG7bGgI9WsdZ8sOMcZD_0FYxNlHKPSChbgw; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711356119:t=1711383469:v=2:sig=AQHd82x2wmOrEUinpWMUoqSumnm7thv9"; li_mc=MTsyMTsxNzExMzU3MzM2OzI7MDIxAdG1QK8bbcuKeDmJq0ey4DLjFZszCE7JjhRCegIKT/A=; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzExMzU3NDAyOzI7MDIxcChChZMT4OrNPcgxswKzL8h0/enN9c+0qgJAAAy2LmM=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711357847:t=1711383469:v=2:sig=AQEEx0S-hSoqzv3TS2j_b_c1EUsiWH4T"; sdsc=22%3A1%2C1711355253815%7EJAPP%2C0OEHjuDn%2F8jB%2FwUYa7uP3OdX7FUs%3D',
    'csrf-token': 'ajax:5371233139676576627'
    }

    attempts = 0
    while attempts < max_retries:
        response = requests.get(api_request_url, headers=headers, data=payload)
        if response.status_code == 200:
            linkedin_url = None
            full_name = None

            elements = response.json().get('elements', [])
            if elements:
                linkedin_url = elements[0].get('navigationUrl')
                title = elements[0].get('title', {})
                if title:
                    full_name = title.get('text')
            return (linkedin_url, full_name)
        else:
            attempts += 1
            time.sleep(delay)  # Wait before the next attempt

    return None, None  # Return None if all attempts fail

def split_and_clean_full_name(full_name):
    cleaned_name = re.sub(r'[^\w\s]', '', full_name, flags=re.UNICODE)
    name_parts = cleaned_name.split()
    first_name = name_parts[0] # We assume the first part will always be the first name after removing emojis etc
    last_name = name_parts[-1] if len(name_parts) > 1 else ''  # Check to avoid index error if name_parts is empty
    return (first_name, last_name)

def extract_company_info(job_posting_id, max_retries=3, delay=1):
    api_request_url = f"https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_posting_id}?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65"
    payload = {}
    headers = {
    'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; AnalyticsSyncHistory=AQIdocYcGpv1SwAAAY50EHPdIJOXJnTMkM1IqKRCN-xjtebWOGQgAfFoubhez_GPLJtHRjCZyED3AWxvqFIYaQ; lms_ads=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lms_analytics=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19808%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1711957673%7C6%7CMCAAMB-1711957673%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711360073s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq1E28xfVI%252fAcBePtgF5Ot6DvS%252fWB%252fLpFSKQIKiRvmofK47glv4UaszkM5BnaNumC19YjDA%252bGl3u278Mr4GVIBmsfuuHdZTKno6a2sJ4rLM%252bAj0eDcO%252boYUweonHKKXHh788Zkj2SGfNAE9x8tKHwo3oYtG%252fxfgSwib%252fnm2aRhCAFhh9Fc2E7uz1O5fgWEMg2cRnKiCKqv7XwXHsq%252f%252bEEn%252bw%253d; UserMatchHistory=AQKmb6P7HRl1UwAAAY50xgSC9LUMrQMVkRLljSnCrJ90HVCsa441cRTLL9qKlX6i1O796TJSEgL8GfunfiMFakp5E4NQGpZ4V40DJ_8zY1PSKP7Uw6QRian1QRspnn4lsOnJtQfSweE_GkLslrEZAoG4kyeZoZa6iUcGEXUMykKcxaIj84oR5PSXNVgwPgbtr3ZuND98f_e4iATtvE9E8zrkGmhiHh2D1rs631QMeNCVV1AynA_ecMI9_lXkqRsuxnccHsIsFaY9bLSDQGn1YFsIhYqrDHGUOalWaG7bGgI9WsdZ8sOMcZD_0FYxNlHKPSChbgw; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711356119:t=1711383469:v=2:sig=AQHd82x2wmOrEUinpWMUoqSumnm7thv9"; sdsc=22%3A1%2C1711358702924%7EJAPP%2C0Il%2B%2BEl2u2z0VpUMUw0YV3QiPP5w%3D; li_mc=MTsyMTsxNzExMzU5MjUyOzI7MDIxZpfdUzMSAl/jvqRDLzR0Bmsl0ivbeBqjWAv0E8v9JRA=; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzExMzU5MzQ0OzI7MDIxyqTlqWTdQJPWNxDh/xbiQT4itWjB7o6jo2B4Ot+BQKY=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711358640:t=1711383469:v=2:sig=AQF9ncvYxxF7o-JLHiRTCjEY4zv9Awqe"; sdsc=22%3A1%2C1711358702924%7EJAPP%2C0Il%2B%2BEl2u2z0VpUMUw0YV3QiPP5w%3D',
    'csrf-token': 'ajax:5371233139676576627'
    }

    attempts = 0
    while attempts < max_retries:
        response = requests.request("GET", api_request_url, headers=headers, data=payload)
        if response.status_code == 200:
            job_title = None
            company_name = None
            employee_count = None
            company_url = None

            job_title = response.json().get('title')

            companyDetails = response.json().get('companyDetails', {})
            if companyDetails:
                WebJobPostingCompany = companyDetails.get('com.linkedin.voyager.deco.jobs.web.shared.WebJobPostingCompany', {})
                if WebJobPostingCompany:
                    companyResolutionResult = WebJobPostingCompany.get('companyResolutionResult', {})
                    if companyResolutionResult:
                        company_name = companyResolutionResult.get('name')
                        employee_count = companyResolutionResult.get('staffCount')
                        company_url = companyResolutionResult.get('url')

            return (job_title, company_name, employee_count, company_url)
        else:
            attempts += 1
            time.sleep(delay)
    
    return None, None

def scrape_linkedin_and_show_progress(keyword, total_results, progress_bar, text_placeholder):
    result_dataframe = pd.DataFrame(columns=['Hiring Team', 'Förnamn', 'Efternamn', 'LinkedIn URL', 'Jobbtitel som sökes', 'Jobbannons-url', 'Företag', 'Antal anställda', 'Företagssegment', 'Företags-url'])
    print(f"Keyword: {keyword}")
    batches = split_total_into_batches_of_100(total_results)
    print(batches)

    print(f"Starting the scrape! {total_results} to scrape")
    counter = 0
    temp_data_list = []
    all_ids = []

    for i, (start, stop) in enumerate(batches):
        batch_size = stop - start
        api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count={batch_size}&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start={start}"

        payload = {}
        headers = {
        'csrf-token': 'ajax:5371233139676576627',
        'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjc2MTc0OzI7MDIxe9WcWZ2d6Bt7L96zCLaBjXpfuxnqB2ora17i0MVkktc=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
        }
        
        response = requests.request("GET", api_request_url, headers=headers, data=payload)
        
        if response.status_code == 200:
            # Fetch the job posting IDs from the response
            job_posting_list = get_job_posting_ids(response)
            all_ids.extend(job_posting_list)

            # Process the batch
            for job_posting in job_posting_list:
                print(f"Processing job posting #{job_posting}")
                linkedin_url, full_name = extract_linkedin_url_and_full_name(job_posting)
                job_title, company_name, employee_count, company_url = extract_company_info(job_posting)

                # Fetch company segment from company linkedin url
                try:
                    print(company_url)
                    company_response = requests.get(company_url)
                    webpage_html = company_response.text
                    soup = BeautifulSoup(webpage_html, 'html.parser')
                    div_elements = soup.find_all('div', class_='org-top-card-summary-info-list__info-item')
                    print(div_elements)
                    # [0].get_text(strip=True)
                    company_segment = None
                except:
                    print("Error fetching company segment")
                    company_segment = None
            
                if linkedin_url and full_name:
                    first_name, last_name = split_and_clean_full_name(full_name)

                    print(f"#{counter} : LinkedIn URL: {linkedin_url}, Name: {full_name}, Job title: {job_title}, Company: {company_name}")

                    new_row = {'Hiring Team': 'Ja', 'Förnamn': first_name, 'Efternamn': last_name, 'LinkedIn URL': linkedin_url,
                            'Jobbtitel som sökes': job_title, 'Jobbannons-url': f"https://www.linkedin.com/jobs/search/?currentJobId={job_posting}&geoId=105117694&keywords=sem%20seo&location=Sweden", 
                            'Företag': company_name, 'Antal anställda': employee_count, 'Företagssegment': company_segment, 'Företags-url': company_url}

                    # Check if the new_row is a duplicate
                    if new_row not in temp_data_list:
                        temp_data_list.append(new_row)
                    else:
                        print("Duplicate found. Skipping.")  
                else:
                    print(f"#{counter} : Could not fetch name and/or url. LinkedIn URL: {linkedin_url}, Name: {full_name}. Trying other way...")

                    # Look through the company page
                    company_keyword = None
                    if employee_count < 100:
                        company_keyword = "CEO"
                    else:
                        company_keyword = "CMO"

                    people_page = f"{company_url}/people/keywords={company_keyword}"

                    new_row = {'Hiring Team': 'Nej', 'Förnamn': None, 'Efternamn': None, 'LinkedIn URL': None,
                            'Jobbtitel som sökes': job_title, 'Jobbannons-url': f"https://www.linkedin.com/jobs/search/?currentJobId={job_posting}&geoId=105117694&keywords=sem%20seo&location=Sweden", 
                            'Företag': company_name, 'Antal anställda': employee_count, 'Företagssegment': company_segment, 'Företags-url': company_url}

                    # Check if the new_row is a duplicate
                    if new_row not in temp_data_list:
                        temp_data_list.append(new_row)
                    else:
                        print("Duplicate found. Skipping.")  

                counter += 1
                    
                # Update the progress bar and text after each job posting is processed
                progress = counter / total_results
                progress = min(max(progress, 0.0), 1.0)  # Clamp the progress value
                progress_bar.progress(progress)
                text_placeholder.text(f"Processing {counter} / {total_results}")

            # Print the counts after each request
            print(f"After request batch #{i+1}: Total IDs fetched - {len(all_ids)}. Unique IDs - {len(set(all_ids))}")
            time.sleep(1) # Wait 1 second until next batch
        else:
            print(f"Request for batch {start}-{stop} failed with status code: {response.status_code}")
            # Handle the failure accordingly, e.g., retry or log error

    # Final update outside the loop to ensure progress is marked complete
    text_placeholder.text(f"Processing completed! Total processed: {counter} / {total_results}")
    progress_bar.progress(1.0)  # Ensure the progress bar is full at completion

    # Convert the list of dictionaries to a DataFrame and concatenate it with the existing result_dataframe
    new_data_df = pd.DataFrame(temp_data_list)
    result_dataframe = pd.concat([result_dataframe, new_data_df], ignore_index=True)

    print(f"Done. Results:\nTotal found in the request: {total_results}\nTotal fetched succesfully: {len(all_ids)}\nTotal unique ids: {len(set(all_ids))}\nTotal hiring team available: {len(result_dataframe)}")

    # Return the resulting dataframe as well as a set with everything we print out after the scrape. Bad practice, I know :))
    return [result_dataframe, (len(all_ids), len(set(all_ids)), len(result_dataframe))]

def generate_csv(dataframe, result_name):
    if result_name.endswith('.csv'):
        result_name = result_name
    else:
        result_name = result_name + '.csv'
    dataframe.to_csv(result_name, index=False)
    return result_name

def generate_excel(dataframe, result_name):
    if result_name.endswith('.xlsx'):
        result_name = result_name
    else:
        result_name = result_name + '.xlsx'
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output

st.title('LinkedIn Job search URL to CSV Generator')

# User input for LinkedIn URL
linkedin_job_url = st.text_input('Enter URL from the LinkedIn Job search:', '')
result_name = st.text_input('Enter a name for the resulting csv/Excel file:', '')
max_results_to_check = st.text_input('Enter maximum amounts of jobs to check (leave blank to scrape all available jobs for the query):', '')

# Radio button to choose the file format
file_format = st.radio("Choose the file format for download:", ('csv', 'xlsx'))

# Button to the result file
if st.button('Generate File'):
    if linkedin_job_url:
        # Loading bar
        progress_bar = st.progress(0)
        text_placeholder = st.empty()
        
        keyword = re.search(r'keywords=([^&]+)', linkedin_job_url).group(1)
        api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count=100&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start=0"
        
        payload = {}
        headers = {
        'csrf-token': 'ajax:5371233139676576627',
        'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjc2MTc0OzI7MDIxe9WcWZ2d6Bt7L96zCLaBjXpfuxnqB2ora17i0MVkktc=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
        }

        max_retries = 3
        delay = 1
        attempts = 0
        while attempts < max_retries:
            response = requests.request("GET", api_request_url, headers=headers, data=payload)
            if response.status_code == 200:
                total_number_of_results = get_total_number_of_results(response)

                if len(max_results_to_check) != 0 and int(max_results_to_check) < total_number_of_results:
                    total_number_of_results = int(max_results_to_check)

                scraped_data_df, (total_fetched, total_unique, total_hiring_team) = scrape_linkedin_and_show_progress(keyword, total_number_of_results, progress_bar, text_placeholder)
                st.text(f"Total job posting ids found in the request: {total_number_of_results}\nTotal fetched succesfully: {total_fetched}\nTotal unique ids: {total_unique}\nTotal with hiring team available: {total_hiring_team}")

                if file_format == 'csv':
                    csv_file = generate_csv(scraped_data_df, result_name)
                    with open(csv_file, "rb") as file:
                        st.download_button(label="Download CSV", data=file, file_name=csv_file, mime='text/csv')
                    st.success(f'CSV file generated: {csv_file}')
                    break
                elif file_format == 'xlsx':
                    excel_file = generate_excel(scraped_data_df, result_name)
                    st.download_button(label="Download Excel", data=excel_file, file_name=f"{result_name}.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    st.success(f'Excel file generated: {result_name}.xlsx')
                    break
            else:
                attempts += 1
                time.sleep(delay)  # Wait before the next attempt
        
        if attempts == 3:
            st.error('Unable to create a valid request with the given LinkedIn URL.')

    else:
        st.error('Please enter a valid LinkedIn URL.')


# Code graveyard :)
# currentJobId = input[input.find("currentJobId=")+len("currentJobId="):input.find("currentJobId=")+len("currentJobId=")+10]
# currentJobId = re.search(r'currentJobId=(\d+)', input_url).group(1)
# keyword = input_url[input_url.find("keywords=")+len("keywords="):input_url.rfind("&")]
# keyword = re.search(r'keywords=([^&]+)', input_url).group(1)
# keyword_clean = keyword.replace("%20", " ").strip()
# # url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)"
# url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count={num_of_results}&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start=0"
# # url = f"https://www.linkedin.com/voyager/api/graphql?variables=(cardSectionTypes:List(HIRING_TEAM_CARD),jobPostingUrn:urn%3Ali%3Afsd_jobPosting%3A3845653892,includeSecondaryActionsV2:true)&queryId=voyagerJobsDashJobPostingDetailSections.61a1d2cc430218b6e70266051f4d514b"
# url = f"https://www.linkedin.com/voyager/api/graphql?variables=(cardSectionTypes:List(HIRING_TEAM_CARD),jobPostingUrn:urn%3Ali%3Afsd_jobPosting%3A3765078991,includeSecondaryActionsV2:true)&queryId=voyagerJobsDashJobPostingDetailSections.61a1d2cc430218b6e70266051f4d514b"

# payload = {}
# headers = {
#   'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; sdsc=22%3A1%2C1710858906178%7EJAPP%2C0xEIgf1wexK6ckr83inbCVKAcTqI%3D; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AnalyticsSyncHistory=AQLQgW3RRkANCwAAAY5jOmkwk72r8IMTrd9st_hjdmoulqVl5geMen4LqgmF8K0AUn3R-jOxuSedvejsMpUyYg; lms_ads=AQE-j01C-ngGfAAAAY5jOmnPPxW1fk7yURo5p3BzckUP10_2GF31Wb6DTjp2ZQaXuFNEb99nBV3t4n9womVMaXKXpy9e5DeJ; lms_analytics=AQE-j01C-ngGfAAAAY5jOmnPPxW1fk7yURo5p3BzckUP10_2GF31Wb6DTjp2ZQaXuFNEb99nBV3t4n9womVMaXKXpy9e5DeJ; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvqwEPtNDIm57sxDEhWE7kvw8fC5u3jMvAKkvp%252fotUqPYieNgLFCCANfXirRCWZuLFSPdYL21J5slhS%252bQ1o%252fV2tDhrboPn27TYxYN3FUTDJvWhxaVME1vC3nfaq%252b2TOyoU392iU6cthqH%252fLCvPTWtubi48HjubwzjAE4baM%252bY%252bSAuJvXU9FGXao1fxLuAeo%252fVJlo13MP%252bcqsPuAX6kSRrUrFQ%253d; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19806%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1711790369%7C6%7CMCAAMB-1711790369%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711192769s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; li_mc=MTsyMTsxNzExMTkwMjE1OzI7MDIxyRFtLCwn+pkNNW9oYAvY5RDLHGa7S0son4v0fwpeczI=; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_g_recent_logout=v=1&true; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; UserMatchHistory=AQJH9HVExKuEvQAAAY5q58JbFMoNxuK_4yHeRYryrMvAJHh4tJorRwgK13vsaO617yyfQhr3vKz2e6SnW2YP-8F_8xqIz_SMfNiyK-higtiBwc9CLSQnZgKfiC9WrmFFPnKpn8r1UDejBpUXRoHbhn3dnqPLrGEdbjpPkJHZ56LOnn5g1EmqSShtZhu7XK5iOhKLJR5ESXYhl8tgl-5ObCPDup6qlc7g2tZ9hKXoBg8vTrGdyVZhoO0HzxmovdosFQMPpcX-TjaxBXVz6onyjfxd5XXxlB1sR-h_AbkJ-grI3v9oH1tRRFA1MU0nkh2K4bReInY; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4151:u=247:x=1:i=1711190558:t=1711265066:v=2:sig=AQEhbOHG6b2NMBSek7ju52SyqY9s2vNB"; bcookie="v=2&4f26c9a6-f950-41d8-82cc-b41ec3caafa5"; li_mc=MTsyMTsxNzExMjYyNTI1OzI7MDIxxr788LY2gp/ql7Hm1zTLkN7QbgdW0J00Cs1RP/eztJ0=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; JSESSIONID="ajax:5371233139676576627"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm',
#   'csrf-token': 'ajax:5371233139676576627'
# }

# payload = {}
# headers = {
#   'csrf-token': 'ajax:5371233139676576627',
#   'Cookie': 'bcookie="v=2&4f26c9a6-f950-41d8-82cc-b41ec3caafa5"; li_mc=MTsyMTsxNzExMjczOTA0OzI7MDIxJbsswKdLOR/MLFXw1jYNkR1ZxbB9qNb6gz/ltll39F0=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&20240324095144fd05fb1b-7f78-4180-84c1-133606441c75AQH2JA58kNsAk1vOapFltTeRA04_zidE"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# keyword = response.json()['metadata']['keywords']
# # number_of_results = int(response.json()['metadata']['subtitle']['text'].split()[0])
# number_of_results = response.json()['paging']['total']
# all_jobs = response.json()['elements']
# print(number_of_results)
# print(len(all_jobs))
# posterIds = []
# for job in all_jobs:
#     posterId = job['jobCardUnion']['jobPostingCard']['jobPosting'].get('posterId', None)
#     posterIds.append(posterId)
# print(posterIds)

# linkedin_url = response.json()['data']['jobsDashJobPostingDetailSectionsByCardSectionTypes']['elements'][0]['jobPostingDetailSection'][0]['hiringTeamCard']['image'].get('navigationUrl', None)
# data = response.json().get('data', {})
# jobsDashJobPostingDetailSectionsByCardSectionTypes = data.get('jobsDashJobPostingDetailSectionsByCardSectionTypes', {})
# elements = jobsDashJobPostingDetailSectionsByCardSectionTypes.get('elements', [])

# if elements:
#     jobPostingDetailSection = elements[0].get('jobPostingDetailSection', [])
#     if jobPostingDetailSection:
#         hiringTeamCard = jobPostingDetailSection[0].get('hiringTeamCard', {})
#         if hiringTeamCard:
#             linkedin_url = hiringTeamCard.get('navigationUrl', None)
#             title = hiringTeamCard.get('title', {})
#             if title:
#                 full_name = title.get('text', None)

# print(linkedin_url)
# print(full_name)
# data = response.json().get('data', {})
# jobsDashJobPostingDetailSectionsByCardSectionTypes = data.get('jobsDashJobPostingDetailSectionsByCardSectionTypes', {})
# elements = jobsDashJobPostingDetailSectionsByCardSectionTypes.get('elements', [])

# if elements:
#     jobPostingDetailSection = elements[0].get('jobPostingDetailSection', [])
#     if jobPostingDetailSection:
#         hiringTeamCard = jobPostingDetailSection[0].get('hiringTeamCard', {})
#         if hiringTeamCard:
#             linkedin_url = hiringTeamCard.get('navigationUrl')
#             title = hiringTeamCard.get('title', {})
#             if title:
#                 full_name = title.get('text')
        
# def split_total_into_batches_of_100(total):
#     whole = math.floor(total / 100)
#     print(whole)
#     result = []

#     start = 0
#     for i in range(whole):
#         current_set = (start, (i+1)*100)
#         start += 100
#         result.append(current_set)
#     result.append((whole*100, whole*100 + total%100))
    
#     return result
        
# linkedin_job_url = "https://www.linkedin.com/jobs/search/?currentJobId=3836861341&keywords=sem%20seo&origin=SWITCH_SEARCH_VERTICAL"
# keyword = re.search(r'keywords=([^&]+)', linkedin_job_url).group(1)
# print(f"Keyword: {keyword}")
# total_number_of_results = 664
# batches = split_total_into_batches_of_100(total_number_of_results)
# print(batches)

# all_ids = []

# for batch in batches:
#     start, stop = batch

#     api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count={stop}&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start={start}"
        
#     payload = {}
#     headers = {
#     'csrf-token': 'ajax:5371233139676576627',
#     'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjc2MTc0OzI7MDIxe9WcWZ2d6Bt7L96zCLaBjXpfuxnqB2ora17i0MVkktc=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
#     }
#     response = requests.request("GET", api_request_url, headers=headers, data=payload)

#     sem_seo_ids = get_job_posting_ids(response)
#     all_ids.extend(sem_seo_ids)

# print(f"Done. All ids: {all_ids}\nUnique ids: {list(set((all_ids)))}")
# print(f"Initial length: {len(all_ids)}. Length of unique: {len(list(set(all_ids)))}")
        
# linkedin_job_url = "https://www.linkedin.com/jobs/search/?currentJobId=3845996635&keywords=sem%20seo&origin=SWITCH_SEARCH_VERTICAL"
# keyword = re.search(r'keywords=([^&]+)', linkedin_job_url).group(1)
# total_number_of_results = 815
# batches = split_total_into_batches_of_100(total_number_of_results)

# all_ids = []

# for i, (start, stop) in enumerate(batches):
#     # Construct the API request URL using `start` and the `batch_size`
#     batch_size = stop - start
#     api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count={batch_size}&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start={start}"
#     print(f"Batch request {i+1}: API Request URL: {api_request_url}")

#     payload = {}
#     headers = {
#     'csrf-token': 'ajax:5371233139676576627',
#     'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjc2MTc0OzI7MDIxe9WcWZ2d6Bt7L96zCLaBjXpfuxnqB2ora17i0MVkktc=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
#     }
    
#     response = requests.request("GET", api_request_url, headers=headers, data=payload)
    
#     if response.status_code == 200:
#         # Fetch the job posting IDs from the response
#         sem_seo_ids = get_job_posting_ids(response)
#         all_ids.extend(sem_seo_ids)

#         if len(sem_seo_ids) >= 3:
#             print(f"First 3 IDs: {sem_seo_ids[0]}, {sem_seo_ids[1]}, {sem_seo_ids[2]} ; Last 3 IDs: {sem_seo_ids[-1]}, {sem_seo_ids[-2]}, {sem_seo_ids[-3]}")
#         else:
#             print(f"IDs in the last batch: {', '.join(sem_seo_ids)}")

#         # Print the counts after each request
#         print(f"After request {i+1}: Total IDs fetched - {len(all_ids)}. Unique IDs - {len(set(all_ids))}")
#     else:
#         print(f"Request for batch {start}-{stop} failed with status code: {response.status_code}")
#         # Handle the failure accordingly, e.g., retry or log error

# print(f"Done. All ids: {len(all_ids)}\nUnique ids: {len(set(all_ids))}")
        
# for id in sem_seo_ids:
#     lurl, name = extract_linkedin_url_and_full_name(id)
#     title, company = extract_job_title_and_company_name(id)
#     print(f"LURL: {lurl}, Name: {name}, Title: {title}, Company: {company}")
        

# # Completion checks should account for possible early stopping
# if counter >= total_results:
#     text_placeholder.text(f"Processing completed! Total processed: {total_results} / {total_results}")
#     progress_bar.progress(1.0)  # Ensure progress bar is filled at the end
# else:
#     text_placeholder.text(f"Processing completed! Total processed: {counter} / {total_results}")
#     progress_bar.progress(1.0)  # Progress bar reflects actual number processed
        
# batches = split_total_into_batches_of_100(total_results)
# print(f"batches: {batches}")

# print(f"Starting the scrape! {total_results} to scrape")
# counter = 0
# temp_data_list = []
# unique_ids = set()

# # Outer loop for batches
# for start, stop in batches:
#     print(f"Start: {start}, Stop: {stop}")
#     batch_size = stop - start
#     print(f"batch size: {batch_size}")
#     api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count={batch_size}&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start={start}"
#     print(f"req url: {api_request_url}")

#     payload = {}
#     headers = {
#     'csrf-token': 'ajax:5371233139676576627',
#     'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjc2MTc0OzI7MDIxe9WcWZ2d6Bt7L96zCLaBjXpfuxnqB2ora17i0MVkktc=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
#     }

#     max_retries = 3
#     delay = 1
#     attempts = 0
    
#     while attempts < max_retries:
#         response = requests.request("GET", api_request_url, headers=headers, data=payload)
#         if response.status_code == 200:
#             job_posting_list = get_job_posting_ids(response)

#             for job_posting in job_posting_list:
#                 print(f"Processing job posting #{job_posting}")
#                 if job_posting in unique_ids:
#                     print("Id already processed. Skipping")
#                 else:
#                     print("New id. Processing job posting")
#                     unique_ids.add(job_posting)
#                     linkedin_url, full_name = extract_linkedin_url_and_full_name(job_posting)
        
#                     if linkedin_url and full_name:
#                         first_name, last_name = split_and_clean_full_name(full_name)

#                         # Only if we have a name and linkedIn URL (there is a hiring team) do we need to 
#                         # check for job title and company name
#                         job_title, company_name = extract_job_title_and_company_name(job_posting)

#                         print(f"#{counter} : LinkedIn URL: {linkedin_url}, Name: {full_name}, Job title: {job_title}, Company: {company_name}")

#                         new_row = {'Förnamn': first_name, 'Efternamn': last_name, 'LinkedIn URL': linkedin_url,
#                                 'Jobbtitel': job_title, 'Företag': company_name}

#                         # Check if the new_row is a duplicate
#                         if new_row not in temp_data_list:
#                             temp_data_list.append(new_row)
#                         else:
#                             print("Duplicate found. Skipping.")  
#                     else:
#                         print(f"#{counter} : Could not fetch name and/or url. LinkedIn URL: {linkedin_url}, Name: {full_name}")
#                 counter += 1
                
#                 # Update the progress bar and text after each job posting is processed
#                 progress = counter / total_results
#                 progress = min(max(progress, 0.0), 1.0)  # Clamp the progress value
#                 progress_bar.progress(progress)
#                 text_placeholder.text(f"Processing {counter} / {total_results}")
        
#                 if counter >= total_results:
#                     break
#             if counter >= total_results:
#                 break
            
#         else:
#             attempts += 1
#             time.sleep(delay)  # Wait before the next attempt

#     if counter >= total_results:
#         break

# # Final update outside the loop to ensure progress is marked complete
# text_placeholder.text(f"Processing completed! Total processed: {counter} / {total_results}")
# progress_bar.progress(1.0)  # Ensure the progress bar is full at completion

# # Convert the list of dictionaries to a DataFrame and concatenate it with the existing result_dataframe
# new_data_df = pd.DataFrame(temp_data_list)
# result_dataframe = pd.concat([result_dataframe, new_data_df], ignore_index=True)

# print(f"Done. Total number of ids: {total_number_of_results}\nUnique ids: {len(unique_ids)}\nJobs with Hiring team available to scrape: {len(result_dataframe)}")

#linkedin_job_url = "https://www.linkedin.com/jobs/search/?currentJobId=3836861341&keywords=sem%20seo&origin=SWITCH_SEARCH_VERTICAL"
#keyword = re.search(r'keywords=([^&]+)', linkedin_job_url).group(1)