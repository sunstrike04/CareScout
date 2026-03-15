import pymysql
import pandas as pd
#one person connects to the database, and then saves the table as a python dataframe, which is then used in other locations 
def mysqlconnect():
    # To connect MySQL database
    conn = pymysql.connect(
        host='localhost',
        user='newuser3', 
        password = "carescout123",
        db='illinois_hospital_data',
        )
    
    cur = conn.cursor()
    
    # Select query
    cur.execute("SELECT * FROM illinois_hospital_full_pivot;")
    output = cur.fetchall()

    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(output, columns=columns)
    print(df.head())
    df.to_pickle("illinois_hospital_full.pkl")

    
    # for i in output:
    #     print(i)
    
    # To close the connection
    conn.close()

# Driver Code
if __name__ == "__main__" :
    mysqlconnect()
#Algorithm code


# Steps 1
# A: Filter based on location - nearest to furthest from the user's latitude/longitude --> keep all of them 

# B: Filter based on insurance accepted
    # if this returns an empty subset (no hospitals cover user's insurance)
        # Return top 5 from A 
    # else: return top 5 (or as many as we have if less than 5) from B
