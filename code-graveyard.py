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
#     lurl, name = extract_full_name_bio_and_linkedin_url(id)
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
#                     linkedin_url, full_name = extract_full_name_bio_and_linkedin_url(job_posting)
        
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


        
# linkedin_job_url = "https://www.linkedin.com/jobs/search/?currentJobId=3836861341&keywords=sem%20seo&origin=SWITCH_SEARCH_VERTICAL"
# keyword = re.search(r'keywords=([^&]+)', linkedin_job_url).group(1)

# total_results = 367
# batches = split_total_into_batches_of_100(total_results)
# print(batches)



# urls = []
# for i, (start, stop) in enumerate(batches):
#     batch_size = stop - start
#     api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count={batch_size}&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start={start}"
#     urls.append(api_request_url)

# print(urls)

# async def fetch(sem, session, url, headers, payload, max_retries=3, delay=1):
#     async with sem:
#         for attempt in range(max_retries):
#             try:
#                 async with session.get(url, headers=headers, json=payload) as response:
#                     if response.status == 200:
#                         data = await response.json()
#                         return data
#                     elif response.status == 500:
#                         print(f"Attempt {attempt + 1}: Server Error for URL {url}. Retrying in 1 second...")
#                         await asyncio.sleep(1)
#                     else:
#                         print(f"Attempt {attempt + 1}: Other Error for URL {url}. Retrying in 1 second...")
#                         await asyncio.sleep(1)
#             except aiohttp.ClientError as e:
#                 print(f"Request failed: {e}")
#                 await asyncio.sleep(1)
#         print(f"Failed to fetch {url} after 3 attempts.")
#         return None  # Or handle failed fetches as needed

# async def fetch_all(urls):
#     sem = asyncio.Semaphore(5)  # Adjust the number as needed. Tried len(batches)
#     async with aiohttp.ClientSession() as session:
#         payload = {}
#         headers = {
#         'csrf-token': 'ajax:5371233139676576627',
#         'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjc2MTc0OzI7MDIxe9WcWZ2d6Bt7L96zCLaBjXpfuxnqB2ora17i0MVkktc=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
#         }
#         tasks = [asyncio.create_task(fetch(sem, session, url, headers, payload)) for url in urls]
#         return await asyncio.gather(*tasks)

# results = asyncio.run(fetch_all(urls))
# print(len(results))

# job_posting_ids = []
# for result in results:
#     job_posting_id = get_job_posting_ids(result)
#     job_posting_ids.extend(job_posting_id)

# print(job_posting_ids)

# for batch in job_posting_batches:
#     for job_posting in batch:
#         print(f"Processing job posting #{job_posting}")
#         full_name, bio, linkedin_url = extract_full_name_bio_and_linkedin_url(job_posting)
#         job_title, company_name, employee_count, company_url, companyID = extract_company_info(job_posting)
#         first_name, last_name = split_and_clean_full_name(full_name)

#         print(first_name, last_name, bio, linkedin_url, company_name, employee_count, company_url)

# def get_job_posting_ids(response_json):
#     metadata = response_json.get('metadata', {})
#     jobCardPrefetchQueries = metadata.get('jobCardPrefetchQueries', [])
#     job_posting_ids_list = []

#     if jobCardPrefetchQueries:
#         prefetchJobPostingCardUrns = jobCardPrefetchQueries[0].get('prefetchJobPostingCardUrns', {})
#         for job_posting in prefetchJobPostingCardUrns:
#             job_posting_id = re.search(r"\d+", job_posting).group()
#             job_posting_ids_list.append(job_posting_id)

#     return job_posting_ids_list

# def extract_full_name_bio_and_linkedin_url(job_posting_id, max_retries=3, delay=1):
#     api_request_url = f"https://www.linkedin.com/voyager/api/voyagerHiringDashJobHiringSocialHirersCards?jobPosting=urn%3Ali%3Afsd_jobPosting%3A{job_posting_id}&q=jobPosting"
#     payload = {}
#     headers = {
#     'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; AnalyticsSyncHistory=AQIdocYcGpv1SwAAAY50EHPdIJOXJnTMkM1IqKRCN-xjtebWOGQgAfFoubhez_GPLJtHRjCZyED3AWxvqFIYaQ; lms_ads=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lms_analytics=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19808%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1711957673%7C6%7CMCAAMB-1711957673%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711360073s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq1E28xfVI%252fAcBePtgF5Ot6DvS%252fWB%252fLpFSKQIKiRvmofK47glv4UaszkM5BnaNumC19YjDA%252bGl3u278Mr4GVIBmsfuuHdZTKno6a2sJ4rLM%252bAj0eDcO%252boYUweonHKKXHh788Zkj2SGfNAE9x8tKHwo3oYtG%252fxfgSwib%252fnm2aRhCAFhh9Fc2E7uz1O5fgWEMg2cRnKiCKqv7XwXHsq%252f%252bEEn%252bw%253d; sdsc=22%3A1%2C1711355253815%7EJAPP%2C0OEHjuDn%2F8jB%2FwUYa7uP3OdX7FUs%3D; UserMatchHistory=AQKmb6P7HRl1UwAAAY50xgSC9LUMrQMVkRLljSnCrJ90HVCsa441cRTLL9qKlX6i1O796TJSEgL8GfunfiMFakp5E4NQGpZ4V40DJ_8zY1PSKP7Uw6QRian1QRspnn4lsOnJtQfSweE_GkLslrEZAoG4kyeZoZa6iUcGEXUMykKcxaIj84oR5PSXNVgwPgbtr3ZuND98f_e4iATtvE9E8zrkGmhiHh2D1rs631QMeNCVV1AynA_ecMI9_lXkqRsuxnccHsIsFaY9bLSDQGn1YFsIhYqrDHGUOalWaG7bGgI9WsdZ8sOMcZD_0FYxNlHKPSChbgw; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711356119:t=1711383469:v=2:sig=AQHd82x2wmOrEUinpWMUoqSumnm7thv9"; li_mc=MTsyMTsxNzExMzU3MzM2OzI7MDIxAdG1QK8bbcuKeDmJq0ey4DLjFZszCE7JjhRCegIKT/A=; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzExMzU3NDAyOzI7MDIxcChChZMT4OrNPcgxswKzL8h0/enN9c+0qgJAAAy2LmM=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711357847:t=1711383469:v=2:sig=AQEEx0S-hSoqzv3TS2j_b_c1EUsiWH4T"; sdsc=22%3A1%2C1711355253815%7EJAPP%2C0OEHjuDn%2F8jB%2FwUYa7uP3OdX7FUs%3D',
#     'csrf-token': 'ajax:5371233139676576627'
#     }

