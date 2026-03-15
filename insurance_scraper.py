import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re
import pandas as pd
from rapidfuzz import fuzz, process



def normalize(text):
    return re.sub(r'\s+', '', text).lower()

def scrape_hospital_insurances(hospital_url, hospital_name):
    result = find_insurance_page(hospital_url, hospital_name)
    return result

def has_insurance_content(soup):
    """Check if page contains actual insurance information"""
    text = soup.get_text().lower()
   
    insurance_companies = pd.read_csv("InsuranceList.csv", header = None)
    insurance_companies = list(insurance_companies[0])
    print(text)
    
    mentions = sum(1 for company in insurance_companies if company.lower() in text)
    print(f"Insurance mentions found: {mentions}")
    
    if mentions >= 3:
        return True
    
    insurance_phrases = [
        'insurance accepted', 'accepted insurance', 'insurance plans',
        'we accept', 'plans accepted', 'in-network', 'insurance providers'
    ]
    
    phrase_count = sum(1 for phrase in insurance_phrases if phrase in text)

    
    return phrase_count >= 2

def extract_insurance_info(soup):
    insurance_companies = pd.read_csv("InsuranceList.csv", header = None)
    insurance_companies = list(insurance_companies[0])

    insurance_phrases = [
        'insurance accepted', 'accepted insurance', 'insurance plans',
        'we accept', 'plans accepted', 'in-network', 'insurance providers'
    ]
    
    for i in range(len(insurance_companies)):
        insurance_companies[i] = insurance_companies[i].lower()
    found_insurances = []
    
    page_text = soup.get_text()

    lines = page_text.split('\n')
    for line in lines:
        if any(phrase in line.lower() for phrase in insurance_phrases):
            continue
        line = line.lower().strip()

        # we want to skip too short of lines
        if len(line) < 5:
            continue
        
        best_match = (None, 0, None)
        full_name = ""
        
        for word in line.split():
            if full_name:
                full_name += " " + word
            else:
                full_name = word
            
            result = process.extractOne(
                full_name,
                insurance_companies,
                scorer=fuzz.token_sort_ratio,
                score_cutoff=85
            )
            
            if result and result[1] > best_match[1]:
                best_match = result

        if best_match[0] and best_match[0] not in found_insurances:
            print("-----")
            print(best_match[0], line, best_match[1])
            found_insurances.append(best_match[0])
        
        if result:
            matched_insurance, score, index = result
            print("------")
            if matched_insurance not in found_insurances:
                print(matched_insurance, line)
                found_insurances.append(matched_insurance)
            print("------")
        

    print("insurance list found", found_insurances)
    print(len(found_insurances))


    
    return found_insurances

def find_insurance_page(hospital_url, hospital_name):
    """
    Try multiple strategies to find insurance information
    Returns: (insurance_url, insurance_data, method_used)
    """
    print(f"\n{'='*60}")
    print(f"Searching insurance info for: {hospital_name}")
    print(f"Base URL: {hospital_url}")
    
    result = try_url_patterns(hospital_url)
    if result:
        return result
    
    
    # result = search_homepage_links(hospital_url, hospital_name)
    # if result:
    #     return result
    
    
    
    print(f"No insurance info found for {hospital_name}")
    return None, None, "not_found"

def try_url_patterns(base_url):
    """Strategy 1: Try predictable URL patterns"""
    print("Strategy 1: Trying common URL patterns...")
    
    # ***OUR PATHS***
    patterns = [
        "/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans",
        "/patients-visitors/health-plans-accepted",
        "/billing-insurance-information/",
        "/patients-visitors/accepted-insurance/",
        "/patient-information/accepted-insurance-plans",
        "/patients-visitors/financial-services/billing-insurance",
        "/patients-visitors/billing-information/insurance",
        "/patients-visitors/billing-insurance/insurance/insurance-plans-accepted",
        "/resources/frequently-asked-questions",
        "/admissions/paying-for-treatment/",
        "/about-us/insurance-accepted",
        "/billing/insurance-accepted",
        "/billing-insurance-information",
        "/patient-information/insurance",
        "/patients/insurance-providers",
        "/patient-visitor-information/accepted-insurances",
        "/medical-group/patient-resources/hshs-insurance-plans",
        "/patients-and-visitors/accepted-health-plans",
        "/patients_and_visitors/accepted-insurance/",
        "/admissions/paying-for-treatment/",
        "/getpage.php?name=insurance",
        "/patients-visitors/medicare",
        "/accepted-insurance-plans/",
        "/contact/insurance",
        "/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/northwestern-memorial-hospital", 
        "/en/patients-visitors/billing-financial-assistance/insurance/commercial-plans-we-accept/"
    ]
    
    for pattern in patterns:
        test_url = urljoin(base_url, pattern)
        print(f"Test URL: {test_url}")
        try:
            response = requests.get(test_url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                print("Page found, checking content...")
                soup = BeautifulSoup(response.text, 'html.parser')
        
                if has_insurance_content(soup):
                    print(f"Found via URL pattern: {pattern}")
                    insurance_data = extract_insurance_info(soup)
                    return test_url, insurance_data, "url_pattern"
        except:
            continue
        
        time.sleep(0.5)  
    
    print("  No matches in URL patterns")
    return None

# def search_homepage_links(base_url, hospital_name):
#     """Strategy 2: Parse homepage and find insurance-related links"""
#     print("Strategy 2: Searching homepage links...")
    
#     try:
#         response = requests.get(base_url, timeout=10)
#         soup = BeautifulSoup(response.text, 'html.parser')
#     except Exception as e:
#         print(f"Could not fetch homepage: {e}")
#         return None
    
#     insurance_keywords = [
#         'insurance', 'billing', 'payment', 'financial', 
#         'accepted plans', 'pay bill', 'patient financial',
#         'managed care', 'health plans', 'patients', 'patient'
#     ]
    
#     potential_links = []
    
#     for link in soup.find_all('a', href=True):
#         link_text = link.get_text().lower().strip()
#         link_url = link['href'].lower()
        
#         score = 0
#         for keyword in insurance_keywords:
#             if keyword in link_text:
#                 score += 10
#             if keyword in link_url:
#                 score += 5
        
#         if score > 0:
#             full_url = urljoin(base_url, link['href'])
#             potential_links.append((score, full_url, link_text))
    
#     potential_links.sort(reverse=True, key=lambda x: x[0])
    
#     print(f"  Found {len(potential_links)} potential insurance links")
    
#     for score, url, text in potential_links[:5]:  # Try top 5
#         print(f"  Trying: {text[:50]}... (score: {score})")
#         try:
#             response = requests.get(url, timeout=10)
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             if has_insurance_content(soup):
#                 print(f"✓ Found via homepage link: {text[:50]}")
#                 insurance_data = extract_insurance_info(soup)
#                 return url, insurance_data, "homepage_link"
#         except:
#             continue
        
#         time.sleep(0.5)
    
#     print("  No valid insurance pages found in links")
#     return None

