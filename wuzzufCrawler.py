import requests
from bs4 import BeautifulSoup
import webbrowser
from datetime import datetime, date
from sys import modules
from CONSTANTS import *

try:
    import winsound
    from win10toast import ToastNotifier
except Exception as e:
    print(e)

class wuzzuf():
    def getJobs(self, keyword):
        url = BASE.format(keyword)
        try:
            res = requests.get(url, headers=HEADERS)
            if res.status_code != 200:
                return STATUS_CODE_ERROR
            return res.content
        except Exception as e:
            return INTERNET_ERROR+"\n"+e

    def filter(self, jobMaxTime, source):
        newJobs=[] 
        soup = BeautifulSoup(source, 'html.parser')
        current_time = datetime.now().strftime("%b %d %Y %I:%M%p")
        number_of_jobs = soup.find('p',{"class", "no-of-jobs"}).get_text().split("/")[0]
        pagePosts = soup.findAll('div', {'class': 'new-time'})
        all_links = [x.a['href'] for x in pagePosts]
        all_times = [datetime.strptime(("".join(x.find('time', {'class': 'time1 job-date'})['datetime'].replace("T", " ").split("+")[0])),   "%Y-%m-%d %H:%M:%S") for x in pagePosts]
        jobs_times_human_readable = [datetime.strftime(datetime.strptime(("".join(x.find('time', {'class': 'time1 job-date'})['datetime'].replace("T", " ").split("+")[0])),   "%Y-%m-%d %H:%M:%S"), "%b %d %Y %I:%M%p") for x in pagePosts]
        for i in range (len(all_times)):
            time_difference = datetime.now() - all_times[i]#datetime.strptime((eachTime),   "%Y-%m-%d %H:%M:%S")
            elapsed_time_in_minutes = divmod(time_difference.days * 86400 + time_difference.seconds, 60)[0]
            if elapsed_time_in_minutes  <= jobMaxTime:
                newJobs.append(all_links[i])
        return newJobs


    def jobNotify(self, jobLink):
        if 'winsound' in modules and 'win10toast' in modules:
            toaster = ToastNotifier()
            toaster.show_toast(title="WUZZUF bot\nNew Job Found!", msg=jobLink, duration=7, icon_path=r"logo-blue.ico", )
            winsound.Beep(FREQUENCY, DURATION)
            webbrowser.open(jobLink)