#     attempts = 0
#     while attempts < max_retries:
#         response = requests.get(api_request_url, headers=headers, data=payload)
#         if response.status_code == 200:
#             full_name = None
#             bio = None
#             linkedin_url = None

#             elements = response.json().get('elements', [])
#             if elements:
#                 title = elements[0].get('title', {})
#                 if title:
#                     full_name = title.get('text')
#                 subtitle = elements[0].get('subtitle')
#                 if subtitle:
#                     bio = subtitle.get('text')
#                 linkedin_url = elements[0].get('navigationUrl')
                
#             return (full_name, bio, linkedin_url)
#         else:
#             attempts += 1
#             time.sleep(delay)  # Wait before the next attempt

#     return None, None, None  # Return None if all attempts fail

# def extract_company_info(job_posting_id, max_retries=3, delay=1):
#     api_request_url = f"https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_posting_id}?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65"
#     payload = {}
#     headers = {
#     'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; AnalyticsSyncHistory=AQIdocYcGpv1SwAAAY50EHPdIJOXJnTMkM1IqKRCN-xjtebWOGQgAfFoubhez_GPLJtHRjCZyED3AWxvqFIYaQ; lms_ads=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lms_analytics=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19808%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1711957673%7C6%7CMCAAMB-1711957673%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711360073s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq1E28xfVI%252fAcBePtgF5Ot6DvS%252fWB%252fLpFSKQIKiRvmofK47glv4UaszkM5BnaNumC19YjDA%252bGl3u278Mr4GVIBmsfuuHdZTKno6a2sJ4rLM%252bAj0eDcO%252boYUweonHKKXHh788Zkj2SGfNAE9x8tKHwo3oYtG%252fxfgSwib%252fnm2aRhCAFhh9Fc2E7uz1O5fgWEMg2cRnKiCKqv7XwXHsq%252f%252bEEn%252bw%253d; UserMatchHistory=AQKmb6P7HRl1UwAAAY50xgSC9LUMrQMVkRLljSnCrJ90HVCsa441cRTLL9qKlX6i1O796TJSEgL8GfunfiMFakp5E4NQGpZ4V40DJ_8zY1PSKP7Uw6QRian1QRspnn4lsOnJtQfSweE_GkLslrEZAoG4kyeZoZa6iUcGEXUMykKcxaIj84oR5PSXNVgwPgbtr3ZuND98f_e4iATtvE9E8zrkGmhiHh2D1rs631QMeNCVV1AynA_ecMI9_lXkqRsuxnccHsIsFaY9bLSDQGn1YFsIhYqrDHGUOalWaG7bGgI9WsdZ8sOMcZD_0FYxNlHKPSChbgw; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711356119:t=1711383469:v=2:sig=AQHd82x2wmOrEUinpWMUoqSumnm7thv9"; sdsc=22%3A1%2C1711358702924%7EJAPP%2C0Il%2B%2BEl2u2z0VpUMUw0YV3QiPP5w%3D; li_mc=MTsyMTsxNzExMzU5MjUyOzI7MDIxZpfdUzMSAl/jvqRDLzR0Bmsl0ivbeBqjWAv0E8v9JRA=; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzExMzU5MzQ0OzI7MDIxyqTlqWTdQJPWNxDh/xbiQT4itWjB7o6jo2B4Ot+BQKY=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711358640:t=1711383469:v=2:sig=AQF9ncvYxxF7o-JLHiRTCjEY4zv9Awqe"; sdsc=22%3A1%2C1711358702924%7EJAPP%2C0Il%2B%2BEl2u2z0VpUMUw0YV3QiPP5w%3D',
#     'csrf-token': 'ajax:5371233139676576627'
#     }

#     attempts = 0
#     while attempts < max_retries:
#         response = requests.request("GET", api_request_url, headers=headers, data=payload)
#         if response.status_code == 200:
#             job_title = None
#             company_name = None
#             employee_count = None
#             company_url = None
#             companyID = None

#             job_title = response.json().get('title')

