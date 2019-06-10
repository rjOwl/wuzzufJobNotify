import requests
from bs4 import BeautifulSoup
import webbrowser
from sys import modules
try:
    import winsound
    from win10toast import ToastNotifier
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
except Exception as e:
    print(e)

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
BASE="https://wuzzuf.net/search/jobs?q={}"
STATUS_CODE_ERROR=-1
INTERNET_ERROR = -2

class wuzzuf(requests):
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
        for i in range (len(all_times)):
            time_difference = datetime.now() - all_times[i]#datetime.strptime((eachTime),   "%Y-%m-%d %H:%M:%S")
            elapsed_time_in_minutes = divmod(time_difference.days * 86400 + time_difference.seconds, 60)[0]
            if elapsed_time_in_minutes  <= jobMaxTime:
                newJobs.append(all_links[i])
        return newJobs


    def jobNotify(jobLink):
        if 'winsound' in modules and 'win10toast' in modules:
            toaster = ToastNotifier()
            toaster.show_toast("New Job Found!", jobLink)
            winsound.Beep(frequency, duration)
            webbrowser.open(jobLink)



