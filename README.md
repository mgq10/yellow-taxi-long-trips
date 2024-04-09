# A Simple Data Pipeline with NYC Yellow Taxi Trip Data

## Purpose

The purpose of this Python code is to quickly show a basic data pipeline that downloads parquet files from the [Taxi & Limousine Commission (TLC)](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), filters them based on a specific criterion, and delivers the results in parquet files. 

You may be familiar with the Yellow Taxi Trip Data, as it is a popular public dataset that is relatively clean and large enough to be a good candidate for dev purposes. Until May 2022 the data was provided in csv format; they were converted to Apache Parquet files for more efficient processing. 

So, perhaps you can also use this as a guide for updating legacy code that processed the old csv files.

## Approach

A common scenario in Data Engineering is providing ad-hoc reports/datasets for business analytics or other data consumers.  

Here is a specific request the code tries to deliver:

***Provide all the trips over 0.9 percentile in distance traveled for any of the parquet files found in the TLC website.***

[TLC Yellow Taxi Data Dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)

Although one could interpret this in a couple of ways, we are going to assume "any of the parquet files found" to imply processing **all** of the files.  If just one file satisfies, then that can be done as well by limiting the number of files to download.

---

The code is set up to do without the use of third party services, like AWS s3 object storage, compute resources or a datawarehouse, to focus on the handling of parquet files and getting familiar with the dataset. 

Parquet files can be large, especially for trip data covering a big city like NYC. The full dataset is estimated to be over 260 GB, wich will usually exceed what one can handle on an average local machine.  For this reason, the code is flexible in that you can choose how many files to handle at one time.

***So, it is up to you to determine how much data to download depending on your resources.***

You can control this by including/excluding URLs from the downloads list. (see Key Files section below for details).

The code is primarily designed for handling large dataframes  by using the  Dask library instead of Pandas (although it is built on top of Pandas). It is a library that uses parallel computing to handle processing more efficiently.
If you're interested in the details check out their [docs](https://docs.dask.org/en/latest/install.html).

---

There is definitely room for improvement (adding error handling, basic reformating for readability and such, and adding a housekeeping script just to start).

But it is pretty short, so hopefully it's not too painful to get the logic.


## Summary of Pipeline

### Flow

1. **Setup:**
   - Imports necessary libraries: `dask`, `urllib`, `os` , `time`
   - Creates two directories, `Results` and  `Data`, if they don't already exist.

2. **Data Download:**
   - Reads a list of URLs from a file named `selected_data_urls.txt`.
   - Downloads each file into the `Data` directory.

3. **Data Processing:**
   - Reads all Parquet files in the `Data` directory into a Dask DataFrame.
   - Calculates the 0.9 percentile value for the `Trip_Distance` column.
   - Filters the DataFrame to retain only trips with distances exceeding the percentile value- what we'll call long trips.

4. **Results Generation:**
   - Saves the filtered DataFrame as multiple Parquet files with names starting with  `LongTrips-` within the `Results` directory.

### Key Files

- `selected_data_urls.txt` : 
    * Contains a list of URLs pointing to the Parquet files to be downloaded.
    * Update this list to your needs.

- `all_data_urls.txt` : 
    * Contains a **complete list** (as of April 2024) of URLs pointing to the Parquet files from the source site.
    * This file is not used by the code. It is there for you to choose which files to include in the file mentioned above.

- `LongTrips-n.parquet:` The generated Parquet files containing long trips (for `n` an integer beginning with 0).

### Dependencies

- This installs dependencies: `dask`
- `os` , `time` and `urllib.request` libraries (built-in)

### Usage

Ensure you have Dask installed:

``` 
python -m pip install "dask[complete]"
```

[Other Dask installations](https://docs.dask.org/en/latest/install.html)

Update the `selected_data_urls.txt` to have the necessary list of URLs.

Run `generate_files.py` script.

The downloaded files will be in the `Data` directory, and the filtered results with Long Trips data will be in the `Results` directory.

---