#             companyDetails = response.json().get('companyDetails', {})
#             if companyDetails:
#                 WebJobPostingCompany = companyDetails.get('com.linkedin.voyager.deco.jobs.web.shared.WebJobPostingCompany', {})
#                 if WebJobPostingCompany:
#                     companyResolutionResult = WebJobPostingCompany.get('companyResolutionResult', {})
#                     if companyResolutionResult:
#                         company_name = companyResolutionResult.get('name')
#                         employee_count = companyResolutionResult.get('staffCount')
#                         company_url = companyResolutionResult.get('url')
#                         companyID = re.search(r'(\d+)$', companyResolutionResult.get('entityUrn')).group(1)

#             return (job_title, company_name, employee_count, company_url, companyID)
#         else:
#             attempts += 1
#             time.sleep(delay)
    
#     return None, None, None, None, None

# def extract_company_info(job_posting_id, max_retries=3, delay=1):
#     api_request_url = f"https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_posting_id}?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65"
#     payload = {}
#     headers = {
#     'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; AnalyticsSyncHistory=AQIdocYcGpv1SwAAAY50EHPdIJOXJnTMkM1IqKRCN-xjtebWOGQgAfFoubhez_GPLJtHRjCZyED3AWxvqFIYaQ; lms_ads=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lms_analytics=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19808%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1711957673%7C6%7CMCAAMB-1711957673%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711360073s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq1E28xfVI%252fAcBePtgF5Ot6DvS%252fWB%252fLpFSKQIKiRvmofK47glv4UaszkM5BnaNumC19YjDA%252bGl3u278Mr4GVIBmsfuuHdZTKno6a2sJ4rLM%252bAj0eDcO%252boYUweonHKKXHh788Zkj2SGfNAE9x8tKHwo3oYtG%252fxfgSwib%252fnm2aRhCAFhh9Fc2E7uz1O5fgWEMg2cRnKiCKqv7XwXHsq%252f%252bEEn%252bw%253d; UserMatchHistory=AQKmb6P7HRl1UwAAAY50xgSC9LUMrQMVkRLljSnCrJ90HVCsa441cRTLL9qKlX6i1O796TJSEgL8GfunfiMFakp5E4NQGpZ4V40DJ_8zY1PSKP7Uw6QRian1QRspnn4lsOnJtQfSweE_GkLslrEZAoG4kyeZoZa6iUcGEXUMykKcxaIj84oR5PSXNVgwPgbtr3ZuND98f_e4iATtvE9E8zrkGmhiHh2D1rs631QMeNCVV1AynA_ecMI9_lXkqRsuxnccHsIsFaY9bLSDQGn1YFsIhYqrDHGUOalWaG7bGgI9WsdZ8sOMcZD_0FYxNlHKPSChbgw; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711356119:t=1711383469:v=2:sig=AQHd82x2wmOrEUinpWMUoqSumnm7thv9"; sdsc=22%3A1%2C1711358702924%7EJAPP%2C0Il%2B%2BEl2u2z0VpUMUw0YV3QiPP5w%3D; li_mc=MTsyMTsxNzExMzU5MjUyOzI7MDIxZpfdUzMSAl/jvqRDLzR0Bmsl0ivbeBqjWAv0E8v9JRA=; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzExMzU5MzQ0OzI7MDIxyqTlqWTdQJPWNxDh/xbiQT4itWjB7o6jo2B4Ot+BQKY=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711358640:t=1711383469:v=2:sig=AQF9ncvYxxF7o-JLHiRTCjEY4zv9Awqe"; sdsc=22%3A1%2C1711358702924%7EJAPP%2C0Il%2B%2BEl2u2z0VpUMUw0YV3QiPP5w%3D',
#     'csrf-token': 'ajax:5371233139676576627'
#     }

#     attempts = 0
#     while attempts < max_retries:
#         response = requests.request("GET", api_request_url, headers=headers, data=payload)
#         if response.status_code == 200:
#             job_title = None
#             company_name = None
#             employee_count = None
#             company_url = None
#             companyID = None

#             job_title = response.json().get('title')

#             companyDetails = response.json().get('companyDetails', {})
#             if companyDetails:
#                 WebJobPostingCompany = companyDetails.get('com.linkedin.voyager.deco.jobs.web.shared.WebJobPostingCompany', {})
#                 if WebJobPostingCompany:
#                     companyResolutionResult = WebJobPostingCompany.get('companyResolutionResult', {})
#                     if companyResolutionResult:
#                         company_name = companyResolutionResult.get('name')
#                         employee_count = companyResolutionResult.get('staffCount')
#                         company_url = companyResolutionResult.get('url')
#                         companyID = re.search(r'(\d+)$', companyResolutionResult.get('entityUrn')).group(1)

#             return (job_title, company_name, employee_count, company_url, companyID)
#         else:
#             attempts += 1
#             time.sleep(delay)
    
#     return None, None, None, None, None

# def extract_non_hiring_person(keywords, company_id, company_name, max_retries=3, delay=1):
#     api_request_url = f"https://www.linkedin.com/voyager/api/graphql?variables=(start:0,origin:FACETED_SEARCH,query:(keywords:{keywords},flagshipSearchIntent:ORGANIZATIONS_PEOPLE_ALUMNI,queryParameters:List((key:currentCompany,value:List({company_id})),(key:resultType,value:List(ORGANIZATION_ALUMNI))),includeFiltersInResponse:true),count:12)&queryId=voyagerSearchDashClusters.95b56a377280ee0fdf38866e2fa1abbb"

