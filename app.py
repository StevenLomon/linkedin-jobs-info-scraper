import time, re, requests, asyncio, aiohttp
import pandas  as pd
import streamlit as st
from rich import print, print_json
from io import BytesIO

def get_total_number_of_results(keyword, max_retries=3, delay=1):
    api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count=100&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start=0"
        
    payload = {}
    headers = {
    'csrf-token': 'ajax:5371233139676576627',
    'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjc2MTc0OzI7MDIxe9WcWZ2d6Bt7L96zCLaBjXpfuxnqB2ora17i0MVkktc=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
    }

    for attempt in range(max_retries):
        try:
            response = requests.request("GET", api_request_url, headers=headers, data=payload)
            if response.status_code == 200:
                total = None
                paging = response.json().get('paging', {})
                if paging:
                    total = paging.get('total')
                
                if isinstance(total, int):
                    return total
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(delay)
    return None     

# We can only fetch 100 at a time
def split_total_into_batches_of_100(total):
    batches = [(i, i + 100) for i in range(0, total, 100)]
    # Adjust the last batch to not exceed the total
    if batches:
        batches[-1] = (batches[-1][0], total)
    return batches

async def fetch_job_posting_ids(keyword, batch, sem, session, max_retries=3, delay=1):
    start, stop = batch
    print(f"Start: {start}, Stop: {stop}")
    batch_size = stop - start
    print(f"Batch size: {batch_size}")

    api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count={batch_size}&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start={start}"
    headers = {
    'csrf-token': 'ajax:5371233139676576627',
    'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjc2MTc0OzI7MDIxe9WcWZ2d6Bt7L96zCLaBjXpfuxnqB2ora17i0MVkktc=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
    }

    async with sem:
        for attempt in range(max_retries):
            try:
                async with session.get(api_request_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()

                        job_posting_ids_list = []
                        prefetchJobPostingCardUrns = data.get('metadata', {}) \
                            .get('jobCardPrefetchQueries', [{}])[0] \
                            .get('prefetchJobPostingCardUrns', {})
                        for job_posting in prefetchJobPostingCardUrns:
                            job_posting_id_search = re.search(r"(\d+)", job_posting)
                            job_posting_id = job_posting_id_search.group(1) if job_posting_id_search else None
                            job_posting_ids_list.append(job_posting_id)
            except Exception as e:
                print(f"Request failed: {e}")
                await asyncio.sleep(delay)
    return job_posting_ids_list #Return the list, even if its empty

async def extract_all_job_posting_ids(keyword, batches, sem, session):
    tasks = [fetch_job_posting_ids(keyword, batch, sem, session) for batch in batches]
    results = await asyncio.gather(*tasks)
    # Flatten the list of lists
    job_posting_ids = [id for sublist in results for id in sublist]
    return job_posting_ids

async def extract_full_name_bio_and_linkedin_url(job_posting_id, sem, session, max_retries=3, delay=1):
    api_request_url = f"https://www.linkedin.com/voyager/api/voyagerHiringDashJobHiringSocialHirersCards?jobPosting=urn%3Ali%3Afsd_jobPosting%3A{job_posting_id}&q=jobPosting"
    headers = {
    'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; AnalyticsSyncHistory=AQIdocYcGpv1SwAAAY50EHPdIJOXJnTMkM1IqKRCN-xjtebWOGQgAfFoubhez_GPLJtHRjCZyED3AWxvqFIYaQ; lms_ads=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lms_analytics=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19808%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1711957673%7C6%7CMCAAMB-1711957673%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711360073s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq1E28xfVI%252fAcBePtgF5Ot6DvS%252fWB%252fLpFSKQIKiRvmofK47glv4UaszkM5BnaNumC19YjDA%252bGl3u278Mr4GVIBmsfuuHdZTKno6a2sJ4rLM%252bAj0eDcO%252boYUweonHKKXHh788Zkj2SGfNAE9x8tKHwo3oYtG%252fxfgSwib%252fnm2aRhCAFhh9Fc2E7uz1O5fgWEMg2cRnKiCKqv7XwXHsq%252f%252bEEn%252bw%253d; sdsc=22%3A1%2C1711355253815%7EJAPP%2C0OEHjuDn%2F8jB%2FwUYa7uP3OdX7FUs%3D; UserMatchHistory=AQKmb6P7HRl1UwAAAY50xgSC9LUMrQMVkRLljSnCrJ90HVCsa441cRTLL9qKlX6i1O796TJSEgL8GfunfiMFakp5E4NQGpZ4V40DJ_8zY1PSKP7Uw6QRian1QRspnn4lsOnJtQfSweE_GkLslrEZAoG4kyeZoZa6iUcGEXUMykKcxaIj84oR5PSXNVgwPgbtr3ZuND98f_e4iATtvE9E8zrkGmhiHh2D1rs631QMeNCVV1AynA_ecMI9_lXkqRsuxnccHsIsFaY9bLSDQGn1YFsIhYqrDHGUOalWaG7bGgI9WsdZ8sOMcZD_0FYxNlHKPSChbgw; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711356119:t=1711383469:v=2:sig=AQHd82x2wmOrEUinpWMUoqSumnm7thv9"; li_mc=MTsyMTsxNzExMzU3MzM2OzI7MDIxAdG1QK8bbcuKeDmJq0ey4DLjFZszCE7JjhRCegIKT/A=; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzExMzU3NDAyOzI7MDIxcChChZMT4OrNPcgxswKzL8h0/enN9c+0qgJAAAy2LmM=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711357847:t=1711383469:v=2:sig=AQEEx0S-hSoqzv3TS2j_b_c1EUsiWH4T"; sdsc=22%3A1%2C1711355253815%7EJAPP%2C0OEHjuDn%2F8jB%2FwUYa7uP3OdX7FUs%3D',
    'csrf-token': 'ajax:5371233139676576627'
    }

    async with sem:
        for attempt in range(max_retries):
            try:
                async with session.get(api_request_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        elements = data.get('elements', [{}])
                        full_name = elements[0].get('title', {}).get('text', None)
                        bio = elements[0].get('subtitle', {}).get('text', None)
                        linkedin_url = elements[0].get('navigationUrl')                        
                        return (full_name, bio, linkedin_url)
            except Exception as e:
                print(f"Request failed: {e}")
                await asyncio.sleep(delay)
    return None, None, None  # Return None if all attempts fail

def split_and_clean_full_name(full_name):
    cleaned_name = re.sub(r'[^\w\s]', '', full_name, flags=re.UNICODE)
    name_parts = cleaned_name.split()
    first_name = name_parts[0] # We assume the first part will always be the first name after removing emojis etc
    last_name = name_parts[-1] if len(name_parts) > 1 else ''  # Check to avoid index error if name_parts is empty
    return (first_name, last_name)

async def extract_company_info(job_posting_id, sem, session, max_retries=3, delay=1):
    api_request_url = f"https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_posting_id}?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65"
    headers = {
    'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; AnalyticsSyncHistory=AQIdocYcGpv1SwAAAY50EHPdIJOXJnTMkM1IqKRCN-xjtebWOGQgAfFoubhez_GPLJtHRjCZyED3AWxvqFIYaQ; lms_ads=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lms_analytics=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19808%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1711957673%7C6%7CMCAAMB-1711957673%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711360073s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq1E28xfVI%252fAcBePtgF5Ot6DvS%252fWB%252fLpFSKQIKiRvmofK47glv4UaszkM5BnaNumC19YjDA%252bGl3u278Mr4GVIBmsfuuHdZTKno6a2sJ4rLM%252bAj0eDcO%252boYUweonHKKXHh788Zkj2SGfNAE9x8tKHwo3oYtG%252fxfgSwib%252fnm2aRhCAFhh9Fc2E7uz1O5fgWEMg2cRnKiCKqv7XwXHsq%252f%252bEEn%252bw%253d; UserMatchHistory=AQKmb6P7HRl1UwAAAY50xgSC9LUMrQMVkRLljSnCrJ90HVCsa441cRTLL9qKlX6i1O796TJSEgL8GfunfiMFakp5E4NQGpZ4V40DJ_8zY1PSKP7Uw6QRian1QRspnn4lsOnJtQfSweE_GkLslrEZAoG4kyeZoZa6iUcGEXUMykKcxaIj84oR5PSXNVgwPgbtr3ZuND98f_e4iATtvE9E8zrkGmhiHh2D1rs631QMeNCVV1AynA_ecMI9_lXkqRsuxnccHsIsFaY9bLSDQGn1YFsIhYqrDHGUOalWaG7bGgI9WsdZ8sOMcZD_0FYxNlHKPSChbgw; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711356119:t=1711383469:v=2:sig=AQHd82x2wmOrEUinpWMUoqSumnm7thv9"; sdsc=22%3A1%2C1711358702924%7EJAPP%2C0Il%2B%2BEl2u2z0VpUMUw0YV3QiPP5w%3D; li_mc=MTsyMTsxNzExMzU5MjUyOzI7MDIxZpfdUzMSAl/jvqRDLzR0Bmsl0ivbeBqjWAv0E8v9JRA=; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzExMzU5MzQ0OzI7MDIxyqTlqWTdQJPWNxDh/xbiQT4itWjB7o6jo2B4Ot+BQKY=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711358640:t=1711383469:v=2:sig=AQF9ncvYxxF7o-JLHiRTCjEY4zv9Awqe"; sdsc=22%3A1%2C1711358702924%7EJAPP%2C0Il%2B%2BEl2u2z0VpUMUw0YV3QiPP5w%3D',
    'csrf-token': 'ajax:5371233139676576627'
    }

    async with sem:
        for attempt in range(max_retries):
            try:
                async with session.get(api_request_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        job_title = data.get('title', None)

                        companyResolutionResult = data.get('companyDetails', {}) \
                            .get('com.linkedin.voyager.deco.jobs.web.shared.WebJobPostingCompany', {}) \
                            .get('companyResolutionResult', {})
                        company_name = companyResolutionResult.get('name', None)
                        employee_count = companyResolutionResult.get('staffCount', None)
                        company_url = companyResolutionResult.get('url', None)
                        companyID_search = re.search(r'(\d+)$', companyResolutionResult.get('entityUrn', ''))
                        companyID = companyID_search.group(1) if companyID_search else None

                        return (job_title, company_name, employee_count, company_url, companyID)
            except Exception as e:
                print(f"Request failed: {e}")
                await asyncio.sleep(delay)
    return None, None, None, None, None

async def extract_company_segment(job_posting_id, sem, session, max_retries=3, delay=1):
    api_request_url = f"https://www.linkedin.com/voyager/api/graphql?queryId=voyagerJobsDashJobPostingDetailSections.0a2eefbfd33e3ff566b3fbe31312c8ed&variables=(cardSectionTypes:List(COMPANY_CARD),jobPostingUrn:urn%3Ali%3Afsd_jobPosting%3A{job_posting_id},includeSecondaryActionsV2:true)"

    # payload = {}
    headers = {
    'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; AnalyticsSyncHistory=AQIdocYcGpv1SwAAAY50EHPdIJOXJnTMkM1IqKRCN-xjtebWOGQgAfFoubhez_GPLJtHRjCZyED3AWxvqFIYaQ; lms_ads=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lms_analytics=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq92w%252bmvbGBUtNoqdDDGU6K1bm1h82%252bvTwd5d9RxSjyqHKve2TN%252fU1qbwaJVqqH1GEuDg0a0qlsVjDyu6M%252bN5RV%252fIXe2ZN%252flEMI%252fBHHwg3PGu9dktCK7gumT5arLAvFaxC3bmPIHli9%252bB0setOxl6WF4LiYsVd%252bVJpbksyOh%252ffPp89f24dvjSFhWT6wkNTleVQJ4VuwhZF5JiBbSfQxz%252bYWc%253d; sdsc=22%3A1%2C1711462099933%7EJAPP%2C0AgLnCcsJR96aeTsG%2FE69adrVVF4%3D; __cf_bm=XUaVjb_yxnwanRjtokE8Horyb443hwji7VAfjojIzis-1711471681-1.0.1.1-PeTZcP10fT6yKv96rtf5ev8f2Zf77nsmyiuf851hQReBUzs4tIaF.U121htJ7.CGjWCFAz.utMUFimvs1TjfFA; li_mc=MTsyMTsxNzExNDcxNzkyOzI7MDIxIv706UPGtRPQ+6CckOOl29O91ZeGpStrdGS1x1TEp0o=; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19808%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712076989%7C6%7CMCAAMB-1712076989%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711479389s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; UserMatchHistory=AQKQHbt-oTRe4AAAAY57suv6OCAUqZNXKSczMTZ2g5qZz1s58prBJ5YjvaCqCQZBk7UWzEzIEiBH0yiCLOjOD1wkEG1TDRjHRPGQjG8Y_3DMsgyAX7aZeizllMAwDh-nEVgmPtyLnB-hpC2GXKgivEQrzz-7_OfZ7yVOMW0t-wO3vpjJAjtaOcTtL2tsmqrC9OEtuI_jy1RFB91h0_Cu3ioKe8xb6Jhegs0qXP6ynuQY6BDHbWJeQrzvKMUdPbtJ9QADbzHPr3NEk3Z4LE_cpcIsC2HDdCcwWhUDJ78MmstZIdNfTZ0nVHVPUGVP-Hvro_UgG38; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4158:u=247:x=1:i=1711472308:t=1711540940:v=2:sig=AQFtWBAyB43Zq72h20RayXgdxThybm5u"; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzEyMTI5NjUzOzI7MDIxb1FDm4/OAQd3RE96phr4myBQirtxp4cumtS5p/PhkAI=; liap=true; lidc="b=OB74:s=O:r=O:a=O:p=O:g=4532:u=252:x=1:i=1712129653:t=1712131143:v=2:sig=AQEHHUP-6BQJFHT-86M1VAdRS7sfW_fN"; JSESSIONID="ajax:5371233139676576627"; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOw2TMvE0AFsDybLtUTmv0FMxT50kAEGZ9VsWUe-PpCGDBaJfv3cu3EFB2F9WewOHhiJ99vjDLoxliKYuiiM5nt_Ivx92s6DJMCE-owqou0cPCGFDhyL_Rmu5_',
    'csrf-token': 'ajax:5371233139676576627'
    }

    async with sem:
        for attempt in range(max_retries):
            try:
                async with session.get(api_request_url, headers=headers) as response:
                    print("In the async session")
                    print(f"Response status: {response.status}")
                    if response.status == 200:
                        print("Response 200")
                        data = await response.json()
                        if data:
                            print("We have data")
                        company_segment = data.get('data', {}) \
                            .get('jobsDashJobPostingDetailSectionsByCardSectionTypes', {}) \
                            .get('elements', [{}])[0] \
                            .get('jobPostingDetailSection', [{}])[0] \
                            .get('companyCardV2', {}) \
                            .get('company', {}) \
                            .get('industryV2Taxonomy', [{}])[0] \
                            .get('name', None)
                        
                        print(f"Company segment: {company_segment}")

                        return company_segment
            except Exception as e:
                print(f"Request failed: {e}")
                await asyncio.sleep(delay)    
    return None        

async def extract_non_hiring_person(keywords, company_id, company_name, sem, session, max_retries=3, delay=1):
    api_request_url = f"https://www.linkedin.com/voyager/api/graphql?variables=(start:0,origin:FACETED_SEARCH,query:(keywords:{keywords},flagshipSearchIntent:ORGANIZATIONS_PEOPLE_ALUMNI,queryParameters:List((key:currentCompany,value:List({company_id})),(key:resultType,value:List(ORGANIZATION_ALUMNI))),includeFiltersInResponse:true),count:12)&queryId=voyagerSearchDashClusters.95b56a377280ee0fdf38866e2fa1abbb"
    headers = {
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; AnalyticsSyncHistory=AQIdocYcGpv1SwAAAY50EHPdIJOXJnTMkM1IqKRCN-xjtebWOGQgAfFoubhez_GPLJtHRjCZyED3AWxvqFIYaQ; lms_ads=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lms_analytics=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lang=v=2&lang=en-us; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19810%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712132028%7C6%7CMCAAMB-1712132028%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711534428s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq%252fDg1P2Me884P8DqJE%252bu%252bhdOIkdyU2Cd9w7yHB6iYtKb6U8xaAwTvjnq2ssHPK9ys0CAhVje7nR0DTLdIy9PE45kvhPJ3sibyhZTSZKysPbaKCqnS2Sh571VGFuY8f7wMKVMw9Fr9GO9AFcBiIYaQR39wL6dxjxiNCgNyh2USDm5N%252boMdbTeHx8KVUtII%252b%252fAwOj5zdC0JUS4BawY8JnOEP8%253d; li_mc=MTsyMTsxNzExNTM0MjE5OzI7MDIx1u11r1q1nZqdf9VZ9i4emq/otsc8a1aE1Ey3hNklH0w=; UserMatchHistory=AQKXWw-1YRtD4gAAAY5_a8Auf7UfWtLREei053hA5noLL671okszgbKq2Zb2dZBffrFWdvFTgBDY0Lu9DPzgLkRCsvcXBATGNVCUaCU5ECIr9seK7Mga8vwwisdtb5bCJMpPjoCjBEobBEjSJqs3zHYzQfmOknbzSQu5oQTrY7i5TV5Hhec30h6jewTNa74LM0zJXCDTufhARjnsXh_KrXpvQbpffv1Aqg8XuHnNV48lrNxSYaDqhFnLoEiADcTd_z5PAm9zAT6n0yfNnljBhoKuvizFtRi82bigcnx30pBXodVkoqZK1B1qiskaux2xtpZbx-o; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4160:u=247:x=1:i=1711534752:t=1711617371:v=2:sig=AQFNrIKZoqRhrNuX34UJHAh5kfxs_Skg"; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzExNTM2MTgyOzI7MDIxZbVJ/rJpkAJJ7wrIljpYP8RVlT8ZZ7duyC5fy/bxuWw=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4160:u=247:x=1:i=1711534708:t=1711617371:v=2:sig=AQGsSO7VGSkbkYwJDZahwdPhzv2WlGE8"',
    'csrf-token': 'ajax:5371233139676576627'
    }

    async with sem:
        for attempt in range(max_retries):
            try:
                async with session.get(api_request_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        included = data.get('included', [{}])

                        # Filter out any items in 'included' that don't represent a person based on a minimum number of keys
                        filtered_people = [person for person in included if len(person) >= 5]
                        
                        processed = []
                        for person in filtered_people:
                            if not isinstance(person, dict):
                                continue

                            linkedin_url = person.get('navigationUrl')
                            if isinstance(linkedin_url, str):
                                linkedin_url_search = re.search(r'^(.*?)\?', linkedin_url)
                                linkedin_url_result = linkedin_url_search.group(1) if linkedin_url_search else linkedin_url # Use the original URL if no query parameters are found
                            else:
                                linkedin_url_result = None
                            full_name = person.get('title', {}).get('text', None)
                            bio = person.get('primarySubtitle', {}).get('text', None)
                            
                            processed.append((full_name, bio, linkedin_url_result))

                        return processed
            except Exception as e:
                print(f"Request failed: {e}")
                await asyncio.sleep(delay)
    return []

async def hiring_person_or_not(job_posting_id, employee_threshold, less_than_keywords, more_than_keywords, sem, session):
    full_name, bio, linkedin_url = await extract_full_name_bio_and_linkedin_url(job_posting_id, sem, session)
    if full_name and bio and linkedin_url:
        return [(full_name, bio, linkedin_url)]
    else:
        job_title, company_name, employee_count, company_url, companyID = await extract_company_info(job_posting_id, sem, session)

        if employee_count is not None:
            company_keywords = less_than_keywords if employee_count <= employee_threshold else more_than_keywords
            url_formatted_keywords = company_keywords.replace(', ', '%20OR%20').strip()        
            company_people = await extract_non_hiring_person(url_formatted_keywords, companyID, company_name, sem, session)
            return company_people
        else:
            return []


async def main(keyword, batches, employee_threshold, less_than_keywords, more_than_keywords, semaphore_value=5):
    sem = asyncio.Semaphore(semaphore_value)
    async with aiohttp.ClientSession() as session:
        all_job_posting_ids = await extract_all_job_posting_ids(keyword, batches, sem, session)
        print(f"All job posting ids: {all_job_posting_ids}")
        job_postings_to_process = len(all_job_posting_ids)

        tasks = []
        for job_posting in all_job_posting_ids:
            company_info_task = extract_company_info(job_posting, sem, session)
            company_segment_task = extract_company_segment(job_posting, sem, session)
            employee_info_task = hiring_person_or_not(job_posting, employee_threshold, less_than_keywords, more_than_keywords, sem, session)
            tasks += [company_info_task, company_segment_task, employee_info_task]

        all_results = await asyncio.gather(*tasks)

        # Group all results into tuples (will make the DataFrame processing a lot easier)
        grouped_results = []
        for i in range(0, job_postings_to_process * 3, 3):
            grouped_result = (all_results[i], all_results[i+1], all_results[i+2])
            grouped_results.append(grouped_result)
    
    return grouped_results

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

### STREAMLIT CODE
# st.title('LinkedIn Job search URL to CSV Generator V2')
# st.markdown(f'Sample URL: https://www.linkedin.com/jobs/search/?currentJobId=3836861341&keywords=sem%20seo&origin=SWITCH_SEARCH_VERTICAL')

# # User input for LinkedIn URL
# linkedin_job_url = st.text_input('Enter URL from the LinkedIn Job search:', '')
# result_name = st.text_input('Enter a name for the resulting csv/Excel file:', '')
# max_results_to_check = st.text_input('Enter maximum amounts of jobs to check (leave blank to scrape all available jobs for the query):', '')
# st.write("If there is no Hiring Team available and the company has less than or equal to")
# employee_threshold = st.number_input("Employee Threshold", min_value=1, value=100, step=1, format="%d", label_visibility="collapsed")
# less_than_keywords = st.text_input('employees, search the company for (separate keywords with comma):', '')
# more_than_keywords = st.text_input('If it has more, search the company for: (separate keywords with comma)', '')

# # Radio button to choose the file format
# file_format = st.radio("Choose the file format for download:", ('csv', 'xlsx'))

# # Button to the result file
# if st.button('Generate File'):
#     with st.spinner('Generating file, hold on'):
#         if linkedin_job_url:
#             keyword_search = re.search(r'keywords=([^&]+)', linkedin_job_url)
#             keyword = keyword_search.group(1) if keyword_search else None

#             start_time = time.time()
#             total_number_of_results = get_total_number_of_results(keyword)
#             if total_number_of_results is None:
#                 st.error("Could not fetch total amount of ads. Try again in a bit")

#             if len(max_results_to_check) != 0 and int(max_results_to_check) < total_number_of_results:
#                 total_number_of_results = int(max_results_to_check)
#             print(f"Attempting to scrape info from {total_number_of_results} job ads!")

#             batches = split_total_into_batches_of_100(total_number_of_results)
#             print(f"Splitting {total_number_of_results} in batches: {batches}")

#             results = asyncio.run(main(keyword, batches, employee_threshold, less_than_keywords, more_than_keywords))
#             end_time = time.time()
#             print("Done!")
#             print(results)
#             print(len(results))
#             st.text(f"Done! Scraped {total_number_of_results} products in {end_time - start_time} seconds")
#             # st.text(f"Total job posting ids found in the request: {total_number_of_results}\nTotal fetched succesfully: {total_fetched}\nTotal unique ids: {total_unique}\nTotal with hiring team available: {total_hiring_team}")

#             # if file_format == 'csv':
#             #     csv_file = generate_csv(scraped_data_df, result_name)
#             #     with open(csv_file, "rb") as file:
#             #         st.download_button(label="Download CSV", data=file, file_name=csv_file, mime='text/csv')
#             #     st.success(f'CSV file generated: {csv_file}')
#             # elif file_format == 'xlsx':
#             #     excel_file = generate_excel(scraped_data_df, result_name)
#             #     st.download_button(label="Download Excel", data=excel_file, file_name=f"{result_name}.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#             #     st.success(f'Excel file generated: {result_name}.xlsx')
#         else:
#             st.error('Please enter a valid LinkedIn URL.')

linkedin_job_url = "https://www.linkedin.com/jobs/search/?currentJobId=3836861341&keywords=sem%20seo&origin=SWITCH_SEARCH_VERTICAL"

start_time = time.time()
print("Running...")
keyword_search = re.search(r'keywords=([^&]+)', linkedin_job_url)
keyword = keyword_search.group(1) if keyword_search else None
print(f"Keyword: {keyword}")
total_number_of_results = 3
print(f"Total: {total_number_of_results}")
batches = split_total_into_batches_of_100(total_number_of_results)
print(f"Batches: {batches}")
employee_threshold = 100
less_than_keywords = "ceo"
more_than_keywords = "cmo"

grouped_results = asyncio.run(main(keyword, batches, employee_threshold, less_than_keywords, more_than_keywords))
end_time = time.time()
print(f"Done! Scraped info from {total_number_of_results} job ads in {end_time - start_time} seconds")
print(grouped_results)

with open ("times.txt", "a") as f:
    f.write(f"Total: {total_number_of_results}, Time: {end_time - start_time}\n")

# for batch in batches:
#     start, stop = batch
#     print(f"Start: {start}, Stop: {stop}")
#     batch_size = stop - start
#     print(f"Batch size: {batch_size}")

#     api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count={batch_size}&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start={start}"
#     headers = {
#     'csrf-token': 'ajax:5371233139676576627',
#     'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjc2MTc0OzI7MDIxe9WcWZ2d6Bt7L96zCLaBjXpfuxnqB2ora17i0MVkktc=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
#     }

#     response = requests.get(api_request_url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()

#         job_posting_ids_list = []
#         prefetchJobPostingCardUrns = data.get('metadata', {}) \
#             .get('jobCardPrefetchQueries', [{}])[0] \
#             .get('prefetchJobPostingCardUrns', {})
#         for job_posting in prefetchJobPostingCardUrns:
#             job_posting_id_search = re.search(r"(\d+)", job_posting)
#             job_posting_id = job_posting_id_search.group(1) if job_posting_id_search else None
#             job_posting_ids_list.append(job_posting_id)

# for job_posting in job_posting_ids_list:
#     url = f"https://www.linkedin.com/voyager/api/graphql?queryId=voyagerJobsDashJobPostingDetailSections.0a2eefbfd33e3ff566b3fbe31312c8ed&variables=(cardSectionTypes:List(COMPANY_CARD),jobPostingUrn:urn%3Ali%3Afsd_jobPosting%3A{job_posting},includeSecondaryActionsV2:true)"

#     payload = {}
#     headers = {
#     'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; AnalyticsSyncHistory=AQIdocYcGpv1SwAAAY50EHPdIJOXJnTMkM1IqKRCN-xjtebWOGQgAfFoubhez_GPLJtHRjCZyED3AWxvqFIYaQ; lms_ads=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lms_analytics=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq92w%252bmvbGBUtNoqdDDGU6K1bm1h82%252bvTwd5d9RxSjyqHKve2TN%252fU1qbwaJVqqH1GEuDg0a0qlsVjDyu6M%252bN5RV%252fIXe2ZN%252flEMI%252fBHHwg3PGu9dktCK7gumT5arLAvFaxC3bmPIHli9%252bB0setOxl6WF4LiYsVd%252bVJpbksyOh%252ffPp89f24dvjSFhWT6wkNTleVQJ4VuwhZF5JiBbSfQxz%252bYWc%253d; sdsc=22%3A1%2C1711462099933%7EJAPP%2C0AgLnCcsJR96aeTsG%2FE69adrVVF4%3D; __cf_bm=XUaVjb_yxnwanRjtokE8Horyb443hwji7VAfjojIzis-1711471681-1.0.1.1-PeTZcP10fT6yKv96rtf5ev8f2Zf77nsmyiuf851hQReBUzs4tIaF.U121htJ7.CGjWCFAz.utMUFimvs1TjfFA; li_mc=MTsyMTsxNzExNDcxNzkyOzI7MDIxIv706UPGtRPQ+6CckOOl29O91ZeGpStrdGS1x1TEp0o=; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19808%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712076989%7C6%7CMCAAMB-1712076989%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711479389s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; UserMatchHistory=AQKQHbt-oTRe4AAAAY57suv6OCAUqZNXKSczMTZ2g5qZz1s58prBJ5YjvaCqCQZBk7UWzEzIEiBH0yiCLOjOD1wkEG1TDRjHRPGQjG8Y_3DMsgyAX7aZeizllMAwDh-nEVgmPtyLnB-hpC2GXKgivEQrzz-7_OfZ7yVOMW0t-wO3vpjJAjtaOcTtL2tsmqrC9OEtuI_jy1RFB91h0_Cu3ioKe8xb6Jhegs0qXP6ynuQY6BDHbWJeQrzvKMUdPbtJ9QADbzHPr3NEk3Z4LE_cpcIsC2HDdCcwWhUDJ78MmstZIdNfTZ0nVHVPUGVP-Hvro_UgG38; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4158:u=247:x=1:i=1711472308:t=1711540940:v=2:sig=AQFtWBAyB43Zq72h20RayXgdxThybm5u"; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzEyMTI5NjUzOzI7MDIxb1FDm4/OAQd3RE96phr4myBQirtxp4cumtS5p/PhkAI=; liap=true; lidc="b=OB74:s=O:r=O:a=O:p=O:g=4532:u=252:x=1:i=1712129653:t=1712131143:v=2:sig=AQEHHUP-6BQJFHT-86M1VAdRS7sfW_fN"; JSESSIONID="ajax:5371233139676576627"; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOw2TMvE0AFsDybLtUTmv0FMxT50kAEGZ9VsWUe-PpCGDBaJfv3cu3EFB2F9WewOHhiJ99vjDLoxliKYuiiM5nt_Ivx92s6DJMCE-owqou0cPCGFDhyL_Rmu5_',
#     'csrf-token': 'ajax:5371233139676576627'
#     }

#     response = requests.request("GET", url, headers=headers, data=payload)

#     if response.status_code == 200:
#         print("Response 200")
#         data = response.json()
#         if data:
#             print("We have data")
#         company_segment = data.get('data', {}) \
#             .get('jobsDashJobPostingDetailSectionsByCardSectionTypes', {}) \
#             .get('elements', [{}])[0] \
#             .get('jobPostingDetailSection', [{}])[0] \
#             .get('companyCardV2', {}) \
#             .get('company', {}) \
#             .get('industryV2Taxonomy', [{}])[0] \
#             .get('name', None)
        
#     print(f"Company segment: {company_segment}")

# url = "https://www.linkedin.com/voyager/api/jobs/jobPostings/3872996790?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65"
# headers = {
#   'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; AnalyticsSyncHistory=AQIdocYcGpv1SwAAAY50EHPdIJOXJnTMkM1IqKRCN-xjtebWOGQgAfFoubhez_GPLJtHRjCZyED3AWxvqFIYaQ; lms_ads=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lms_analytics=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19808%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1711957673%7C6%7CMCAAMB-1711957673%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711360073s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq1E28xfVI%252fAcBePtgF5Ot6DvS%252fWB%252fLpFSKQIKiRvmofK47glv4UaszkM5BnaNumC19YjDA%252bGl3u278Mr4GVIBmsfuuHdZTKno6a2sJ4rLM%252bAj0eDcO%252boYUweonHKKXHh788Zkj2SGfNAE9x8tKHwo3oYtG%252fxfgSwib%252fnm2aRhCAFhh9Fc2E7uz1O5fgWEMg2cRnKiCKqv7XwXHsq%252f%252bEEn%252bw%253d; UserMatchHistory=AQKmb6P7HRl1UwAAAY50xgSC9LUMrQMVkRLljSnCrJ90HVCsa441cRTLL9qKlX6i1O796TJSEgL8GfunfiMFakp5E4NQGpZ4V40DJ_8zY1PSKP7Uw6QRian1QRspnn4lsOnJtQfSweE_GkLslrEZAoG4kyeZoZa6iUcGEXUMykKcxaIj84oR5PSXNVgwPgbtr3ZuND98f_e4iATtvE9E8zrkGmhiHh2D1rs631QMeNCVV1AynA_ecMI9_lXkqRsuxnccHsIsFaY9bLSDQGn1YFsIhYqrDHGUOalWaG7bGgI9WsdZ8sOMcZD_0FYxNlHKPSChbgw; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711356119:t=1711383469:v=2:sig=AQHd82x2wmOrEUinpWMUoqSumnm7thv9"; sdsc=22%3A1%2C1711358702924%7EJAPP%2C0Il%2B%2BEl2u2z0VpUMUw0YV3QiPP5w%3D; li_mc=MTsyMTsxNzExMzU5MjUyOzI7MDIxZpfdUzMSAl/jvqRDLzR0Bmsl0ivbeBqjWAv0E8v9JRA=; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzEyMDcwMzYyOzI7MDIxdkKPQcXXwInAKiDeseXFhF0mBvFumW4hjo4rjALm1tE=; liap=true; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4174:u=251:x=1:i=1712070346:t=1712115531:v=2:sig=AQH3GK8h11VL-_K9XAcszYbeJyOzNAGk"; JSESSIONID="ajax:5371233139676576627"; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOw2TMvE0AFsDybLtUTmv0FMxT50kAEGZ9VsWUe-PpCGDBaJfv3cu3EFB2F9WewOHhiJ99vjDLoxliKYuiiM5nt_Ivx92s6DJMCE-owqou0cPCGFDhyL_Rmu5_',
#   'csrf-token': 'ajax:5371233139676576627'
# }

# response = requests.request("GET", url, headers=headers)
# data = response.json()
# job_title = data.get('title', None)

# companyResolutionResult = data.get('companyDetails', {}) \
#     .get('com.linkedin.voyager.deco.jobs.web.shared.WebJobPostingCompany', {}) \
#     .get('companyResolutionResult', {})
# company_name = companyResolutionResult.get('name', None)
# employee_count = companyResolutionResult.get('staffCount', None)
# print(f"Epmloyee count: {employee_count}")


# for batch in batches:
#     start, stop = batch
#     batch_size = stop - start
#     api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count={batch_size}&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start={start}"
#     headers = {
#     'csrf-token': 'ajax:5371233139676576627',
#     'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjc2MTc0OzI7MDIxe9WcWZ2d6Bt7L96zCLaBjXpfuxnqB2ora17i0MVkktc=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
#     }
#     response = requests.get(api_request_url, headers=headers)
#     if response.status_code == 200:
#         print("Response 200")
#         data = response.json()
#         if data:
#             print("We have data")

#         job_posting_ids_list = []
#         prefetchJobPostingCardUrns = data.get('metadata', {}) \
#             .get('jobCardPrefetchQueries', [{}])[0] \
#             .get('prefetchJobPostingCardUrns', {})
#         if prefetchJobPostingCardUrns:
#             print("We have prefetch")
#         for job_posting in prefetchJobPostingCardUrns:
#             print(f"Job posting: {job_posting}")
#             job_posting_id_search = re.search(r"(\d+)", job_posting)
#             job_posting_id = job_posting_id_search.group(1) if job_posting_id_search else None
#             print(f"Job posting ID: {job_posting_id}")
#             # job_posting_ids_list.append(job_posting_id)
#             time.sleep(200)

# INVISE: 3803170223
result_dataframe = pd.DataFrame(columns=['Hiring Team', 'Förnamn', 'Efternamn', 'Bio', 'LinkedIn URL', 'Jobbtitel som sökes', 'Jobbannons-url', 'Företag', 'Antal anställda', 'Företagssegment', 'Företags-url'])

counter = 0
hiring_team_counter = 0
temp_data_list = []