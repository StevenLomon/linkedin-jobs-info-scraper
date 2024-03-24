import time, os, re, pickle, random, requests
import pandas  as pd
import streamlit as st
from rich import print, print_json

df = pd.DataFrame(columns=['Förnamn', 'Efternamn', 'LinkedIn URL', 'Företag'])

input_url = "https://www.linkedin.com/jobs/search/?currentJobId=3850239811&keywords=sem%20seo&origin=SWITCH_SEARCH_VERTICAL"
num_of_results = 100

# currentJobId = input[input.find("currentJobId=")+len("currentJobId="):input.find("currentJobId=")+len("currentJobId=")+10]
currentJobId = re.search(r'currentJobId=(\d+)', input_url).group(1)
# keyword = input_url[input_url.find("keywords=")+len("keywords="):input_url.rfind("&")]
keyword = re.search(r'keywords=([^&]+)', input_url).group(1)
keyword_clean = keyword.replace("%20", " ").strip()
print(keyword)
print(keyword_clean)
print(currentJobId)
# url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)"
url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-63&count={num_of_results}&q=jobSearch&query=(origin:HISTORY,keywords:{keyword},locationUnion:(geoId:105117694),selectedFilters:(distance:List(25.0)),spellCorrectionEnabled:true)&servedEventEnabled=false&start=0"

payload = {}
headers = {
  'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; sdsc=22%3A1%2C1710858906178%7EJAPP%2C0xEIgf1wexK6ckr83inbCVKAcTqI%3D; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AnalyticsSyncHistory=AQLQgW3RRkANCwAAAY5jOmkwk72r8IMTrd9st_hjdmoulqVl5geMen4LqgmF8K0AUn3R-jOxuSedvejsMpUyYg; lms_ads=AQE-j01C-ngGfAAAAY5jOmnPPxW1fk7yURo5p3BzckUP10_2GF31Wb6DTjp2ZQaXuFNEb99nBV3t4n9womVMaXKXpy9e5DeJ; lms_analytics=AQE-j01C-ngGfAAAAY5jOmnPPxW1fk7yURo5p3BzckUP10_2GF31Wb6DTjp2ZQaXuFNEb99nBV3t4n9womVMaXKXpy9e5DeJ; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvqwEPtNDIm57sxDEhWE7kvw8fC5u3jMvAKkvp%252fotUqPYieNgLFCCANfXirRCWZuLFSPdYL21J5slhS%252bQ1o%252fV2tDhrboPn27TYxYN3FUTDJvWhxaVME1vC3nfaq%252b2TOyoU392iU6cthqH%252fLCvPTWtubi48HjubwzjAE4baM%252bY%252bSAuJvXU9FGXao1fxLuAeo%252fVJlo13MP%252bcqsPuAX6kSRrUrFQ%253d; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19806%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1711790369%7C6%7CMCAAMB-1711790369%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711192769s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; li_mc=MTsyMTsxNzExMTkwMjE1OzI7MDIxyRFtLCwn+pkNNW9oYAvY5RDLHGa7S0son4v0fwpeczI=; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_g_recent_logout=v=1&true; visit=v=1&M; lang=v=2&lang=en-us; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; liap=true; JSESSIONID="ajax:5371233139676576627"; UserMatchHistory=AQJH9HVExKuEvQAAAY5q58JbFMoNxuK_4yHeRYryrMvAJHh4tJorRwgK13vsaO617yyfQhr3vKz2e6SnW2YP-8F_8xqIz_SMfNiyK-higtiBwc9CLSQnZgKfiC9WrmFFPnKpn8r1UDejBpUXRoHbhn3dnqPLrGEdbjpPkJHZ56LOnn5g1EmqSShtZhu7XK5iOhKLJR5ESXYhl8tgl-5ObCPDup6qlc7g2tZ9hKXoBg8vTrGdyVZhoO0HzxmovdosFQMPpcX-TjaxBXVz6onyjfxd5XXxlB1sR-h_AbkJ-grI3v9oH1tRRFA1MU0nkh2K4bReInY; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4151:u=247:x=1:i=1711190558:t=1711265066:v=2:sig=AQEhbOHG6b2NMBSek7ju52SyqY9s2vNB"; bcookie="v=2&4f26c9a6-f950-41d8-82cc-b41ec3caafa5"; li_mc=MTsyMTsxNzExMjYyNTI1OzI7MDIxxr788LY2gp/ql7Hm1zTLkN7QbgdW0J00Cs1RP/eztJ0=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4154:u=247:x=1:i=1711257936:t=1711297019:v=2:sig=AQEI3UFEfjQrzprvxRtR2ODZ2EXxFVpB"; JSESSIONID="ajax:5371233139676576627"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YFmyS7AAABjmrnuugAAAGOjvQ-6E0AY1fC-ANVhrSwjiNiqIhKYZ1Xib5nml6YE96LyvaMY3LATaVjueFFrqG8UXQNJz_kxu4qPIr20m8fm4URdNFCas5wngLRy2k8BJPw8UGUqCaqXKD7; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm',
  'csrf-token': 'ajax:5371233139676576627'
}

response = requests.request("GET", url, headers=headers, data=payload)

keyword = response.json()['metadata']['keywords']
# number_of_results = int(response.json()['metadata']['subtitle']['text'].split()[0])
number_of_results = response.json()['paging']['total']
all_jobs = response.json()['elements']
print(len(all_jobs))
posterIds = []
for job in all_jobs:
    posterId = job['jobCardUnion']['jobPostingCard']['jobPosting'].get('posterId', None)
    posterIds.append(posterId)
print(posterIds)