#     payload = {}
#     headers = {
#     'accept': 'application/vnd.linkedin.normalized+json+2.1',
#     'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; AnalyticsSyncHistory=AQIdocYcGpv1SwAAAY50EHPdIJOXJnTMkM1IqKRCN-xjtebWOGQgAfFoubhez_GPLJtHRjCZyED3AWxvqFIYaQ; lms_ads=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lms_analytics=AQHHU3ZA76qOPgAAAY50EHTSYy32Va0AfZIZ_naHk1TnVWUYdKtxhz6LuM_j61Vi7XfSximgnyGzdYOGfYoTI8VLA4vjH1ID; lang=v=2&lang=en-us; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19810%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712132028%7C6%7CMCAAMB-1712132028%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711534428s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq%252fDg1P2Me884P8DqJE%252bu%252bhdOIkdyU2Cd9w7yHB6iYtKb6U8xaAwTvjnq2ssHPK9ys0CAhVje7nR0DTLdIy9PE45kvhPJ3sibyhZTSZKysPbaKCqnS2Sh571VGFuY8f7wMKVMw9Fr9GO9AFcBiIYaQR39wL6dxjxiNCgNyh2USDm5N%252boMdbTeHx8KVUtII%252b%252fAwOj5zdC0JUS4BawY8JnOEP8%253d; li_mc=MTsyMTsxNzExNTM0MjE5OzI7MDIx1u11r1q1nZqdf9VZ9i4emq/otsc8a1aE1Ey3hNklH0w=; UserMatchHistory=AQKXWw-1YRtD4gAAAY5_a8Auf7UfWtLREei053hA5noLL671okszgbKq2Zb2dZBffrFWdvFTgBDY0Lu9DPzgLkRCsvcXBATGNVCUaCU5ECIr9seK7Mga8vwwisdtb5bCJMpPjoCjBEobBEjSJqs3zHYzQfmOknbzSQu5oQTrY7i5TV5Hhec30h6jewTNa74LM0zJXCDTufhARjnsXh_KrXpvQbpffv1Aqg8XuHnNV48lrNxSYaDqhFnLoEiADcTd_z5PAm9zAT6n0yfNnljBhoKuvizFtRi82bigcnx30pBXodVkoqZK1B1qiskaux2xtpZbx-o; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4160:u=247:x=1:i=1711534752:t=1711617371:v=2:sig=AQFNrIKZoqRhrNuX34UJHAh5kfxs_Skg"; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzExNTM2MTgyOzI7MDIxZbVJ/rJpkAJJ7wrIljpYP8RVlT8ZZ7duyC5fy/bxuWw=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4160:u=247:x=1:i=1711534708:t=1711617371:v=2:sig=AQGsSO7VGSkbkYwJDZahwdPhzv2WlGE8"',
#     'csrf-token': 'ajax:5371233139676576627'
#     }

#     for attempt in range(max_retries):
#         try:
#             response = requests.request("GET", api_request_url, headers=headers, data=payload)
#             if response.status_code == 200:
#                 included = response.json().get('included', [])
#             else:
#                 print(f"Received status code {response.status_code}")
#         except requests.exceptions.RequestException as e:
#             print(f"Request failed: {e}")

#         time.sleep(delay)

#     processed = []

#     for person in included:
#         if len(person) < 5:
#             continue
#         full_name = None
#         bio = None
#         linkedin_url = None
#         title = person.get('title', {})
#         if title:
#             full_name = title.get('text')
#         primarySubtitle = person.get('primarySubtitle', {})
#         if primarySubtitle:
#             bio = primarySubtitle.get('text')
#         try:
#             linkedin_url = person.get('navigationUrl', {})
#             linkedin_url_trimmed = re.search(r'^(.*?)\?', linkedin_url).group(1)
#         except:
#             print("Failed to fetch LinkedIn url")
#             pass
#         processed.append((full_name, bio, linkedin_url_trimmed))

#     return processed

# def scrape_linkedin_and_show_progress(keyword, total_results, employee_threshold, less_than_keywords, more_than_keywords, progress_bar, text_placeholder):
#     result_dataframe = pd.DataFrame(columns=['Hiring Team', 'Förnamn', 'Efternamn', 'Bio', 'LinkedIn URL', 'Jobbtitel som sökes', 'Jobbannons-url', 'Företag', 'Antal anställda', 'Företagssegment', 'Företags-url'])
#     print(f"Keyword: {keyword}")
#     batches = split_total_into_batches_of_100(total_results)
#     print(batches)

#     print(f"Starting the scrape! {total_results} to scrape")
#     start_time = time.time()
#     counter = 0
#     hiring_team_counter = 0
#     temp_data_list = []
#     all_ids = []

#     for i, (start, stop) in enumerate(batches):
#         batch_size = stop - start
#         api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count={batch_size}&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start={start}"

#         payload = {}
#         headers = {
#         'csrf-token': 'ajax:5371233139676576627',
#         'Cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_mc=MTsyMTsxNzExMjc2MTc0OzI7MDIxe9WcWZ2d6Bt7L96zCLaBjXpfuxnqB2ora17i0MVkktc=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; sdsc=22%3A1%2C1711273501254%7EJAPP%2C08tO5%2Fcka%2F8fklcFLQeSLJeOemic%3D; JSESSIONID="ajax:5371233139676576627"; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm'
#         }
        
