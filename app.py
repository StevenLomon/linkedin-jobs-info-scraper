import time, re, requests, random
import pandas  as pd
import streamlit as st
from rich import print, print_json
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_total_number_of_results(keyword, max_retries=2):
    api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-67&count=25&q=jobSearch&query=(origin:SWITCH_SEARCH_VERTICAL,keywords:{keyword},spellCorrectionEnabled:true)&start=0"    
        
    payload = {}
    headers = {
        'accept': 'application/vnd.linkedin.normalized+json+2.1',
        'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AnalyticsSyncHistory=AQInqKM9VjeJfgAAAY6jDr95ykAKgdVEJ-lmi2hFEpuwpHs0GW_s9vj-G4Uw6j1j_pUJJhZMGdSj03dRsS-GKQ; lms_ads=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; lms_analytics=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19817%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712823944%7C6%7CMCAAMB-1712823944%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1712226344s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvqxsjRiMumDMdY2cZBC7rnBcwKqNM68r3TpZblRKHzhjqTvmVAWbcHGdsb5IwTFqJY%252fMUYh2Qg2S1xLvrOKsF819j5MizM%252fQkmqKNoUidY7bXjPqOzaXZfqS9qrp55bj79ludUr4VLcG1FqHXzI%252fnEZb6Gg8pzytrnrgQFlDD4qhZPoL773oMaOt5Xu7Zj6UYRpAMqFbr0QakvMVWMSvw93s%253d; li_g_recent_logout=v=1&true; lang=v=2&lang=en-us; li_at=AQEDASvMh7YD9s79AAABjqiLGqYAAAGOzJeepk0AeYx2DWyrkdJ2zOVnqqljd2pif0w70vXt5CAmfT-Fzviq450QuPbnNpN17uHRhNTjn38eeZfAzJg70FJChZAL8U0ElXl--_qooC9a45fdzqkaU7Sv; liap=true; JSESSIONID="ajax:2715582253737539260"; li_mc=MTsyMTsxNzEyMjI0NzMyOzI7MDIxzODtaxUnhH03NiFJxX2nAcg+Zt1SBwH5NvsRAxtAtmk=; UserMatchHistory=AQKpLFT71zoM5QAAAY6olBvzmoHGZBhPQlhG2QJfDL6VSRwwrqxGU5OYng_P7oC3i705LjK1mJLCoudXGg-J0NDW4inNM4LtM90f1IHjAKPkiKBQOsqx7x89ZsAUgQ_Id-tKl50XVNuPZnAfsIVhngEuxkV6538FxYjln7OKcc94E830eKTIGCzm9sUFevFdtaLpUziPshqg7A5qPAlpsBx_ltoEvRBdb6eZSTz-zYDAogKN9htKasaYbT-8BPcjbuJVhvAmT24k4rFh07c3Zx78yU0PaPxnN68ue8yS7BangTpKgFAr9JustG_rujNj9mHuB9A; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4190:u=253:x=1:i=1712225263:t=1712308566:v=2:sig=AQGNtWMcukq66YUQAxEHE2Y2woh1guTQ"; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19817%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712823944%7C6%7CMCAAMB-1712823944%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1712226344s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; AnalyticsSyncHistory=AQInqKM9VjeJfgAAAY6jDr95ykAKgdVEJ-lmi2hFEpuwpHs0GW_s9vj-G4Uw6j1j_pUJJhZMGdSj03dRsS-GKQ; UserMatchHistory=AQKz6POJSiLt1AAAAY6okULilyFDXuLLHMAMYVzy-IMAs6Dlwno_fksOjnrsAnsZpD2MUiiNSG9oGzLrbQNa4N5CTJqA0FOGwUAH3-vZ9blAScHMZjWEElHwe_wJf4WbR02jFr8oZXirGt2T5fmAiHm_27xgkRrk0ivUr11nWHvdhh6l_QpEkhkJhkL1gItuDoH1ok95GHg4SC0rIoD7Txfw0C_QUZnpE8oMvyyScBkPIIwEBHuDwDKIW9Bd8LPkVpLt-FRLcxHxceXm1RjE12H6A3hq8Hmugcmg5htGzvIiW-lBiKnLsYGUSPowBkKdDtoFxVk; __cf_bm=46m5tvraQgrQpHhlW.Lwh9JA1WKE1fNfwR6JoACj1tc-1712225398-1.0.1.1-nXNAZAkaZHgAm2sBxkPt_tsSjFNf8oliPxZqefYXuc9oq6O6Lbwhyr7mIKovqCN1.OeYtBp7PvBct4AgSGNnUw; _gcl_au=1.1.308589430.1710419664; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; aam_uuid=16424388958969701103162659259461292262; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvqxsjRiMumDMdY2cZBC7rnBcwKqNM68r3TpZblRKHzhjqTvmVAWbcHGdsb5IwTFqJY%252fMUYh2Qg2S1xLvrOKsF819j5MizM%252fQkmqKNoUidY7bXjPqOzaXZfqS9qrp55bj79ludUr4VLcG1FqHXzI%252fnEZb6Gg8pzytrnrgQFlDD4qhZPoL773oMaOt5Xu7Zj6UYRpAMqFbr0QakvMVWMSvw93s%253d; lang=v=2&lang=en-us; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; li_mc=MTsyMTsxNzEyMjI1NDc1OzI7MDIx4g1UjJLNxrgq1LN73193ANa7nJGrX7QYtI3diLCYb2I=; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; liap=true; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4190:u=253:x=1:i=1712225077:t=1712308566:v=2:sig=AQFhNZWPI_v5oL4y8oX9xLFL8a3cbxtv"; lms_ads=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; lms_analytics=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; test=cookie; visit=v=1&M; JSESSIONID="ajax:2715582253737539260"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YD9s79AAABjqiLGqYAAAGOzJeepk0AeYx2DWyrkdJ2zOVnqqljd2pif0w70vXt5CAmfT-Fzviq450QuPbnNpN17uHRhNTjn38eeZfAzJg70FJChZAL8U0ElXl--_qooC9a45fdzqkaU7Sv; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm',
        'csrf-token': 'ajax:2715582253737539260',
        'sec-fetch-mode': 'cors'
    }

    for attempt in range(max_retries):
        try:
            response = requests.request("GET", api_request_url, headers=headers, data=payload)
            if response.status_code == 200:
                data = response.json()
                total = None
                paging = data.get('data', {}).get('paging', {})
                if paging:
                    total = paging.get('total')
                
                if isinstance(total, int):
                    return total
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(random.randint(3,5))
    return None     

