
import dask.dataframe as dd
import os
import urllib.request
import time


'''
Request:

Using NYC “Yellow Taxi” Trips Data, 
give me all the trips over 0.9 percentile in distance traveled 
for any of the parquet files you can find there.

(Give me all the trips that traveled farther than 90% of all trips in the set)

'''

# Create folders for the downloads and results
new_directories = ["./Results", "./Data"]

for path in new_directories:
    
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
      

url_file = "./selected_data_urls.txt"
download_dir = new_directories[1]

# Wait time between downloads (seconds)
wait_time = 1

with open(url_file, "r") as url_file:

  for url in url_file:
      
    # Remove trailing newline characters
    url = url.strip()
    filename = url.split("/")[-1]
    download_path = os.path.join(download_dir, filename)

    # Request the data
    urllib.request.urlretrieve(url, download_path)
    
    # Wait for the specified time
    time.sleep(wait_time)

print("Files downloaded to Data folder.")



# Read the data into dataframe
df = dd.read_parquet('./Data/*.parquet')

# Calculate the 0.9 percentile for the chosen column
percentile_value = df['Trip_Distance'].quantile(0.9)

# percentile_value.compute()

# Filter the DataFrame for trips exceeding the percentile
long_trips_df = df[df['Trip_Distance'] > percentile_value]


# #Exploratory 

# long_trips_df.head()
# dd.compute(long_trips_df['Trip_Distance'].min(), long_trips_df['Trip_Distance'].max())
# distance_counts = long_trips_df.groupby('Trip_Distance')['Trip_Distance'].count()
# distance_counts.compute()
# long_trips_df.size.compute()
# df.size.compute()


# Create results files for delivery
name = lambda x: f"LongTrips-{x}.parquet"
long_trips_df.to_parquet("./Results", name_function=name)

# long_trips_df.to_csv("./Results")

print("Process complete. Files with results saved in Results folder.")