#         response = requests.request("GET", api_request_url, headers=headers, data=payload)
        
#         if response.status_code == 200:
#             # Fetch the job posting IDs from the response
#             job_posting_list = get_job_posting_ids(response.json())
#             all_ids.extend(job_posting_list)

#             # Process the batch
#             for job_posting in job_posting_list:
#                 print(f"Processing job posting #{job_posting}")
#                 full_name, bio, linkedin_url = extract_full_name_bio_and_linkedin_url(job_posting)
#                 job_title, company_name, employee_count, company_url, companyID = extract_company_info(job_posting)
#                 company_segment = None
#                 if company_name is not None:
#                     company_segment = extract_company_segment(job_posting)
#                 else:
#                     company_segment = None
            
#                 if linkedin_url and full_name:
#                     first_name, last_name = split_and_clean_full_name(full_name)

#                     print(f"#{counter} : LinkedIn URL: {linkedin_url}, Name: {full_name}, Job title: {job_title}, Company: {company_name}")

#                     new_row = {'Hiring Team': 'Ja', 'Förnamn': first_name, 'Efternamn': last_name, 'Bio': bio, 'LinkedIn URL': linkedin_url,
#                             'Jobbtitel som sökes': job_title, 'Jobbannons-url': f"https://www.linkedin.com/jobs/search/?currentJobId={job_posting}&geoId=105117694&keywords=sem%20seo&location=Sweden", 
#                             'Företag': company_name, 'Antal anställda': employee_count, 'Företagssegment': company_segment, 'Företags-url': company_url}

#                     # Check if the new_row is a duplicate
#                     if new_row not in temp_data_list:
#                         temp_data_list.append(new_row)
#                         hiring_team_counter += 1
#                     else:
#                         print("Duplicate found. Skipping.")  
#                 else:
#                     print(f"#{counter} : Could not fetch name and/or url from Hiring team card. Trying other way...")

#                     # Look through the company page
#                     company_keywords = None
#                     try:
#                         if employee_count <= employee_threshold:
#                             company_keywords = less_than_keywords
#                         else:
#                             company_keywords = more_than_keywords

#                         print(f"Keywords: {company_keywords}")
#                         print(f"Company name: {company_name}")
#                         print(f"Company ID: {companyID}")

#                         url_formatted_keywords = company_keywords.replace(', ', '%20OR%20').strip()
#                         print(url_formatted_keywords)

#                         company_people = extract_non_hiring_person(url_formatted_keywords, companyID, company_name)

#                         print(f"Company people: {company_people}")

#                         for person in company_people:
#                             full_name, bio, linkedin_url = person
#                             first_name, last_name = split_and_clean_full_name(full_name)

#                             print(f"Trying to add: {first_name}, {last_name}, {linkedin_url}")

#                             new_row = {'Hiring Team': 'Nej', 'Förnamn': first_name, 'Efternamn': last_name, 'Bio': bio, 'LinkedIn URL': linkedin_url,
#                                     'Jobbtitel som sökes': job_title, 'Jobbannons-url': f"https://www.linkedin.com/jobs/search/?currentJobId={job_posting}&geoId=105117694&keywords=sem%20seo&location=Sweden", 
#                                     'Företag': company_name, 'Antal anställda': employee_count, 'Företagssegment': company_segment, 'Företags-url': company_url}

#                             # Check if the new_row is a duplicate
#                             if new_row not in temp_data_list:
#                                 temp_data_list.append(new_row)
#                             else:
#                                 print("Duplicate found. Skipping.")  
#                     except requests.exceptions.RequestException as e:
#                         print(f"Error: {e}")
#                         # new_row = {'Hiring Team': 'Nej', 'Förnamn': None, 'Efternamn': None, 'Bio': None, 'LinkedIn URL': None,
#                         #             'Jobbtitel som sökes': job_title, 'Jobbannons-url': f"https://www.linkedin.com/jobs/search/?currentJobId={job_posting}&geoId=105117694&keywords=sem%20seo&location=Sweden", 
#                         #             'Företag': company_name, 'Antal anställda': None, 'Företagssegment': company_segment, 'Företags-url': company_url}

#                         # # Check if the new_row is a duplicate
#                         # if new_row not in temp_data_list:
#                         #     temp_data_list.append(new_row)
#                         # else:
#                         #     print("Duplicate found. Skipping.") 

#                 counter += 1
                    
#                 # Update the progress bar and text after each job posting is processed
#                 progress = counter / total_results
#                 progress = min(max(progress, 0.0), 1.0)  # Clamp the progress value
#                 progress_bar.progress(progress)
#                 text_placeholder.text(f"Processing {counter} / {total_results}")

#             # Print the counts after each request
#             print(f"After request batch #{i+1}: Total IDs fetched - {len(all_ids)}. Unique IDs - {len(set(all_ids))}")
#             time.sleep(1) # Wait 1 second until next batch
#         else:
#             print(f"Request for batch {start}-{stop} failed with status code: {response.status_code}")
#             # Handle the failure accordingly, e.g., retry or log error

#     end_time = time.time()
#     print(f"Everything processed! Took {end_time - start_time} seconds\n")

#     # Final update outside the loop to ensure progress is marked complete
#     text_placeholder.text(f"Processing completed! Total processed: {counter} / {total_results}")
#     progress_bar.progress(1.0)  # Ensure the progress bar is full at completion

