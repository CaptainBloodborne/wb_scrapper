import concurrent.futures
import datetime
# import sys
import pandas as pd
from time import sleep, time

from parser import connect_to_base, get_driver, write_to_file
from concurrent.futures import ThreadPoolExecutor, wait


def run_process(search_request):
    # init browser
    browser = get_driver(headless=headless)

    conn = connect_to_base(browser, search_request)
    if conn:
        sleep(2)
        browser.quit()
        print(f"Found null response - {search_request}")
        return search_request
    else:
        print(f"{search_request} is OK")
        browser.quit()


if __name__ == "__main__":

    # headless mode?
    headless = True

    # set variables
    start_time = time()
    current_attempt = 1
    output_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = f"output_{output_timestamp}.csv"
    output_list = list()

    df = pd.read_csv("/home/artem/Documents/wildberries/csv_reports/WBX_Search._Битый_поиск_2022_04_10.csv", index_col=["text"])
    search_list = [text for text in df.index]

    # scrape and crawl
    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [
            executor.submit(run_process, text) for text in search_list[:10]
        ]
    wait(futures)

    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
        except Exception as error:
            print(f"Something went wrong: {error}")
        else:
            if result is not None:
                output_list.append(result)

    write_to_file(output_list, output_filename)
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"Elapsed run time: {elapsed_time} seconds")
