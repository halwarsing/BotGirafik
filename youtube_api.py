from requests import get
from bs4 import BeautifulSoup
import json

class Youtube:
    def __init__(self):
        self.version = "0.0.1"
        self.key = "AIzaSyCghM41BZAlte89ww3dF9LnGfoYOr8MMFs"

    def get_last_video(self,id_channel):
        soup = BeautifulSoup(self.get_channel_videos(id_channel),'lxml')
        return json.loads(str(soup.find("p")).split("<p>")[1].split("</p>")[0])["items"][0]['id']['videoId']

    def get_channel_videos(self,id_channel):
        return get("https://www.googleapis.com/youtube/v3/search?key="+self.key+"&order=date&channelId="+id_channel).content