#     # Convert the list of dictionaries to a DataFrame and concatenate it with the existing result_dataframe
#     new_data_df = pd.DataFrame(temp_data_list)
#     result_dataframe = pd.concat([result_dataframe, new_data_df], ignore_index=True)

#     print(f"Done. Results:\nTotal found in the request: {total_results}\nTotal fetched succesfully: {len(all_ids)}\nTotal unique ids: {len(set(all_ids))}\nTotal hiring team available: {hiring_team_counter}")

#     # Return the resulting dataframe as well as a set with everything we print out after the scrape. Bad practice, I know :))
#     return [result_dataframe, (len(all_ids), len(set(all_ids)), hiring_team_counter)]



    #         full_name, bio, linkedin_url = extract_full_name_bio_and_linkedin_url(job_posting)
    #         job_title, company_name, employee_count, company_url, companyID = extract_company_info(job_posting)
    #         company_segment = None
    #         if company_name is not None:
    #             company_segment = extract_company_segment(job_posting)
    #         else:
    #             company_segment = None
        
    #         if linkedin_url and full_name:
    #             first_name, last_name = split_and_clean_full_name(full_name)

    #             print(f"#{counter} : LinkedIn URL: {linkedin_url}, Name: {full_name}, Job title: {job_title}, Company: {company_name}")

    #             new_row = {'Hiring Team': 'Ja', 'Förnamn': first_name, 'Efternamn': last_name, 'Bio': bio, 'LinkedIn URL': linkedin_url,
    #                     'Jobbtitel som sökes': job_title, 'Jobbannons-url': f"https://www.linkedin.com/jobs/search/?currentJobId={job_posting}&geoId=105117694&keywords=sem%20seo&location=Sweden", 
    #                     'Företag': company_name, 'Antal anställda': employee_count, 'Företagssegment': company_segment, 'Företags-url': company_url}

    #             # Check if the new_row is a duplicate
    #             if new_row not in temp_data_list:
    #                 temp_data_list.append(new_row)
    #                 hiring_team_counter += 1
    #             else:
    #                 print("Duplicate found. Skipping.")  
    #         else:
    #             print(f"#{counter} : Could not fetch name and/or url from Hiring team card. Trying other way...")

    #             # Look through the company page
    #             company_keywords = None
    #             try:
    #                 if employee_count <= employee_threshold:
    #                     company_keywords = less_than_keywords
    #                 else:
    #                     company_keywords = more_than_keywords

    #                 print(f"Keywords: {company_keywords}")
    #                 print(f"Company name: {company_name}")
    #                 print(f"Company ID: {companyID}")

    #                 url_formatted_keywords = company_keywords.replace(', ', '%20OR%20').strip()
    #                 print(url_formatted_keywords)

    #                 company_people = extract_non_hiring_person(url_formatted_keywords, companyID, company_name)

    #                 print(f"Company people: {company_people}")

    #                 for person in company_people:
    #                     full_name, bio, linkedin_url = person
    #                     first_name, last_name = split_and_clean_full_name(full_name)

    #                     print(f"Trying to add: {first_name}, {last_name}, {linkedin_url}")

    #                     new_row = {'Hiring Team': 'Nej', 'Förnamn': first_name, 'Efternamn': last_name, 'Bio': bio, 'LinkedIn URL': linkedin_url,
    #                             'Jobbtitel som sökes': job_title, 'Jobbannons-url': f"https://www.linkedin.com/jobs/search/?currentJobId={job_posting}&geoId=105117694&keywords=sem%20seo&location=Sweden", 
    #                             'Företag': company_name, 'Antal anställda': employee_count, 'Företagssegment': company_segment, 'Företags-url': company_url}

    #                     # Check if the new_row is a duplicate
    #                     if new_row not in temp_data_list:
    #                         temp_data_list.append(new_row)
    #                     else:
    #                         print("Duplicate found. Skipping.")  
    #             except requests.exceptions.RequestException as e:
    #                 print(f"Error: {e}")
    #                 # new_row = {'Hiring Team': 'Nej', 'Förnamn': None, 'Efternamn': None, 'Bio': None, 'LinkedIn URL': None,
    #                 #             'Jobbtitel som sökes': job_title, 'Jobbannons-url': f"https://www.linkedin.com/jobs/search/?currentJobId={job_posting}&geoId=105117694&keywords=sem%20seo&location=Sweden", 
    #                 #             'Företag': company_name, 'Antal anställda': None, 'Företagssegment': company_segment, 'Företags-url': company_url}

    #                 # # Check if the new_row is a duplicate
    #                 # if new_row not in temp_data_list:
    #                 #     temp_data_list.append(new_row)
    #                 # else:
    #                 #     print("Duplicate found. Skipping.") 
    #         else:
    #             print(f"Request for batch {start}-{stop} failed with status code: {response.status_code}")
    #             # Handle the failure accordingly, e.g., retry or log error

    # # Convert the list of dictionaries to a DataFrame and concatenate it with the existing result_dataframe
    # new_data_df = pd.DataFrame(temp_data_list)
    # result_dataframe = pd.concat([result_dataframe, new_data_df], ignore_index=True)

    # print(f"Done. Results:\nTotal found in the request: {total_results}\nTotal fetched succesfully: {len(all_ids)}\nTotal unique ids: {len(set(all_ids))}\nTotal hiring team available: {hiring_team_counter}")

    # # Return the resulting dataframe as well as a set with everything we print out after the scrape. Bad practice, I know :))
    # return [result_dataframe, (len(all_ids), len(set(all_ids)), hiring_team_counter)]
        
