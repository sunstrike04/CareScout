# from geopy.geocoders import Nominatim
# from geopy.distance import distance

import pandas as pd

df = pd.read_pickle("/Users/niharika0425/Desktop/CareScout/hospital_insurances_accepted.pkl")

print(df)

print(len(df))
print(df.columns)

# # Increase timeout and set user_agent
# geolocator = Nominatim(user_agent="geo_test", timeout=10)  # 10 seconds timeout

# addr1 = "701 N First St, Springfield, IL 62781"
# addr2 = "701 N 1st St, Springfield, IL 62781"

# loc1 = geolocator.geocode(addr1)
# loc2 = geolocator.geocode(addr2)

# print("Address 1:", loc1.address if loc1 else "Not found")
# print("Coordinates 1:", (loc1.latitude, loc1.longitude) if loc1 else "N/A")

# print("Address 2:", loc2.address if loc2 else "Not found")
# print("Coordinates 2:", (loc2.latitude, loc2.longitude) if loc2 else "N/A")

# if loc1 and loc2:
#     dist = distance((loc1.latitude, loc1.longitude), (loc2.latitude, loc2.longitude)).meters
#     print(f"Distance between addresses: {dist:.2f} meters")



# \begin{table}[h]
# \centering
# \begin{tabular}{|l|l|}
# \hline
# \textbf{Location} & \textbf{Insurance Provider} \\ \hline
# 2020 Olive Hill Dr, Buffalo Grove, IL 60089 & Aetna \\ \hline
# Highland Park, IL & Cigna \\ \hline
# 1600 Sherman Ave, Evanston, IL, 60201 & Medicare \\ \hline
# Peoria, IL & Ambetter \\ \hline
# 3802 Sugar Loaf Dr, Springfield, IL & Molina Healthcare \\ \hline
# Chicago, IL & Oscar Health \\ \hline
# 320. W. Jackson Ave. Naperville, IL 60540 & Anthem \\ \hline
# Hinsdale, IL & Kaiser Permanente \\ \hline
# Barrington, IL & Medicaid \\ \hline
# 101 Pine St, St. Charles, IL & Humana \\ \hline
# \end{tabular}
# \caption{List of locations (addresses and cities) and their associated insurance providers}
# \label{tab:insurance_addresses}
# \end{table}
