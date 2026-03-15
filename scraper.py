import requests
from bs4 import BeautifulSoup 
import insurance_scraper
import pandas as pd


hospital_dictionary = {}
def scrapeTab(hospital_dictionary): 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"}

    SOURCE_URL = "https://www.team-iha.org/our-association/illinois-hospitals-and-health-systems-listing/"

    response = requests.get(SOURCE_URL, headers=headers)

    if response.status_code != 200: 
        print(f"Response status code = {response.status_code}")
    else: 
        print("Response status code = 200")

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    main_content = soup.find('div', class_='resp-tabs-container')
    if main_content: 
        print("Found resp-tabs-container")
    else:
        print("could not find resp-tabs-container")

    
    hospitals = []
    item_containers = main_content.find_all('div', class_='item-container')
    for container in item_containers:
        h4 = container.find('h4')
        if not h4:
            continue
        link = h4.find('a', href=True)
        if not link:
            continue
        hospital_name = link.get_text(strip=True)
        hospital_url = link['href']
       

        p_tag = container.find('p')
        if p_tag:
           
            address_lines = []
            for br in p_tag.find_all('br'):
                br.replace_with('\n')
            
            full_text = p_tag.get_text(separator=" ", strip=True)
           
            lines = [line.strip() for line in full_text.split("\n") if line.strip()]
            
            
            cleaned_lines = []
            for line in lines:
                if '(' in line:
                    line = line[:line.index('(')].strip()
                if line: 
                    cleaned_lines.append(line)
            lines = cleaned_lines

            address = " ".join(lines)
           # print(f"Hospital name: {hospital_name}, URL: {hospital_url}, Address: {address}")
            hospital_dictionary[hospital_name] = [hospital_url, address]
        else:
            address = ''
        
      
scrapeTab(hospital_dictionary)
hospital_insurance_list = []
hopsitals_with_no_insurance_found = []

for hospital_name in hospital_dictionary:    
    key = hospital_dictionary[hospital_name]
    hospital_url = key[0]
    hospital_address = key[1]
    print(f"Scraping insurances for {hospital_name} at {hospital_url}")
    result = insurance_scraper.scrape_hospital_insurances(hospital_url, hospital_name)
    insurances_accepted = result[1]
    if insurances_accepted is not None and len(insurances_accepted) > 0:        
        hospital_insurance_list.append([hospital_name, hospital_url, hospital_address, insurances_accepted])
    else:
        hopsitals_with_no_insurance_found.append(hospital_name)

hospital_insurance_dataframe = pd.DataFrame(hospital_insurance_list, columns = ["Hospital Name", "Hospital URL", "Hospital Address", "Insurances Accepted"])

# Convert the pandas dataframe to a pickle file:
hospital_insurance_dataframe.to_pickle("./hospital_insurances_accepted.pkl")  

# Write the list of hospitals we couldn't find insurance information for to a .txt file
hopsitals_with_no_insurance_found_file = "hopsitals_with_no_insurance_found.txt"
with open(hopsitals_with_no_insurance_found_file, 'w') as f:
    for item in hopsitals_with_no_insurance_found:
        f.write(f"{item}\n")