# scraped_data_df, (total_fetched, total_unique, total_hiring_team) = scrape_linkedin_and_show_progress(keyword, total_number_of_results, employee_threshold, less_than_keywords, more_than_keywords)

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
#     if response.status_code_code == 200:
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

#     if response.status_code_code == 200:
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
#     if response.status_code_code == 200:
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
    
# company_segment = data.get('data', {}) \
#     .get('jobsDashJobPostingDetailSectionsByCardSectionTypes', {}) \
#     .get('elements', [{}])[0] \
#     .get('jobPostingDetailSection', [{}])[0] \
#     .get('companyCardV2', {}) \
#     .get('company', {}) \
#     .get('industryV2Taxonomy', [{}])[0] \
#     .get('name', None)

# INVISE: 3803170223
# result_dataframe = pd.DataFrame(columns=['Hiring Team', 'Förnamn', 'Efternamn', 'Bio', 'LinkedIn URL', 'Jobbtitel som sökes', 'Jobbannons-URL', 'Företag', 'Antal anställda', 'Företagssegment', 'Företags-URL'])
# counter = 0
# hiring_team_counter = 0
# temp_data_list = []

# def fetch_and_parse_company_segment(company_url, session):
#     try:
#         # Fetch the company page content asynchronously. Add headers if necessary
#         async with session.get(company_url) as company_response:
#             if company_response.status_code == 200:
#                 company_page_content = await company_response.text()

#                 # Parse the HTML content in a separate threat to avoid blocking
#                 def parse_html(content):
#                     soup = BeautifulSoup(content, 'html.parser')
#                     segment_div = soup.find('div', attrs={'class':'org-top-card-summary-info-list__info-item'})
#                     return segment_div.text if segment_div else None

#                 company_segment = time.to_thread(parse_html, company_page_content)
#                 return company_segment
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching pr parsing company page: {e}")
#     return None

# def extract_company_segment(job_posting_id, max_retries=1):
#     encoded_job_posting_id = quote(job_posting_id)
#     # api_request_url = f"https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&queryId=voyagerJobsDashJobPostingDetailSections.0a2eefbfd33e3ff566b3fbe31312c8ed&variables=(cardSectionTypes:List(COMPANY_CARD),jobPostingUrn:urn%3Ali%3Afsd_jobPosting%3A{encoded_job_posting_id},includeSecondaryActionsV2:true)"
#     api_request_url = f"https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(cardSectionTypes:List(COMPANY_CARD),jobPostingUrn:urn%3Ali%3Afsd_jobPosting%3A{encoded_job_posting_id},includeSecondaryActionsV2:true)&queryId=voyagerJobsDashJobPostingDetailSections.0a2eefbfd33e3ff566b3fbe31312c8ed"

#     payload = {}
#     headers = {
#     'accept': 'application/vnd.linkedin.normalized+json+2.1',
#     'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; liap=true; JSESSIONID="ajax:5371233139676576627"; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOtB0iaE0AQHehmeCXmo7JEQx3yzhQjkI1cvmPVd7EzPepRsZcwBgZaN9XMv4eSGcvul37iTmqpBD147YfRWhoW8-3x9ikT69bCEq_DRX8ACytmVxBtyl111Xf; lang=v=2&lang=en-us; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; li_mc=MTsyMTsxNzEyMTMyNjMyOzI7MDIxEOujgeP6A1uF93oEvaEg+fIAJjfK8Vs7qImxVpjeaz8=; UserMatchHistory=AQJVPgiTOiwfdAAAAY6jDr95_pWMNsUjTn69xHkgZEj9Ez4sQO2wBYEhmslKsa3P0suMzo-d_4QoDSYax4O0NGbzyTEKexrWpb777oYEKp9J2bBQGh6yd28i8G1arHkDC0DyqjHdCie9D8JPZoNBa4ms_n5HKpPfo460qqs0VMHmgoLtOUx-PveqG6D3BVOctHVOQ_MddhK8GdDit4JcAUCgsvje_7V02R0hMRGBxBwZsPrMfwj-O1U2EPGTmsRodndRn9jZ2INxkDl-vvw0p_abXhr7F5-XJ-L808to0dOlQqq10tHn1pOPmISnIFpd-QVmtbM; AnalyticsSyncHistory=AQInqKM9VjeJfgAAAY6jDr95ykAKgdVEJ-lmi2hFEpuwpHs0GW_s9vj-G4Uw6j1j_pUJJhZMGdSj03dRsS-GKQ; lms_ads=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; lms_analytics=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; lidc="b=OB74:s=O:r=O:a=O:p=O:g=4532:u=252:x=1:i=1712132637:t=1712136627:v=2:sig=AQFdII_5Lf9mKQxgOBkJHsM8_gwOxIoz"; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19817%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712737437%7C6%7CMCAAMB-1712737437%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1712139837s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvq1XHMHv0golcc9kyTlgPT0DQ7JBk5Weg1OFuj%252bBpbzR0yg1GKFeEO7FBR%252fAQh3%252fvoGMMS4yB67D9ec7jZcX51g1isL2VU7thmLU8lNVu23cEqSqzc23XEsnSvwUxxHx%252bzLkDNEGyOcJsJebOEcZWjWJvj90a49gGKwdqFTnBeghPmpl46CpkaXo%252b9ll0Y17aXNHqFPigu2LYSoW6N0pKT0M%253d; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTEzMDI5MjU7MjswMjEqcpbT05l8RjddPvbR76R/mVH9CGHsfxhK+QmNWHNGzA==; li_mc=MTsyMTsxNzEyMTMyNDQ3OzI7MDIxDRXUR1kLsrM78f0RNi8WYGUzAhl1iMPau6k9YeWDtFY=; liap=true; JSESSIONID="ajax:5371233139676576627"; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOw2TMvE0AFsDybLtUTmv0FMxT50kAEGZ9VsWUe-PpCGDBaJfv3cu3EFB2F9WewOHhiJ99vjDLoxliKYuiiM5nt_Ivx92s6DJMCE-owqou0cPCGFDhyL_Rmu5_',
#     'csrf-token': 'ajax:5371233139676576627'
#     }

