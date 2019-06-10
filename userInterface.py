from __future__ import print_function
from datetime import datetime, date
from time import sleep
import os
import wuzzufCrawler

if __name__=="__main__":
    print("#"*100+"""
App will work to get you the most new jobs based on your keywords.
But, don't leave it all to the app. 
Scroll and look for jobs yourself, you might end up finding a "NOT NEW" good job opportunity\n"""+"#"*100+"\n")
    print("link:", AUTAMENDY_URL)
    while True:
        keyword = input("Your keyword: ")
        wuz = wuzzufCrawler()
        jobs = wuz.getJobs(keyword)
        if wuz.STATUS_CODE_ERROR != jobs or wuz.INTERNET_ERROR != jobs:
            newJobs = wuz.filter(30, jobs)
            if len(newJobs) >0:
                for i in newJobs:
                    wuz.jobNotify(i)
            else:
                print("No new jobs found!")
        else:
            print(jobs)
