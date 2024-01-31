"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Adam Simunek
email: adam.simunek@seznam.cz
discord: adamsim2
"""

#https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

import csv
import sys
import bs4
import requests
from bs4 import BeautifulSoup


def process_response_from_server(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def find_municipalities(soup: BeautifulSoup) -> list:
    all_table = soup.find("div", {"id": "inner"})
    muni_tr = all_table.find_all("tr")[2:-2]
    return muni_tr

def process_tr_tag(tr_tag: BeautifulSoup) -> dict:
    tr_text = tr_tag.get_text(separator="").splitlines()
    a_tags = tr_tag.find_all("a")
    href_value = list([a.get('href') for a in a_tags])
    url_muni_data = str()
    for value in href_value:
        url_muni_data = "https://volby.cz/pls/ps2017nss/"+ value #last URL will be used
    muni_dict = {
                "code": tr_text[1], 
                "location": tr_text[2],
                "url_muni_data": url_muni_data
        }      
    return muni_dict

def clean_muni_dict(list_with_muni: list) -> dict:
    cleand_dict = dict()
    for item in list_with_muni:
        values = list(item.values())
        if (values[0]).isnumeric():
            cleand_dict[(values[0])] = item
    return cleand_dict

def find_districts_and_their_url(muni_dict: dict) -> dict:
    for dict in muni_dict:
        url = muni_dict[dict]['url_muni_data']
        if dict == url[-6:]:
            soup = process_response_from_server(url)
            table = soup.find("table", {"class": "table"})
            a_tags = table.find_all("a")
            href_value = [a.get('href') for a in a_tags]
            district_url = list()
            for value in href_value:
                district_url.append("https://volby.cz/pls/ps2017nss/"+ value)
            muni_dict[dict]['url_muni_data'] = district_url
    return muni_dict      

def process_vote_results(muni_dict_with_districts: dict) -> dict:
    for dict in muni_dict_with_districts:
        muni_dict_with_districts[dict]['registred'] = 0
        muni_dict_with_districts[dict]['envelopes'] = 0
        muni_dict_with_districts[dict]['valid'] = 0   
        url = muni_dict_with_districts[dict]['url_muni_data'] 
        if type(url) is list:
            for str_url in url:
                soup_dist = process_response_from_server(str_url)
                table_dist = soup_dist.find("table", {"class": "table"})
                td_tags_dist = table_dist.find_all("td")
                stats_dist = [td.get_text(separator="").replace('\xa0', '') for td in td_tags_dist]
                stats_dist_cleaned = list()
                for stats in stats_dist:
                    stats_dist_cleaned.append(stats.replace('\xa0', ''))
                muni_dict_with_districts[dict]['registred'] += int(stats_dist_cleaned[0])
                muni_dict_with_districts[dict]['envelopes'] += int(stats_dist_cleaned[1])
                muni_dict_with_districts[dict]['valid'] += int(stats_dist_cleaned[4])

                all_result_tables_dist = soup_dist.find("div", {"id": "inner"})

                td_parties_dist = all_result_tables_dist.find_all("td", {"headers": "t1sa1 t1sb2"}) + all_result_tables_dist.find_all("td", {"headers": "t2sa1 t2sb2"})
                parties_list_dist = [td.get_text(separator="") for td in td_parties_dist]
                td_results_dist = all_result_tables_dist.find_all("td", {"headers": "t1sa2 t1sb3"}) + all_result_tables_dist.find_all("td", {"headers": "t2sa2 t2sb3"})
                results_list_dist = [td.get_text(separator="") for td in td_results_dist]

                for i in range(0, len(parties_list_dist)-1):
                    if results_list_dist[i].isnumeric(): 
                        if parties_list_dist[i] in muni_dict_with_districts[dict]:
                            muni_dict_with_districts[dict][parties_list_dist[i]] += int(results_list_dist[i])
                        else: 
                            muni_dict_with_districts[dict][parties_list_dist[i]] = int(results_list_dist[i])
                    else:
                        muni_dict_with_districts[dict][parties_list_dist[i]] = 'INVALID DATA'

        else:
            soup_muni = process_response_from_server(url)
            table_muni = soup_muni.find("table", {"class": "table"})
            td_tags_muni = table_muni.find_all("td")
            stats_muni = [td.get_text(separator="") for td in td_tags_muni]
            stats_muni_cleaned = list()
            for stats in stats_muni:
                stats_muni_cleaned.append(stats.replace('\xa0', ''))               
            muni_dict_with_districts[dict]['registred'] += int(stats_muni_cleaned[3])
            muni_dict_with_districts[dict]['envelopes'] += int(stats_muni_cleaned[4])
            muni_dict_with_districts[dict]['valid'] += int(stats_muni_cleaned[7])

            
            all_result_tables_muni = soup_muni.find("div", {"id": "inner"})
            td_parties_muni = all_result_tables_muni.find_all("td", {"headers": "t1sa1 t1sb2"}) + all_result_tables_muni.find_all("td", {"headers": "t2sa1 t2sb2"})
            parties_list_muni = [td.get_text(separator="") for td in td_parties_muni]
            td_results_muni = all_result_tables_muni.find_all("td", {"headers": "t1sa2 t1sb3"}) + all_result_tables_muni.find_all("td", {"headers": "t2sa2 t2sb3"})
            results_list_muni = [td.get_text(separator="") for td in td_results_muni]

            for i in range(0, len(parties_list_muni)-1):
                if results_list_muni[i].isnumeric(): 
                    if parties_list_muni[i] in muni_dict_with_districts[dict]:
                        muni_dict_with_districts[dict][parties_list_muni[i]] += int(results_list_muni[i])
                    else:
                        muni_dict_with_districts[dict][parties_list_muni[i]] = int(results_list_muni[i])
                else:
                    muni_dict_with_districts[dict][parties_list_muni[i]] = 'INVALID DATA'      
    return muni_dict_with_districts

def prepare_for_csv_export(muni_dict: dict) -> list:
    list_of_muni_dicts = muni_dict.values()
    for item in list_of_muni_dicts:
        del item['url_muni_data']
    return list(list_of_muni_dicts)

def export_to_csv(new_csv: str, list_of_muni_dicts: list):
    csv_with_muni = open(new_csv, mode="w", newline="")
    csv_head = list_of_muni_dicts[0].keys()
    writer = csv.DictWriter(csv_with_muni, fieldnames=csv_head)
    writer.writeheader()
    for muni_dict in list_of_muni_dicts:
        writer.writerow(muni_dict)
    
    csv_with_muni.close()


def main():
    #users input
    url = sys.argv[1]
    csv_results = sys.argv[2]

    if len(sys.argv) == 3 and "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj" in str(sys.argv[1]) and "xnumnuts" in str(sys.argv[1]) and ".csv" == str((sys.argv[2])[-4:]):

        print(10*"*" + "ELECTION SCRAPER" + 10*"*")
        print("DOWNLOADING DATA FROM URL: " + url)
        #download code and parsing it by BeautifulSoup
        soup = process_response_from_server(url)
        
        #finds table with municipalities names and codes
        all_tr_tag = find_municipalities(soup)

        #processing tr tags in table
        list_with_muni = list()
        for tr_tag in all_tr_tag:
            list_with_muni.append(process_tr_tag(tr_tag))

        #cleaned muni dict - leaves just muni-code, muni-name, URL to page with results 
        cleaned_muni_dict = clean_muni_dict(list_with_muni)

        #separation to municipalities with districts and municipalities without districts
        muni_dict_with_districts = find_districts_and_their_url(cleaned_muni_dict)

        #download and processed data with results
        all_data_dict = process_vote_results(muni_dict_with_districts)
        
        #preparation data for csv export 
        data_csv_ready = prepare_for_csv_export(all_data_dict)
        print("SAVING DATA TO FILE: " + csv_results)
        
        #write data to csv and export csv
        export_to_csv(csv_results, data_csv_ready)  

        #success - data has been saved
        print("DATA SAVED")
        print(10*"*" + "ELECTION SCRAPER" + 10*"*")
    else:
        #invalid users input 
        print(10*"*" + "ELECTION SCRAPER" + 10*"*")
        print("!!! INVALID INPUT !!!")
        print(10*"*" + "ELECTION SCRAPER" + 10*"*")
        quit()

if __name__ == "__main__":
    main()