# We can only fetch 100 at a time
def split_total_into_batches_of_100(total):
    batches = [(i, i + 100) for i in range(0, total, 100)]
    # Adjust the last batch to not exceed the total
    if batches:
        batches[-1] = (batches[-1][0], total)
    return batches

def fetch_job_posting_ids(keyword, batch, max_retries=2):
    start, stop = batch
    batch_size = stop - start

    api_request_url = f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-67&count={batch_size}&q=jobSearch&query=(origin:SWITCH_SEARCH_VERTICAL,keywords:{keyword},spellCorrectionEnabled:true)&start={start}"
    headers = {
        'accept': 'application/vnd.linkedin.normalized+json+2.1',
        'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AnalyticsSyncHistory=AQInqKM9VjeJfgAAAY6jDr95ykAKgdVEJ-lmi2hFEpuwpHs0GW_s9vj-G4Uw6j1j_pUJJhZMGdSj03dRsS-GKQ; lms_ads=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; lms_analytics=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19817%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712823944%7C6%7CMCAAMB-1712823944%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1712226344s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvqxsjRiMumDMdY2cZBC7rnBcwKqNM68r3TpZblRKHzhjqTvmVAWbcHGdsb5IwTFqJY%252fMUYh2Qg2S1xLvrOKsF819j5MizM%252fQkmqKNoUidY7bXjPqOzaXZfqS9qrp55bj79ludUr4VLcG1FqHXzI%252fnEZb6Gg8pzytrnrgQFlDD4qhZPoL773oMaOt5Xu7Zj6UYRpAMqFbr0QakvMVWMSvw93s%253d; li_g_recent_logout=v=1&true; lang=v=2&lang=en-us; li_at=AQEDASvMh7YD9s79AAABjqiLGqYAAAGOzJeepk0AeYx2DWyrkdJ2zOVnqqljd2pif0w70vXt5CAmfT-Fzviq450QuPbnNpN17uHRhNTjn38eeZfAzJg70FJChZAL8U0ElXl--_qooC9a45fdzqkaU7Sv; liap=true; JSESSIONID="ajax:2715582253737539260"; li_mc=MTsyMTsxNzEyMjI0NzMyOzI7MDIxzODtaxUnhH03NiFJxX2nAcg+Zt1SBwH5NvsRAxtAtmk=; UserMatchHistory=AQKpLFT71zoM5QAAAY6olBvzmoHGZBhPQlhG2QJfDL6VSRwwrqxGU5OYng_P7oC3i705LjK1mJLCoudXGg-J0NDW4inNM4LtM90f1IHjAKPkiKBQOsqx7x89ZsAUgQ_Id-tKl50XVNuPZnAfsIVhngEuxkV6538FxYjln7OKcc94E830eKTIGCzm9sUFevFdtaLpUziPshqg7A5qPAlpsBx_ltoEvRBdb6eZSTz-zYDAogKN9htKasaYbT-8BPcjbuJVhvAmT24k4rFh07c3Zx78yU0PaPxnN68ue8yS7BangTpKgFAr9JustG_rujNj9mHuB9A; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4190:u=253:x=1:i=1712225263:t=1712308566:v=2:sig=AQGNtWMcukq66YUQAxEHE2Y2woh1guTQ"; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19817%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712823944%7C6%7CMCAAMB-1712823944%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1712226344s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; AnalyticsSyncHistory=AQInqKM9VjeJfgAAAY6jDr95ykAKgdVEJ-lmi2hFEpuwpHs0GW_s9vj-G4Uw6j1j_pUJJhZMGdSj03dRsS-GKQ; UserMatchHistory=AQKz6POJSiLt1AAAAY6okULilyFDXuLLHMAMYVzy-IMAs6Dlwno_fksOjnrsAnsZpD2MUiiNSG9oGzLrbQNa4N5CTJqA0FOGwUAH3-vZ9blAScHMZjWEElHwe_wJf4WbR02jFr8oZXirGt2T5fmAiHm_27xgkRrk0ivUr11nWHvdhh6l_QpEkhkJhkL1gItuDoH1ok95GHg4SC0rIoD7Txfw0C_QUZnpE8oMvyyScBkPIIwEBHuDwDKIW9Bd8LPkVpLt-FRLcxHxceXm1RjE12H6A3hq8Hmugcmg5htGzvIiW-lBiKnLsYGUSPowBkKdDtoFxVk; __cf_bm=46m5tvraQgrQpHhlW.Lwh9JA1WKE1fNfwR6JoACj1tc-1712225398-1.0.1.1-nXNAZAkaZHgAm2sBxkPt_tsSjFNf8oliPxZqefYXuc9oq6O6Lbwhyr7mIKovqCN1.OeYtBp7PvBct4AgSGNnUw; _gcl_au=1.1.308589430.1710419664; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; aam_uuid=16424388958969701103162659259461292262; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvqxsjRiMumDMdY2cZBC7rnBcwKqNM68r3TpZblRKHzhjqTvmVAWbcHGdsb5IwTFqJY%252fMUYh2Qg2S1xLvrOKsF819j5MizM%252fQkmqKNoUidY7bXjPqOzaXZfqS9qrp55bj79ludUr4VLcG1FqHXzI%252fnEZb6Gg8pzytrnrgQFlDD4qhZPoL773oMaOt5Xu7Zj6UYRpAMqFbr0QakvMVWMSvw93s%253d; lang=v=2&lang=en-us; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; li_mc=MTsyMTsxNzEyMjI1NDc1OzI7MDIx4g1UjJLNxrgq1LN73193ANa7nJGrX7QYtI3diLCYb2I=; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; liap=true; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4190:u=253:x=1:i=1712225077:t=1712308566:v=2:sig=AQFhNZWPI_v5oL4y8oX9xLFL8a3cbxtv"; lms_ads=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; lms_analytics=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; test=cookie; visit=v=1&M; JSESSIONID="ajax:2715582253737539260"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YD9s79AAABjqiLGqYAAAGOzJeepk0AeYx2DWyrkdJ2zOVnqqljd2pif0w70vXt5CAmfT-Fzviq450QuPbnNpN17uHRhNTjn38eeZfAzJg70FJChZAL8U0ElXl--_qooC9a45fdzqkaU7Sv; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm',
        'csrf-token': 'ajax:2715582253737539260',
        'sec-fetch-mode': 'cors'
        }

    job_posting_ids_list = []
    for attempt in range(max_retries):
        try:
            response = requests.request("GET", api_request_url, headers=headers)
            if response.status_code == 200:
                data = response.json()

                # Navigate to jobCardPrefetchQueries and get the first item's prefetchJobPostingCardUrns
                prefetch_job_posting_card_urns = data.get('data', {}) \
                                                    .get('metadata', {}) \
                                                    .get('jobCardPrefetchQueries', [{}])[0] \
                                                    .get('prefetchJobPostingCardUrns', [])
                for urn in prefetch_job_posting_card_urns:
                    job_posting_id_search = re.search(r"urn:li:fsd_jobPostingCard:\((\d+),JOB_DETAILS\)", urn)
                    if job_posting_id_search:
                        job_posting_id = job_posting_id_search.group(1)
                        job_posting_ids_list.append(job_posting_id)

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(random.randint(3,5))
    return job_posting_ids_list #Return the list, even if its empty

