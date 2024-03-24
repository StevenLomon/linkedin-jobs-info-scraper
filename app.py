import time, os, re, pickle, random, requests, math
import pandas  as pd
import streamlit as st
from rich import print, print_json

input_url = "https://www.linkedin.com/jobs/search/?currentJobId=3850239811&keywords=sem%20seo&origin=SWITCH_SEARCH_VERTICAL"

def get_total_number_of_results(response):
    paging = response.json().get('paging', {})

    total = None
    if paging:
        total = paging.get('total')
    
    return total

# We can only fetch 100 at a time
def split_total_in_chunks_of_100(total):
    chunks = [(i, min(i+100, total)) for i in range(0, total, 100)]
    return chunks

def get_job_posting_ids(response, start, stop):
    metadata = response.json().get('metadata', {})
    jobCardPrefetchQueries = metadata.get('jobCardPrefetchQueries', [])
    job_posting_ids_list = []

    if jobCardPrefetchQueries:
        prefetchJobPostingCardUrns = jobCardPrefetchQueries[0].get('prefetchJobPostingCardUrns', {})
        for job_posting in prefetchJobPostingCardUrns:
            job_posting_id = re.search(r"\d+", job_posting).group()
            job_posting_ids_list.append(job_posting_id)

    return job_posting_ids_list

def extract_linkedin_url_and_full_name(job_posting_id):
    api_request_url = f"https://www.linkedin.com/voyager/api/voyagerHiringDashJobHiringSocialHirersCards?jobPosting=urn%3Ali%3Afsd_jobPosting%3A{job_posting_id}&q=jobPosting"
    payload = {}
    headers = {
    'csrf-token': 'ajax:5371233139676576627',
    'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjg0MDU2OzI7MDIxZLMBMLTcKNFI+XOFChkDeYTioZ13bwCgrBw2moel0Qs=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711283633176%7EJAPP%2C00PNKdLCsk3RALmZlPoHhisVmNd0%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403241240565ed10e98-4f9c-45b3-8b4e-2c91c3e311e8AQHSQovhAxZsuoNIIhO8vfSDUSjwXhHn"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
    }
    response = requests.request("GET", api_request_url, headers=headers, data=payload)

    if response.status_code != 200:
        return None
    else:
        linkedin_url = None
        full_name = None

        elements = response.json().get('elements', [])
        if elements:
            linkedin_url = elements[0].get('navigationUrl')
            title = elements[0].get('title', {})
            if title:
                full_name = title.get('text')
        
        return (linkedin_url, full_name)

def split_and_clean_full_name(full_name):
    cleaned_name = re.sub(r'[^\w\s]', '', full_name, flags=re.UNICODE)
    name_parts = cleaned_name.split()
    first_name = name_parts[0] # We assume the first part will always be the first name after removing emojis etc
    last_name = name_parts[-1] if len(name_parts) > 1 else ''  # Check to avoid index error if name_parts is empty
    return (first_name, last_name)

def extract_job_title_and_company_name(job_posting_id):
    api_request_url = f"https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_posting_id}?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65"
    payload = {}
    headers = {
    'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AnalyticsSyncHistory=AQLQgW3RRkANCwAAAY5jOmkwk72r8IMTrd9st_hjdmoulqVl5geMen4LqgmF8K0AUn3R-jOxuSedvejsMpUyYg; lms_ads=AQE-j01C-ngGfAAAAY5jOmnPPxW1fk7yURo5p3BzckUP10_2GF31Wb6DTjp2ZQaXuFNEb99nBV3t4n9womVMaXKXpy9e5DeJ; lms_analytics=AQE-j01C-ngGfAAAAY5jOmnPPxW1fk7yURo5p3BzckUP10_2GF31Wb6DTjp2ZQaXuFNEb99nBV3t4n9womVMaXKXpy9e5DeJ; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq2bNXaXIRuV5eknJfRcJJy%252f5nqyjDnULhxqy9cd6iM21Cb7%252fhxAyWYV8%252fTNNXtTXAz2THy%252bS1UAUJ4C0TFJqZwlgKE1N6wCZBrbq1PYr27WbTaCjVCrA2Xi4%252bdIojAPbJKCM3N7t7VfD39gWluYQ%252fMQulpoiC0OWVKL%252bmdyMB1f2bBiWIjwD7yL%252fmXkbdpys%252bEA0dC3zukOo3gFYjVJIaYI%253d; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19806%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1711906882%7C6%7CMCAAMB-1711906882%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711309282s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; sdsc=22%3A1%2C1711302394031%7EJAPP%2C0%2FASzzgvclVA1rcG151Seh7fZ3vE%3D; li_mc=MTsyMTsxNzExMzAyNDk4OzI7MDIxH8iwcfXfDEtzPiAtqVhNwwrm3dw9onOmS74ikErmNJ8=; UserMatchHistory=AQJRDuzZNIG2_wAAAY5xm9Gxj5VlpKduNO94tLc3KgcQiC1tQBcPqnAdsbCdKVC_CLZRH0zVP9P6bT6CB8lowEfy4vocrB4yoDIa0bBYwFcyJuzMw3R9YpYx6Q44kj2pOW3jz_1Edu6U7aYfWZmFCWXwsPP9B7MB7Je59lyFALkH4xxejaRiZS4YJM5Dk1M30BYrywDR1zuUUbggixPSai4vT1UBlclj6kt7Cf4pyqnH-zJqq4fFLjZzkRCykOpzpLAsAM0zjOmsAwW2BfoLNZp9jHLWUHIhgIU4qD-0c55Lf7foJ6y-Dsn2hsNOeTPt5_TGC9g; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711303021:t=1711383469:v=2:sig=AQFYdoK2Srcqn6EfGJG8i0jCxb6cMO_G"; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzExMzAzNDEzOzI7MDIxGQP05JsWdH+T0k4V8WMWSbty3sS/FP0P48TMUQTQMPg=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711303409:t=1711383469:v=2:sig=AQGXHrUNzDp7ot1SM_08e6GRUJ6lKNMk"; sdsc=22%3A1%2C1711302394031%7EJAPP%2C0%2FASzzgvclVA1rcG151Seh7fZ3vE%3D',
    'csrf-token': 'ajax:5371233139676576627'
    }

    response = requests.request("GET", api_request_url, headers=headers, data=payload)

    job_title = None
    company_name = None

    job_title = response.json().get('title')

    companyDetails = response.json().get('companyDetails', {})
    if companyDetails:
        webJobPostingCompany = companyDetails.get('com.linkedin.voyager.deco.jobs.web.shared.WebJobPostingCompany', {})
        if webJobPostingCompany:
            companyResolutionResult = webJobPostingCompany.get('companyResolutionResult', {})
            if companyResolutionResult:
                company_name = companyResolutionResult.get('name')

    return (job_title, company_name)

