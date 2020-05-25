# Created Dec, 2018

from time import sleep
from CONSTANTS import *
from wuzzufCrawler import  wuzzuf
from colorama import init, Fore, Back, Style
from datetime import datetime, date

if __name__=="__main__":

    init(autoreset=True)
    print(Fore.YELLOW +"#"*100+"""
App will work to get you the most new jobs based on your keywords.
But, don't leave it all to the app. 
Scroll and look for jobs yourself, you might end up finding a "NOT NEW" good job opportunity\n"""+"#"*100+"\n")
    keyword = input("Your keyword: ")
    print("Main page:", BASE.format(keyword))
    wuz = wuzzuf()
    while True:
        current_time = datetime.now().strftime("%b %d %Y %I:%M%p")
        print(Fore.BLUE+"Time now is: "+ current_time) #.strftime("%b %d %Y %I:%M%p"))
        jobs = wuz.getJobs(keyword)
        if STATUS_CODE_ERROR != jobs or INTERNET_ERROR != jobs:
            newJobs = wuz.filter(900, jobs)
            if len(newJobs) >0:
                print(Fore.GREEN+"Found New Job:")
                for i in newJobs:
                    print(i)
                    wuz.jobNotify(i)
            else:
                print(Fore.RED+"No new jobs found!\n")
        else:
            print(jobs)        
        timeToWaitInSeconds = MINUTES_TO_WAIT*60
        sleep(timeToWaitInSeconds)
