"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Adam Simunek
email: adam.simunek@seznam.cz
discord: adamsim2
"""


import csv
import sys

import bs4
import requests
from bs4 import BeautifulSoup

#globals
url_part = "https://volby.cz/pls/ps2017nss/"


def process_response_from_server(url: str) -> BeautifulSoup:
    """
    Process the response from a server and parse it into a BeautifulSoup object.
    """
    response = requests.get(url)
    
    return BeautifulSoup(response.text, "html.parser")


def find_municipalities(soup: BeautifulSoup) -> list:
    """
    Find municipality information from parsed HTML content.

    This function takes a BeautifulSoup object representing parsed HTML content
    and extracts information about municipalities. It finds the relevant table
    rows and returns them as a list.
    """
    all_table = soup.find("div", {"id": "inner"})
    muni_tr = all_table.find_all("tr")[2:-2]
    
    return muni_tr


def process_tr_tag(tr_tag: BeautifulSoup) -> dict:
    """
    Process <tr> tag representing municipality information.

    This function takes a BeautifulSoup Tag object representing a table row (<tr> tag)
    containing information about a municipality. It extracts relevant data such as code,
    location, and URL for further data retrieval.
    """
    tr_text = tr_tag.get_text(separator="").splitlines()
    a_tags = tr_tag.find_all("a")
    href_value = list([a.get('href') for a in a_tags])
    url_muni_data = str()
    for value in href_value:
        url_muni_data = url_part + value #last URL will be used
    
    return {
                "code": tr_text[1],
                "location": tr_text[2],
                "url_muni_data": url_muni_data
        }


def clean_muni_dict(list_with_muni: list) -> dict:
    """
    Clean a list of municipalities' information.

    This function takes a list of dictionaries containing municipality information
    and filters out invalid entries based on the assumption that the first value
    of each dictionary corresponds to the municipality code. Only dictionaries with
    numeric codes are retained in the cleaned dictionary.
    """
    cleaned_dict = dict()
    for item in list_with_muni:
        values = list(item.values())
        if (values[0]).isnumeric():
            cleaned_dict[(values[0])] = item
   
    return cleaned_dict


def select_muni_with_districts(url: str) -> str:
    """
    Check if the URL corresponds to a municipality with districts.

    This function takes a URL string and checks if it contains a specific query parameter
    indicating that the municipality has districts.
    """
    if "&xvyber" in url:
        result = False
    else:
        result = True
   
    return result


def find_districts_and_their_url(muni_dict: dict) -> dict:
    """
    Find districts and their URLs for municipalities with districts.

    This function takes a dictionary containing information about municipalities
    and their URLs. It checks each URL to determine if the municipality has districts.
    For municipalities with districts, it finds the URLs for each district and updates
    the dictionary with these URLs.
    """
    for item in muni_dict:
        url = muni_dict[item]['url_muni_data']
        if select_muni_with_districts(url) == True:
            soup = process_response_from_server(url)
            table = soup.find("table", {"class": "table"})
            a_tags = table.find_all("a")
            href_value = [a.get('href') for a in a_tags]
            district_url = list()
            for value in href_value:
                district_url.append(url_part + value)
            muni_dict[item]['url_muni_data'] = district_url
 
    return muni_dict


def find_tables_with_stats(url: str) -> list:
    """
    Extract statistics from a table on a web page.

    This function takes a URL of a webpage containing statistical data in a table format.
    It fetches the data from the table and returns it as a list of strings.
    """
    soup = process_response_from_server(url)
    table = soup.find("table", {"class": "table"})
    td_tags = table.find_all("td")
    stats = [td.get_text(separator="") for td in td_tags]
    stats_cleaned = list()
    for item in stats:
        stats_cleaned.append(item.replace('\xa0', ''))
    
    return stats_cleaned


def extract_data_from_td(td_elements):
    """
    Extract text data from td elements and return it as a list.
    """
    return [td.get_text(separator="") for td in td_elements]


def find_tables_with_election_results(url: str) -> dict:
    """
    Fetch election results from the provided URL and extract parties and their respective results.
    """
    soup = process_response_from_server(url)
    all_result_tables = soup.find("div", {"id": "inner"})
    
    td_parties_1 = all_result_tables.find_all("td", {"headers": "t1sa1 t1sb2"})
    td_parties_2 = all_result_tables.find_all("td", {"headers": "t2sa1 t2sb2"})
    parties_list = extract_data_from_td(td_parties_1) + extract_data_from_td(td_parties_2)
    
    td_results_1 = all_result_tables.find_all("td", {"headers": "t1sa2 t1sb3"})
    td_results_2 = all_result_tables.find_all("td", {"headers": "t2sa2 t2sb3"})
    results_list = extract_data_from_td(td_results_1) + extract_data_from_td(td_results_2)
    
    return {"results": results_list, "parties": parties_list}


def process_vote_results(muni_dict_with_districts: dict) -> dict:
    """
    Process voting results for municipalities with districts.

    This function takes a dictionary containing information about municipalities
    with their respective districts and URLs to fetch voting statistics. It updates
    the dictionary with aggregated voting results.
    """
    for muni_dict in muni_dict_with_districts:
        muni_dict_with_districts[muni_dict]['registred'] = 0
        muni_dict_with_districts[muni_dict]['envelopes'] = 0
        muni_dict_with_districts[muni_dict]['valid'] = 0  
        url = muni_dict_with_districts[muni_dict]['url_muni_data'] 
        if type(url) is list:
            for str_url in url:
                stats_dist_cleaned = find_tables_with_stats(str_url)
                muni_dict_with_districts[muni_dict]['registred'] += int(stats_dist_cleaned[0])
                muni_dict_with_districts[muni_dict]['envelopes'] += int(stats_dist_cleaned[1])
                muni_dict_with_districts[muni_dict]['valid'] += int(stats_dist_cleaned[4])

                election_results_dist = find_tables_with_election_results(str_url)
                results_list_dist = election_results_dist['results']
                parties_list_dist = election_results_dist['parties']
                for i in range(0, len(parties_list_dist)-1):
                    if results_list_dist[i].isnumeric():
                        if parties_list_dist[i] in muni_dict_with_districts[muni_dict]:
                            muni_dict_with_districts[muni_dict][parties_list_dist[i]] += int(results_list_dist[i])
                        else:
                            muni_dict_with_districts[muni_dict][parties_list_dist[i]] = int(results_list_dist[i])
                    else:
                        muni_dict_with_districts[muni_dict][parties_list_dist[i]] = 'INVALID DATA'   
        else:
            stats_muni_cleaned = find_tables_with_stats(url)
            muni_dict_with_districts[muni_dict]['registred'] += int(stats_muni_cleaned[3])
            muni_dict_with_districts[muni_dict]['envelopes'] += int(stats_muni_cleaned[4])
            muni_dict_with_districts[muni_dict]['valid'] += int(stats_muni_cleaned[7])

            election_results_muni = find_tables_with_election_results(str(url))
            results_list_muni = election_results_muni['results']
            parties_list_muni = election_results_muni['parties']
            for i in range(0, len(parties_list_muni)-1):
                if results_list_muni[i].isnumeric():
                    if parties_list_muni[i] in muni_dict_with_districts[muni_dict]:
                        muni_dict_with_districts[muni_dict][parties_list_muni[i]] += int(results_list_muni[i])
                    else:
                        muni_dict_with_districts[muni_dict][parties_list_muni[i]] = int(results_list_muni[i])
                else:
                    muni_dict_with_districts[muni_dict][parties_list_muni[i]] = 'INVALID DATA'      
    return muni_dict_with_districts


def prepare_for_csv_export(muni_dict: dict) -> list:
    """
    Prepare municipality data for export to CSV format.

    This function takes a dictionary containing information about municipalities
    and prepares it for export to CSV format. It removes the 'url_muni_data' key
    from each municipality dictionary and returns a list of dictionaries suitable
    for exporting to CSV.
    """
    list_of_muni_dicts = muni_dict.values()
    for item in list_of_muni_dicts:
        del item['url_muni_data']
    return list(list_of_muni_dicts)


def export_to_csv(new_csv: str, list_of_muni_dicts: list):
    """
    Export municipality data to a CSV file.

    This function takes a list of dictionaries containing municipality data and
    exports it to a CSV file specified by `new_csv`.
    """
    csv_head = list_of_muni_dicts[0].keys()
    with open(new_csv, mode="w", newline="") as csv_with_muni:
        writer = csv.DictWriter(csv_with_muni, fieldnames=csv_head)
        writer.writeheader()
        for muni_dict in list_of_muni_dicts:
            writer.writerow(muni_dict) 


def main():
    #users input
    url = sys.argv[1]
    csv_results = sys.argv[2]

    if (
        len(sys.argv) == 3 and 
        "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj" in str(sys.argv[1]) and 
        "xnumnuts" in str(sys.argv[1]) and 
        ".csv" == str((sys.argv[2])[-4:])
    ):
        print(10*"*" + "ELECTION SCRAPER" + 10*"*")
        print("DOWNLOADING DATA FROM URL: " + url)
        #download code and parsing it by BeautifulSoup
        soup = process_response_from_server(url)
        
        #find table with municipalities names and codes
        all_tr_tag = find_municipalities(soup)


        #process tr tags in table
        list_with_muni = list()
        for tr_tag in all_tr_tag:
            list_with_muni.append(process_tr_tag(tr_tag))
        

        #cleaned muni dict - leave just muni-code, muni-name, URL with results 
        cleaned_muni_dict = clean_muni_dict(list_with_muni)


        #separate municipalities with districts and municipalities without districts
        muni_dict_with_districts = find_districts_and_their_url(cleaned_muni_dict)


        #download and process data with results
        all_data_dict = process_vote_results(muni_dict_with_districts)

        #prepare data for csv export 
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


if __name__ == "__main__":
    main()