#     
#         for attempt in range(max_retries):
#             try:
#                 async with session.get(api_request_url, headers=headers, data=payload) as response:
#                     # print("In the async session")
#                     # print(f"Headers: {headers}")
#                     # print(f"Response status: {response.status_code}")
#                     # response_text = response.text()
#                     # print(f"Response text: {response_text}")
#                     if response.status_code == 200:
#                         data = response.json()
#                         if data:
#                             company_segment = data.get('included', [{}])[1].get('name', None)
#                         print(f"Company segment: {company_segment}")

#                         return company_segment
#             except requests.exceptions.RequestException as e:
#                 print(f"Request failed: {e}")
#                 time.sleep(random.randint(3,5))    
#     return None   

# url_formatted_keywords = company_keywords.replace(', ', '%20OR%20').replace(' ', '%20OR%20').strip()    

# for person in result[1]:
#     hiring_team, full_name, bio, linkedin_url = person
#     first_name, last_name = split_and_clean_full_name(full_name)

#     results['Hiring Team'].append(hiring_team)
#     results['Förnamn'].append(first_name)
#     results['Efternamn'].append(last_name)
#     results['Bio'].append(bio)
#     results['LinkedIn URL'].append(linkedin_url)
#     results['Jobbtitel som sökes'].append(job_title)
#     results['Jobbannons-URL'].append(f"https://www.linkedin.com/jobs/search/?currentJobId={job_posting_id}&geoId=105117694&keywords={keyword}&location=Sweden")
#     results['Företag'].append(company_name)
#     results['Antal anställda'].append(employee_count)
#     results['Företagsindustri'].append(company_industry)
#     results['Företags-URL'].append(company_url)

# linkedin_job_url = "https://www.linkedin.com/jobs/search/?currentJobId=3836861341&keywords=sem%20seo&origin=SWITCH_SEARCH_VERTICAL"
# # linkedin_job_url = "https://www.linkedin.com/jobs/search/?currentJobId=3860933366&geoId=105117694&keywords=frontend%20developer&location=Sweden&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true"
# results_name = "linkedin_jobs_sem_seo_fully_working_temp.csv"

# start_time = time.time()
# print("Running...")
# keyword_search = re.search(r'keywords=([^&]+)', linkedin_job_url)
# keyword = keyword_search.group(1) if keyword_search else None
# print(f"Keyword: {keyword}")
# total_number_of_results = get_total_number_of_results(keyword)
# print(f"Total: {total_number_of_results}")
# batches = split_total_into_batches_of_100(total_number_of_results)
# print(f"Batches: {batches}")
# employee_threshold = 100
# under_threshold_keywords = "CEO, VD, Founder"
# over_threshold_keywords = "CMO, Head of Marketing, Marknadschef"
# max_people_per_company = 2

# grouped_results = main(keyword, batches, employee_threshold, under_threshold_keywords, over_threshold_keywords, max_people_per_company)
# end_time = time.time()
# # print(grouped_results)
# print(len(grouped_results))
# print(f"Done! Scraped info from {total_number_of_results} job ads in {end_time - start_time} seconds")

# df = turn_grouped_results_into_df(grouped_results)
# df.to_csv(results_name, index=False)

# with open ("times.txt", "a") as f:
#     f.write(f"Total: {total_number_of_results}, Time: {end_time - start_time}\n")

# construced_url = f"{company_url}/people/?keywords={url_formatted_keywords}"
# print(construced_url)
# job_posting_ids = extract_all_job_posting_ids(keyword, batches)
# # print(job_posting_ids)
# # job_posting_id = job_posting_ids[27]
# job_posting_id = "3852139384"
# print(job_posting_id)
# hiring_team_person = extract_full_name_bio_and_linkedin_url(job_posting_id)
# print(hiring_team_person)
# # # full_name, bio, url = hiring_team_person
# # company_info = extract_company_info(job_posting_id)
# # print(company_info)
# job_posting_id, job_title, company_name, employee_count, company_url, company_industry, companyID = extract_company_info(job_posting_id)
# company_keywords = under_threshold_keywords if employee_count <= employee_threshold else over_threshold_keywords
# print(company_keywords)
# company_people = extract_non_hiring_person(companyID, company_keywords, max_people_per_company)
# print(company_people)