def extract_all_job_posting_ids(keyword, batches):
    job_posting_ids = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(fetch_job_posting_ids, keyword, batch) for batch in batches]
        for future in as_completed(futures):
            job_posting_ids.extend(future.result())
    return job_posting_ids

def extract_full_name_bio_and_linkedin_url(job_posting_id, max_retries=2):
    api_request_url = f"https://www.linkedin.com/voyager/api/graphql?variables=(cardSectionTypes:List(HIRING_TEAM_CARD),jobPostingUrn:urn%3Ali%3Afsd_jobPosting%3A{job_posting_id},includeSecondaryActionsV2:true)&queryId=voyagerJobsDashJobPostingDetailSections.0a2eefbfd33e3ff566b3fbe31312c8ed"
    headers = {
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AnalyticsSyncHistory=AQInqKM9VjeJfgAAAY6jDr95ykAKgdVEJ-lmi2hFEpuwpHs0GW_s9vj-G4Uw6j1j_pUJJhZMGdSj03dRsS-GKQ; lms_ads=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; lms_analytics=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19817%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712823944%7C6%7CMCAAMB-1712823944%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1712226344s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvqxsjRiMumDMdY2cZBC7rnBcwKqNM68r3TpZblRKHzhjqTvmVAWbcHGdsb5IwTFqJY%252fMUYh2Qg2S1xLvrOKsF819j5MizM%252fQkmqKNoUidY7bXjPqOzaXZfqS9qrp55bj79ludUr4VLcG1FqHXzI%252fnEZb6Gg8pzytrnrgQFlDD4qhZPoL773oMaOt5Xu7Zj6UYRpAMqFbr0QakvMVWMSvw93s%253d; li_g_recent_logout=v=1&true; lang=v=2&lang=en-us; li_at=AQEDASvMh7YD9s79AAABjqiLGqYAAAGOzJeepk0AeYx2DWyrkdJ2zOVnqqljd2pif0w70vXt5CAmfT-Fzviq450QuPbnNpN17uHRhNTjn38eeZfAzJg70FJChZAL8U0ElXl--_qooC9a45fdzqkaU7Sv; liap=true; JSESSIONID="ajax:2715582253737539260"; li_mc=MTsyMTsxNzEyMjI0NzMyOzI7MDIxzODtaxUnhH03NiFJxX2nAcg+Zt1SBwH5NvsRAxtAtmk=; UserMatchHistory=AQKpLFT71zoM5QAAAY6olBvzmoHGZBhPQlhG2QJfDL6VSRwwrqxGU5OYng_P7oC3i705LjK1mJLCoudXGg-J0NDW4inNM4LtM90f1IHjAKPkiKBQOsqx7x89ZsAUgQ_Id-tKl50XVNuPZnAfsIVhngEuxkV6538FxYjln7OKcc94E830eKTIGCzm9sUFevFdtaLpUziPshqg7A5qPAlpsBx_ltoEvRBdb6eZSTz-zYDAogKN9htKasaYbT-8BPcjbuJVhvAmT24k4rFh07c3Zx78yU0PaPxnN68ue8yS7BangTpKgFAr9JustG_rujNj9mHuB9A; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4190:u=253:x=1:i=1712225263:t=1712308566:v=2:sig=AQGNtWMcukq66YUQAxEHE2Y2woh1guTQ"; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19817%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712823944%7C6%7CMCAAMB-1712823944%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1712226344s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; AnalyticsSyncHistory=AQInqKM9VjeJfgAAAY6jDr95ykAKgdVEJ-lmi2hFEpuwpHs0GW_s9vj-G4Uw6j1j_pUJJhZMGdSj03dRsS-GKQ; UserMatchHistory=AQKz6POJSiLt1AAAAY6okULilyFDXuLLHMAMYVzy-IMAs6Dlwno_fksOjnrsAnsZpD2MUiiNSG9oGzLrbQNa4N5CTJqA0FOGwUAH3-vZ9blAScHMZjWEElHwe_wJf4WbR02jFr8oZXirGt2T5fmAiHm_27xgkRrk0ivUr11nWHvdhh6l_QpEkhkJhkL1gItuDoH1ok95GHg4SC0rIoD7Txfw0C_QUZnpE8oMvyyScBkPIIwEBHuDwDKIW9Bd8LPkVpLt-FRLcxHxceXm1RjE12H6A3hq8Hmugcmg5htGzvIiW-lBiKnLsYGUSPowBkKdDtoFxVk; __cf_bm=4CjrjV9LRvgqYwoA8OS1IyjQ7zH3YVil1zG0JmeJpeo-1712228179-1.0.1.1-eLHLoYutjvXBo4GP8r1gedbr1ZJCFp3NxwBNOQmMKxL0vYZzyhMKm1vSPtJNItNyNJVzPeN0y_iwqb95HuDArA; _gcl_au=1.1.308589430.1710419664; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; aam_uuid=16424388958969701103162659259461292262; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvqxsjRiMumDMdY2cZBC7rnBcwKqNM68r3TpZblRKHzhjqTvmVAWbcHGdsb5IwTFqJY%252fMUYh2Qg2S1xLvrOKsF819j5MizM%252fQkmqKNoUidY7bXjPqOzaXZfqS9qrp55bj79ludUr4VLcG1FqHXzI%252fnEZb6Gg8pzytrnrgQFlDD4qhZPoL773oMaOt5Xu7Zj6UYRpAMqFbr0QakvMVWMSvw93s%253d; lang=v=2&lang=en-us; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; li_mc=MTsyMTsxNzEyMjI4MjAwOzI7MDIxb94IJj2ruSLZxsh1Efnbk8prKJ9zkDCjFP/uVoEiGwc=; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; liap=true; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4190:u=253:x=1:i=1712225077:t=1712308566:v=2:sig=AQFhNZWPI_v5oL4y8oX9xLFL8a3cbxtv"; lms_ads=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; lms_analytics=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; test=cookie; visit=v=1&M; JSESSIONID="ajax:2715582253737539260"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YD9s79AAABjqiLGqYAAAGOzJeepk0AeYx2DWyrkdJ2zOVnqqljd2pif0w70vXt5CAmfT-Fzviq450QuPbnNpN17uHRhNTjn38eeZfAzJg70FJChZAL8U0ElXl--_qooC9a45fdzqkaU7Sv; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm',
    'csrf-token': 'ajax:2715582253737539260',
    'sec-fetch-mode': 'cors'
    }

    full_name = bio = linkedin_url = None

    for attempt in range(max_retries):
        try:
            response = requests.request("GET", api_request_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                elements = data.get('data', {}) \
                .get('data', {}) \
                .get('jobsDashJobPostingDetailSectionsByCardSectionTypes', {}) \
                .get('elements', [])

                if elements:
                    jobPostingDetailSection = elements[0].get('jobPostingDetailSection', [])
                    if jobPostingDetailSection:
                        hiring_team_card = jobPostingDetailSection[0].get('hiringTeamCard', {})
                        if hiring_team_card:
                            full_name = hiring_team_card.get('title', {}).get('text', None)
                            bio = hiring_team_card.get('subtitle', {}).get('text', None)
                            linkedin_url = hiring_team_card.get('navigationUrl')
                            return (full_name, bio, linkedin_url)
                    
                    return (full_name, bio, linkedin_url)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(random.randint(3,5))
    return None, None, None  # Return None if all attempts fail

def split_and_clean_full_name(full_name):
    # Remove parentheses and content within them
    cleaned_name = re.sub(r'\(.*?\)', '', full_name)
    # Further clean the name by removing any non-word and non-space characters
    cleaned_name = re.sub(r'[^\w\s]', '', cleaned_name, flags=re.UNICODE)
    name_parts = cleaned_name.split()
    first_name = name_parts[0] # We assume the first part will always be the first name after removing emojis etc
    last_name = name_parts[-1] if len(name_parts) > 1 else ''  # Check to avoid index error if name_parts is empty
    return (first_name, last_name)

def extract_company_info(job_posting_id, max_retries=2):
    api_request_url = f"https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_posting_id}?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65"
    headers = {
    'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AnalyticsSyncHistory=AQInqKM9VjeJfgAAAY6jDr95ykAKgdVEJ-lmi2hFEpuwpHs0GW_s9vj-G4Uw6j1j_pUJJhZMGdSj03dRsS-GKQ; lms_ads=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; lms_analytics=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvqxsjRiMumDMdY2cZBC7rnBcwKqNM68r3TpZblRKHzhjqTvmVAWbcHGdsb5IwTFqJY%252fMUYh2Qg2S1xLvrOKsF819j5MizM%252fQkmqKNoUidY7bXjPqOzaXZfqS9qrp55bj79ludUr4VLcG1FqHXzI%252fnEZb6Gg8pzytrnrgQFlDD4qhZPoL773oMaOt5Xu7Zj6UYRpAMqFbr0QakvMVWMSvw93s%253d; lang=v=2&lang=en-us; li_at=AQEDASvMh7YD9s79AAABjqiLGqYAAAGOzJeepk0AeYx2DWyrkdJ2zOVnqqljd2pif0w70vXt5CAmfT-Fzviq450QuPbnNpN17uHRhNTjn38eeZfAzJg70FJChZAL8U0ElXl--_qooC9a45fdzqkaU7Sv; liap=true; JSESSIONID="ajax:2715582253737539260"; li_mc=MTsyMTsxNzEyMjMxMjI0OzI7MDIxEmEZDdiE8GxoqN6bX3J51PVMWKjq87vUcQ1i/o/0Ud4=; __cf_bm=K9OPT3Ix0HrD_IlTjDYANLCxbMHYJZSLqN7MszCxptk-1712231585-1.0.1.1-QVawzdfwQRsHtxtjtR7t68YJ9yfJeneTlD.32ll7xwvsdS1kKIo3SABPdttcUeIR0iPsRDtjdb_q7N0lslqcmQ; UserMatchHistory=AQK6RfznW9o3xgAAAY6o97vkHlUeIQxGEtFzhFDFtcdFCAXQ665jLZTUQDt5EhpMFQPjk2WmeQ7Qb0Db1YCn9tJiBpIEo24K6w78N264yKbaelqGwpS16pEbCoTE7zROlWUm2CITfdk6Ka-JMPL3lgfwFi-7PTXMmQZ4D-D3HeLdlP0_xeMBiY8tpy_H1dc8ygAfahxdFkzHoNjZzcGoG6K-iev7nQDQr2bneg1hPH83U2INoZLyhWxpLrasJDC9Ks3NS3bDogocBkI7-1qwGLs4i-MUfsc0aKJXkf6qgidM0r3IDfnl9wNXruOvgsPsXgRL3tw; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4190:u=253:x=1:i=1712231793:t=1712308566:v=2:sig=AQFzt72littBzVmdj0NAzrfjuaRlQspM"; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19817%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712836595%7C6%7CMCAAMB-1712836595%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1712238995s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19817%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712823944%7C6%7CMCAAMB-1712823944%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1712226344s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; AnalyticsSyncHistory=AQInqKM9VjeJfgAAAY6jDr95ykAKgdVEJ-lmi2hFEpuwpHs0GW_s9vj-G4Uw6j1j_pUJJhZMGdSj03dRsS-GKQ; UserMatchHistory=AQKz6POJSiLt1AAAAY6okULilyFDXuLLHMAMYVzy-IMAs6Dlwno_fksOjnrsAnsZpD2MUiiNSG9oGzLrbQNa4N5CTJqA0FOGwUAH3-vZ9blAScHMZjWEElHwe_wJf4WbR02jFr8oZXirGt2T5fmAiHm_27xgkRrk0ivUr11nWHvdhh6l_QpEkhkJhkL1gItuDoH1ok95GHg4SC0rIoD7Txfw0C_QUZnpE8oMvyyScBkPIIwEBHuDwDKIW9Bd8LPkVpLt-FRLcxHxceXm1RjE12H6A3hq8Hmugcmg5htGzvIiW-lBiKnLsYGUSPowBkKdDtoFxVk; _gcl_au=1.1.308589430.1710419664; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; aam_uuid=16424388958969701103162659259461292262; bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvqxsjRiMumDMdY2cZBC7rnBcwKqNM68r3TpZblRKHzhjqTvmVAWbcHGdsb5IwTFqJY%252fMUYh2Qg2S1xLvrOKsF819j5MizM%252fQkmqKNoUidY7bXjPqOzaXZfqS9qrp55bj79ludUr4VLcG1FqHXzI%252fnEZb6Gg8pzytrnrgQFlDD4qhZPoL773oMaOt5Xu7Zj6UYRpAMqFbr0QakvMVWMSvw93s%253d; lang=v=2&lang=en-us; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; li_mc=MTsyMTsxNzEyMjMyMjk5OzI7MDIxuC3zI1LQwxwweI0/TTbN/C4WmBh+e9F0RtAxD38DujI=; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; liap=true; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4190:u=253:x=1:i=1712225077:t=1712308566:v=2:sig=AQFhNZWPI_v5oL4y8oX9xLFL8a3cbxtv"; lms_ads=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; lms_analytics=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; test=cookie; visit=v=1&M; JSESSIONID="ajax:2715582253737539260"; g_state={"i_l":0}; li_alerts=e30=; li_at=AQEDASvMh7YD9s79AAABjqiLGqYAAAGOzJeepk0AeYx2DWyrkdJ2zOVnqqljd2pif0w70vXt5CAmfT-Fzviq450QuPbnNpN17uHRhNTjn38eeZfAzJg70FJChZAL8U0ElXl--_qooC9a45fdzqkaU7Sv; li_g_recent_logout=v=1&true; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; li_theme=light; li_theme_set=app; timezone=Europe/Stockholm',
    'csrf-token': 'ajax:2715582253737539260',
    'sec-fetch-mode': 'cors'
    }

    for attempt in range(max_retries):
        try:
            response = requests.request("GET", api_request_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                job_title = data.get('title', None)

                companyResolutionResult = data.get('companyDetails', {}) \
                    .get('com.linkedin.voyager.deco.jobs.web.shared.WebJobPostingCompany', {}) \
                    .get('companyResolutionResult', {})
                company_name = companyResolutionResult.get('name', None)
                employee_count = companyResolutionResult.get('staffCount', None)
                companyID_search = re.search(r'(\d+)$', companyResolutionResult.get('entityUrn', ''))
                companyID = companyID_search.group(1) if companyID_search else None
                company_url = companyResolutionResult.get('url', None)
                industries = companyResolutionResult.get('industries', [])
                company_industry = industries[0] if industries else None

                return (job_title, company_name, employee_count, company_url, company_industry, companyID)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(random.randint(3,5))
    return None, None, None, None, None, None

def extract_non_hiring_person(company_id, keywords, max_people_per_company, max_retries=2): 
    keywords_list = keywords.lower().split(", ")
    url_formatted_keywords = keywords.strip().replace(', ', '%20OR%20').replace(' ', '%20')
    
    api_request_url = f"https://www.linkedin.com/voyager/api/graphql?variables=(start:0,origin:FACETED_SEARCH,query:(keywords:{url_formatted_keywords},flagshipSearchIntent:ORGANIZATIONS_PEOPLE_ALUMNI,queryParameters:List((key:currentCompany,value:List({company_id})),(key:resultType,value:List(ORGANIZATION_ALUMNI))),includeFiltersInResponse:true),count:12)&queryId=voyagerSearchDashClusters.aacf309cb55f24005e058d2cf30a95ad"
    headers = {
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'cookie': 'bcookie="v=2&21324318-35a4-4b89-8ccd-66085ea456e6"; li_gc=MTswOzE3MTA0MTk0MzU7MjswMjE2GFD4tGaA955A7K5M9w3OxKao0REV7R8R3/LDZ/ZVJQ==; bscookie="v=1&202403141230369a2ffb3d-11be-445e-8196-32de3e951a31AQFV3WHayzR8g95w6TJ6LrZlOyXvi0m3"; li_alerts=e30=; g_state={"i_l":0}; timezone=Europe/Stockholm; li_theme=light; li_theme_set=app; _guid=9d344ac1-8a69-44f0-ba51-4e8884d4ccac; li_sugr=6fadc81f-40bf-4c11-9bc8-f36f95783541; _gcl_au=1.1.308589430.1710419664; aam_uuid=16424388958969701103162659259461292262; dfpfpt=2585905f65d4454db4b2923a3ee8bc24; li_rm=AQHjnJLrN-yKBQAAAY5q4y9R8BRBllyhPbBn5d_YYX2L59W6HxE_DqKNA8I0kMJ65IWgm2p2lw6Nr-GtGaWvKLjdLWcGo7lk7TxomWVYVRCBBwCg0vdKIUKRO5r3HtOd-9SY1a3tgovir_swKutrRj18DIt1HyV6JLLjK7r_2_Q3Y17vc2CH16R-MR9JvdZ43vTF0Y3FC9phhH2YQIfsbFlThT369bNJPiiDf9KdkGjeERmZH7RAG2iu0b7jY6iAidzkyplMV_nmlyqO_-v-2dRjfqjTYSjZwx0D046PpPzLEu1Vy7RK5SBlfPOm2djsHD8H4sQ32JlCErdlwYI; visit=v=1&M; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AnalyticsSyncHistory=AQInqKM9VjeJfgAAAY6jDr95ykAKgdVEJ-lmi2hFEpuwpHs0GW_s9vj-G4Uw6j1j_pUJJhZMGdSj03dRsS-GKQ; lms_ads=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; lms_analytics=AQEPbpVkVUBMJwAAAY6jDsDdSL3Mw1m_OduZrR3hlmqPxRHRs1Ajcc5Zo_Z8pOj-Kl3vtbYD-sa69Co_lrctHDJKkWtAjACm; lang=v=2&lang=en-us; li_at=AQEDASvMh7YD9s79AAABjqiLGqYAAAGOzJeepk0AeYx2DWyrkdJ2zOVnqqljd2pif0w70vXt5CAmfT-Fzviq450QuPbnNpN17uHRhNTjn38eeZfAzJg70FJChZAL8U0ElXl--_qooC9a45fdzqkaU7Sv; liap=true; JSESSIONID="ajax:2715582253737539260"; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCkAr9en60wAbfeXvyW5bYQhcX76e9lzuPfcckEKYDk1omjn%252fBbajvM3A%252f0ra5KWWbn6CpB5ts0e8OrCs%252bDiqyP2v4aXF1Cod4M2QlHSbNcvqyIS3EHNCaQb1yqedO0SnYQMhwbJN8ySTkCer5wo%252boj3R6Kjve%252b4U7H4WVzqtUgXP7YM6GRQ85K3mDGXrbXg4ZNAFi8w%252bd5zuD%252bFIZ37zTZrbmHBabFntMHiqadB2DZiIaiWEgi%252fl1%252f%252fl1OFnBVL7ugO%252bj6bBBXxf2utkvg%252f%252fWY17NNVTXALlWyLCFcF9%252f%252fzFWz1bRB4FQl%252bLi2QIrLZ704%253d; li_mc=MTsyMTsxNzEyMzI2NTUxOzI7MDIxftb6aAVYVH8gDfsXaIlY3yeEj2uLVVHmOTq0a9yzQuA=; __cf_bm=MMMJZ77oY71_nUapoBIXf53UsEJngGvFl8HAcWNdXdo-1712326552-1.0.1.1-c3FwEI2LnDeCVPYN5aHWT.6roD15mx72mX_UDcXebBQKEiof3DkT_mxqF9tTZd2Gf53MFfnzBo6qYs6TzJhimg; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19819%7CMCMID%7C15864482448327108373110627159475528493%7CMCAAMLH-1712931354%7C6%7CMCAAMB-1712931354%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1712333754s%7CNONE%7CMCCIDH%7C-1259936587%7CvVersion%7C5.1.1; UserMatchHistory=AQIdxcAxC5cMuAAAAY6unqyHEzSFed0QmxyjHcYParVnDqvlBeBYOGzNn0wTj7EPMPwsdad0g63r8sUggTv0RYtoHjEbBQM1BddULbdJZMqB0jgeATGwUSvpHDz2HbNnUeMXt_-AG34fekU0NKkR-QB6GSIWrxgp7OwxMNNmOTdFO1LAN8eGCJjSsVdlZld1kxYvPkgRrwgldSmrmxaNIYf4HmzDvSNAn81fFZjjbM282dCx-Eq1yuTrlstYQ-lJLpXWL3m_JNJmVNrN7tZGUUNnX8rWhqK2c2XqZIJQfgzopJ59VhuaYrXvYm7YoyKLm5N4ljg; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4206:u=253:x=1:i=1712326620:t=1712391543:v=2:sig=AQGUjv2njj0nMPTaqNmrFV0FtUrlqPGL"; bcookie="v=2&70aaf49d-ed55-4b5c-8362-d0eba01b2555"; li_gc=MTswOzE3MTIzMjQ1NDQ7MjswMjH7F5RtGOB+6km5SD86xeRCXtAv1pzxFaZgc9eOZ6nlGQ==; li_mc=MTsyMTsxNzEyMzEwNjM4OzI7MDIxtt/UHTCJyTLYmxgG2aQ96q5IGk7uCVBxDqWoZ+zeaDs=; lidc="b=VB74:s=V:r=V:a=V:p=V:g=4206:u=253:x=1:i=1712326742:t=1712391543:v=2:sig=AQEGOhcsViLtSujkKRWPUgMfRKtbxSEg"',
    'csrf-token': 'ajax:2715582253737539260',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    for attempt in range(max_retries):
        try:
            time.sleep(random.randint(1,3))
            response = requests.request("GET", api_request_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # print(f"Data: {data}")
                included = data.get('included', [{}])

                # Filter out any items in 'included' that don't represent a person based on a minimum number of keys
                filtered_people = [person for person in included if len(person) >= 5]
                # print(filtered_people[:300])
                
                processed = []
                for person in filtered_people:
                    if  len(processed) >= max_people_per_company:
                        break # Exit the loop once we have enough people

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
                    
                    is_present = any(title in bio.lower() for title in keywords_list)
                    if is_present:
                        processed.append(("FALSE", full_name, bio, linkedin_url_result))

                return processed
            else:
                time.sleep(random.randint(3,5))
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(random.randint(3,5))
    return []

def hiring_person_or_not(job_posting_id, employee_threshold, under_threshold_keywords, over_threshold_keywords, max_people_per_company):
    full_name = bio = linkedin_url = None
    full_name, bio, linkedin_url = extract_full_name_bio_and_linkedin_url(job_posting_id)
    if full_name and bio and linkedin_url:
        hiring_team = "TRUE"
        return [(hiring_team, full_name, bio, linkedin_url)]
    else:
        job_title, company_name, employee_count, company_url, company_industry, companyID = extract_company_info(job_posting_id)

        if employee_count:
            company_keywords = under_threshold_keywords if employee_count <= employee_threshold else over_threshold_keywords    
            company_people = extract_non_hiring_person(companyID, company_keywords, max_people_per_company)
            return company_people
        else:
            return []

def main(keyword, batches, employee_threshold, under_threshold_keywords, over_threshold_keywords, max_people_per_company, max_workers=5):
    all_job_posting_ids = extract_all_job_posting_ids(keyword, batches)
    grouped_results = []

    # Using ThreadPoolExecutor to manage a pool of threads
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Dictionary to keep track of futures and job postings
        future_to_company = {
            executor.submit(extract_company_info, job_posting): job_posting for job_posting in all_job_posting_ids
        }
        future_to_employee = {
            executor.submit(hiring_person_or_not, job_posting, employee_threshold, under_threshold_keywords, 
                            over_threshold_keywords, max_people_per_company): job_posting for job_posting in all_job_posting_ids
        }

    results = {job_posting: [None, None] for job_posting in all_job_posting_ids}  # Pre-initialize results dict with placeholders

    #Iterating over completed tasks as they complete
    for future in as_completed(future_to_company | future_to_employee):
        if future:
            job_posting = future_to_company.get(future) or future_to_employee.get(future)
            try:
                data = future.result()
                if future in future_to_company:
                    results[job_posting][0] = data
                else:
                    results[job_posting][1] = data
            except Exception as e:
                print(f"Job posting {job_posting} generated an exception: {e}")
        else:
            print(f"Job posting {job_posting} returned None")
            continue

    # Organizing the results
    for job_posting, data_pair in results.items():
        if None not in data_pair:  # Ensure both company and employee info are present
            grouped_results.append((job_posting, tuple(data_pair)))
    
    return grouped_results

def turn_grouped_results_into_df(grouped_results):
    results = {'Hiring Team':[], 'Förnamn':[], 'Efternamn':[], 'Bio':[], 'LinkedIn URL':[], 'Jobbtitel som sökes':[], 'Jobbannons-URL':[], 'Företag':[], 'Antal anställda':[], 'Företagsindustri':[], 'Företags-URL':[]}

    for result in grouped_results:
        job_posting_id = result[0]
        if isinstance(result[1][1], list): # Employee data will always be a list
            company_data, employee_data = result[1]
        else:
            employee_data, company_data = result[1]

        job_title, company_name, employee_count, company_url, company_industry, company_id = company_data

        for person in employee_data:
            hiring_team, full_name, bio, linkedin_url = person
        
            results['Hiring Team'].append(hiring_team)

            if full_name:
                first_name, last_name = split_and_clean_full_name(full_name)
                results['Förnamn'].append(first_name)
                results['Efternamn'].append(last_name)
            else:
                results['Efternamn'].append(None)
                if employee_count:
                    company_keywords = under_threshold_keywords if employee_count <= employee_threshold else over_threshold_keywords
                    url_formatted_keywords = company_keywords.strip().replace(', ', '%20OR%20').replace(' ', '%20')
                    construced_url = f"{company_url}/people/?keywords={url_formatted_keywords}"
                    results['Förnamn'].append(construced_url)
                else:
                    results['Förnamn'].append(None)
            
            results['Bio'].append(bio)
            results['LinkedIn URL'].append(linkedin_url)
            results['Jobbtitel som sökes'].append(job_title)
            results['Jobbannons-URL'].append(f"https://www.linkedin.com/jobs/search/?currentJobId={job_posting_id}&geoId=105117694&keywords={keyword}&location=Sweden")
            results['Företag'].append(company_name)
            results['Antal anställda'].append(employee_count)
            results['Företagsindustri'].append(company_industry)
            results['Företags-URL'].append(company_url)

    linkedin_jobs_df = pd.DataFrame.from_dict(results)
    return linkedin_jobs_df

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

def convert_seconds_to_minutes_and_seconds(seconds):
    min, sec = divmod(seconds, 60)
    return '%02d:%02d' % (min, sec)

## STREAMLIT CODE
st.title('LinkedIn Job search URL to CSV/xlsx Generator')
explanatory_note = """
The input is a URL where you have searched for a job title on LinkedIn Jobs, e.g. UX Designer / Data Engineer etc. etc. 
For every job ad available (or up to a limit), if there is a person from the Hiring Team available, that person's 
first name, last name, bio and LinkedIn URL will be scraped. If not, the program will go to the company that the ad is
linked to and search for a keyword of your choice based on employee count and scrape up to n people from there. Please 
contact me if you run into any bugs or errors at steven.lennartsson@gmail.com or on LinkedIn @stevenlomon :) 🛠️
"""
st.markdown(explanatory_note)
st.markdown(f'Sample URL: https://www.linkedin.com/jobs/search/?currentJobId=3874201225&keywords=ux%20designer&origin=SWITCH_SEARCH_VERTICAL')

# User input for LinkedIn URL
linkedin_job_url = st.text_input('Enter URL from the LinkedIn Job search:', '')
result_name = st.text_input('Enter a name for the resulting csv/Excel file:', '')
max_results_to_check = st.text_input('Enter maximum amounts of jobs to check (leave blank to scrape all available jobs for the query):', '')
st.write("If there is no Hiring Team available and the company has less than or equal to")
employee_threshold = st.number_input("Employee Threshold", min_value=1, value=100, step=1, format="%d", label_visibility="collapsed")
under_threshold_keywords = st.text_input('employees, search the company for (separate keywords with comma):', '')
over_threshold_keywords = st.text_input('If it has more, search the company for: (separate keywords with comma)', '')
max_people_per_company = st.text_input('Max amount of people to scrape per company if no Hiring Team:', '')

# Radio button to choose the file format
file_format = st.radio("Choose the file format for download:", ('csv', 'xlsx'))

# Button to the result file
if st.button('Generate File'):
    with st.spinner('Generating file, hold on'):
        if linkedin_job_url:
            keyword_search = re.search(r'keywords=([^&]+)', linkedin_job_url)
            keyword = keyword_search.group(1) if keyword_search else None

            start_time = time.time()
            total_number_of_results = get_total_number_of_results(keyword)
            if total_number_of_results is None:
                st.error("Could not fetch total amount of ads. Try again in a bit")

            if len(max_results_to_check) != 0 and int(max_results_to_check) < total_number_of_results:
                total_number_of_results = int(max_results_to_check)
            print(f"Attempting to scrape info from {total_number_of_results} job ads")
            st.markdown(f"Attempting to scrape info from {total_number_of_results} job ads. It takes approximately 3 seconds per job ad, meaning this will take around {convert_seconds_to_minutes_and_seconds(total_number_of_results*3)} minutes but potentially faster")

            batches = split_total_into_batches_of_100(total_number_of_results)
            print(f"Splitting {total_number_of_results} in batches: {batches}")

            results = main(keyword, batches, employee_threshold, under_threshold_keywords, over_threshold_keywords, int(max_people_per_company))
            end_time = time.time()

            print("Done!")
            st.text(f"Done! Scraped info from {total_number_of_results} ads in {convert_seconds_to_minutes_and_seconds(end_time - start_time)} minutes")
            scraped_data_df = turn_grouped_results_into_df(results)
            # st.text(f"Total job posting ids found in the request: {total_number_of_results}\nTotal fetched succesfully: {total_fetched}\nTotal unique ids: {total_unique}\nTotal with hiring team available: {total_hiring_team}")

            if file_format == 'csv':
                csv_file = generate_csv(scraped_data_df, result_name)
                with open(csv_file, "rb") as file:
                    st.download_button(label="Download CSV", data=file, file_name=csv_file, mime='text/csv')
                st.success(f'CSV file generated: {csv_file}')
            elif file_format == 'xlsx':
                excel_file = generate_excel(scraped_data_df, result_name)
                st.download_button(label="Download Excel", data=excel_file, file_name=f"{result_name}.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                st.success(f'Excel file generated: {result_name}.xlsx')
        else:
            st.error('Please enter a valid LinkedIn URL.')