import datetime
from time import sleep
import requests
import urllib
import os
import json
import urllib.request

try:
    import tkinter
except ImportError:
    import Tkinter as tkinter

__version__ = "v.0.2.7"

window = tkinter.Tk()


def download(username):
    request_url = "https://www.instagram.com/" + username + "?__a=1"
    updated_request_url = "https://instagram.com/graphql/query/?query_id=17888483320059182"
    more_available = True
    end_cursors = []
    user_id = None
    baseurlbool = True

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
    }

    make_folder(entry.get())  # makes folder with given username

    while more_available:
        if not end_cursors:
            print(request_url)
            response = requests.get(request_url, headers=headers)

        else:
            print(updated_request_url + "&id={}".format(user_id) + "&first=12&after={}".format(end_cursors[-1]))
            # https://instagram.com/graphql/query/?query_id=17888483320059182&id=6765242919&first=12&after={max_id/end_cursor}
            response = requests.get(
                (updated_request_url + "&id={}".format(user_id) + "&first=12&after={}".format(end_cursors[-1])),
                headers=headers)

        try:
            # data = response.json()
            json_data = json.loads(response.text)
        except:
            print("\033[91mInvalid username!\033[0m")
            os.removedirs(entry.get())
            break;

        print(json_data.keys())
        # for node in json_data["user"]["media"]["nodes"]:
        if baseurlbool:
            nodes = json_data['graphql']['user']['edge_owner_to_timeline_media']['edges']
        else:
            nodes = json_data['data']['user']['edge_owner_to_timeline_media']['edges']

        for node in nodes:

            # Cant access video url anymore
            # if src["is_video"] and do_download_videos.get() == 1:
            #   file_url = src["videos"]["standard_resolution"]["url"]
            # else:

            file_url = node['node']['display_url']
            # file_url = file_url.replace("s640x640", "s1080x1080")
            
            timestamp = node['node']['taken_at_timestamp']
            date_from_timestamp = datetime.datetime.fromtimestamp(timestamp).isoformat()
            file_name = date_from_timestamp.replace(':', '_').replace('-', '_') + '.jpg'

            path = entry.get() + "/" + username + "_" + file_name

            if not os.path.isfile(path):

                try:
                    urllib.request.urlretrieve(file_url, path)
                    print("Downloaded: " + path)
                    sleep(0.5)

                except:
                    try:
                        urllib.urlretrieve(file_url, path)
                        print("Downloaded: " + path)
                        sleep(0.5)

                    except:
                        print("\033[91m----Skipping this image----\033[0m")

        # more_available = json_data["user"]["media"]["page_info"]["has_next_page"]
        if baseurlbool:
            more_available = json_data["graphql"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
            user_id = json_data["graphql"]["user"]["id"]
            end_cursor = json_data["graphql"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
            baseurlbool = False

        else:
            more_available = json_data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
            end_cursor = json_data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]

        end_cursors.append(end_cursor)

        if more_available:
            print("\033[92mGetting next page of images with end_cursor: " + end_cursor + "\033[0m")
        print("\033[92m--------------Completed--------------\033[0m")


def action():
    download(entry.get())


# Make folder with given username
def make_folder(username):
    try:
        os.makedirs(username)
    except OSError:
        os.system("rm -rf " + username)
        os.makedirs(username)


# Building the UI
window.configure(background="grey90")
window.title("insta-dl " + __version__)
window.geometry("300x200")
window.resizable(False, False)

entry = tkinter.Entry(window)
entry.place(x=70, y=68)
entry.configure(highlightbackground="grey90")

button = tkinter.Button(window, text="Download")
button.place(x=110, y=120)
button.configure(command=lambda: action(), highlightbackground="grey90")

notice = tkinter.Label(window, text="insta-dl is not affiliated with Instagram",
                       fg="grey60", bg="grey90")
notice.place(x=30, y=180)

window.mainloop()
