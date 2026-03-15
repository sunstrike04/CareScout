import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic

loc = Nominatim(user_agent="Geopy Library", timeout=10)
geocode = RateLimiter(loc.geocode, min_delay_seconds=1)

hospital_user_distance_dict = {}

illinois_hospitals_df = pd.read_pickle("hospital_insurances_accepted_with_hospitalids.pkl")

def rank_hospital_distances(user_address):
    user_coordinates = None
    getUserLoc = geocode(user_address)

    if getUserLoc:
        user_coordinates = (getUserLoc.latitude, getUserLoc.longitude)
    else:
        return []  # no results

    hospital_user_distance_dict.clear()

    for _, row in illinois_hospitals_df.iterrows():
       # print(_, row)
        hospital_id = row['hospital_id']
        hospital_address = row['Hospital Address']

        getHospitalLoc = geocode(hospital_address)

        if getHospitalLoc:
            hospital_coordinates = (getHospitalLoc.latitude, getHospitalLoc.longitude)
            dist_miles = geodesic(user_coordinates, hospital_coordinates).miles
            hospital_user_distance_dict[hospital_id] = dist_miles

    sorted_distances = sorted(hospital_user_distance_dict.items(), key=lambda item: item[1])
    return sorted_distances


def filter_by_insurance(user_insurance, sorted_distances, top_n=5):
    found_hospitals_with_insurance = True
    hospital_user_distance_dict_sorted = dict(sorted_distances)
    filtered_by_insurance = []

    for hospital_id, distance in hospital_user_distance_dict_sorted.items():
        row = illinois_hospitals_df[illinois_hospitals_df['hospital_id'] == hospital_id].iloc[0]
       
        insurances = row.get('Insurances Accepted', "")
        if user_insurance.lower() in [i.lower() for i in insurances]:
            hospital_name = row['Hospital Name']
            address = row['Hospital Address']
            filtered_by_insurance.append((hospital_name, address, distance))

    if len(filtered_by_insurance) == 0:
        found_hospitals_with_insurance = False
        nearest = []
        for hospital_id, distance in list(hospital_user_distance_dict_sorted.items())[:top_n]:
            row = illinois_hospitals_df[illinois_hospitals_df['hospital_id'] == hospital_id].iloc[0]
            nearest.append((row['Hospital Name'], row['Hospital Address'], distance))
        return nearest, found_hospitals_with_insurance
    else:
        return filtered_by_insurance[:top_n], found_hospitals_with_insurance


if __name__ == "__main__":
    user_address = input("Enter your Illinois address: ")
    sorted_distances = rank_hospital_distances(user_address)

    user_insurance = input("Enter your insurance name: ")
    results = filter_by_insurance(user_insurance, sorted_distances)

    print(results)