def scrape_linkedin_and_show_progress(linkedin_job_url, total_results, progress_bar, text_placeholder):
    result_dataframe = pd.DataFrame(columns=['Förnamn', 'Efternamn', 'LinkedIn URL', 'Jobbtitel', 'Företag'])
    ranges = split_total_in_chunks_of_100(total_results)

    print(f"Starting the scrape! {total_results} to scrape")
    counter = 0

    for start, stop in ranges:
        if counter >= total_results:
            break
        print(f"Going through result {start} to {stop}")
        job_posting_list = get_job_posting_ids(linkedin_job_url, start, stop)

        temp_data_list = []

        for job_posting in job_posting_list:
            counter += 1
            if counter >= total_results:
                break

            linkedin_url, full_name = extract_linkedin_url_and_full_name(job_posting)
 
            if linkedin_url and full_name:
                first_name, last_name = split_and_clean_full_name(full_name)

                # Only if we have a name and linkedIn URL (there is a hiring team) do we need to 
                # check for job title and company name
                job_title, company_name = extract_job_title_and_company_name(job_posting)

                print(f"#{counter} : LinkedIn URL: {linkedin_url}, Name: {full_name}, Job title: {job_title}, Company: {company_name}")

                new_row = {'Förnamn': first_name, 'Efternamn': last_name, 'LinkedIn URL': linkedin_url,
                           'Jobbtitel': job_title, 'Företag': company_name}

                # Check if the new_row is a duplicate
                if new_row not in temp_data_list:
                    temp_data_list.append(new_row)
                else:
                    print("Duplicate found. Skipping.")
                    continue    
            
            # Update the progress bar and text after each job posting is processed
            text_placeholder.text(f"Processing {counter} / {total_results}")
            progress_bar.progress(counter / total_results)

    # Final update to ensure completion is shown
    if counter < total_results:
        text_placeholder.text(f"Processing completed! Total processed: {counter} / {total_results}")
        progress_bar.progress(1.0)  # Ensure progress bar is filled at the end
    else:
        text_placeholder.text(f"Processing {total_results} / {total_results}")
        progress_bar.progress(1.0)  # Ensure progress bar is filled at the end

    # Convert the list of dictionaries to a DataFrame and concatenate it with the existing result_dataframe
    new_data_df = pd.DataFrame(temp_data_list)
    result_dataframe = pd.concat([result_dataframe, new_data_df], ignore_index=True)

    return result_dataframe

def generate_csv(dataframe, result_name):
    if result_name.endswith('.csv'):
        result_name = result_name
    else:
        result_name = result_name + '.csv'
    dataframe.to_csv(result_name, index=False)
    return result_name

st.title('LinkedIn Job search URL to CSV Generator')

# User input for LinkedIn URL
linkedin_job_url = st.text_input('Enter LinkedIn Job URL:', '')
result_name = st.text_input('Enter a name for the csv:', '')
max_results_to_check = st.text_input('Enter maximum amounts of jobs to check (leave blank to scrape all jobs):', '')

# Button to generate CSV
if st.button('Generate CSV'):
    if linkedin_job_url:
        keyword = re.search(r'keywords=([^&]+)', linkedin_job_url).group(1)
        api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count=100&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start=0"
        
        payload = {}
        headers = {
        'csrf-token': 'ajax:5371233139676576627',
        'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjc2MTc0OzI7MDIxe9WcWZ2d6Bt7L96zCLaBjXpfuxnqB2ora17i0MVkktc=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
        }
        response = requests.request("GET", api_request_url, headers=headers, data=payload)

        total_number_of_results = get_total_number_of_results(response)

        if len(max_results_to_check) != 0 and int(max_results_to_check) < total_number_of_results:
            total_number_of_results = int(max_results_to_check)

        # Loading bar
        progress_bar = st.progress(0)
        text_placeholder = st.empty()

        scraped_data_df = scrape_linkedin_and_show_progress(response, total_number_of_results, progress_bar, text_placeholder)
        csv_file = generate_csv(scraped_data_df, result_name)
        
        st.success(f'CSV file generated: {csv_file}')
        # Download link
        with open(csv_file, "rb") as file:
            st.download_button(label="Download CSV", data=file, file_name=csv_file, mime='text/csv')
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
        
# def split_total_in_chunks_of_100(total):
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