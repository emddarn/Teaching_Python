
import os
import json
import requests
from dotenv import load_dotenv
import shutil


def youtube_util():
    """
    1. download youtube playlist
    2. get playlist information from googleapi
    3. get file details from the download folder
    4. create folder using the same name as playlist
    5. move files to the new playlist folder
    6. rename files with playlist item order
    """
    download_dir = "C:\\Users\\mdari\\Downloads\\python_learning_download"
    playlist_id = 'PL-osiE80TeTuRUfjRe54Eea17-YfnOOAx'
    playlistitems_file_info = "C:\\source\\001_learning\\resource\\git_playlistItems.json"
    playlist_file_info = "C:\\source\\001_learning\\resource\\git_playlists.json"
    # folder_name = ''
    file_details = get_file_details(download_dir)
    # playlist_info = get_playlist_info_from_file(playlist_file_info, playlistitems_file_info)
    playlist_info = get_playlist_info_from_URL(playlist_id)
    move_files_to_folder(download_dir, file_details, playlist_info)
    



def dl_youtube():
    # msg=subprocess.run(['resource\\youtube-dl.exe', 'https://www.youtube.com/playlist?list=PL-osiE80TeTuRUfjRe54Eea17-YfnOOAx'],capture_output=True,text=True,shell=False)   
    pass



def get_playlist_info_from_URL(playlist_id):

    ret_playlist_info = {}

    ytd_playlist_api = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&maxResults=50"
    url_playlist_info = "{0}&id={1}&key={2}".format(ytd_playlist_api, playlist_id, os.getenv("YTD_API_KEY"))
    r = requests.get(url_playlist_info)
    # print(r.json())
    data = r.json()
    title = data['items'][0]['snippet']['title'].strip()
    ret_playlist_info["folder_name"] = title

    playlist_info = {}
    ytd_playlist_api = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50"
    url_playlist_info = "{0}&playlistId={1}&key={2}".format(ytd_playlist_api, playlist_id, os.getenv("YTD_API_KEY"))
    r = requests.get(url_playlist_info)
    data = r.json()
    for item in data['items']:
        title = item["snippet"]['title'].strip()
        video_id = item["snippet"]["resourceId"]["videoId"].strip()
        playlist_pos = item["snippet"]["position"]
        playlist_info[video_id] = {"title":title, "playlist_pos":playlist_pos}
        # print(playlist_info)
    
    ret_playlist_info["playlist_info"] = playlist_info
    
    # print(ret_playlist_info)
    return ret_playlist_info



def get_playlist_info_from_file(playlist_file_info, playlistitems_file_info):# get_playlist_info
    
    ret_playlist_info = {}

    with open(playlist_file_info, 'r', encoding="utf8") as f:
        data = json.load(f)
        title = data['items'][0]['snippet']['title'].strip()
        ret_playlist_info["folder_name"] = title
        # print(ret_playlist_info)

   
    playlist_info = {}
    with open(playlistitems_file_info, 'r', encoding="utf8") as f:
        data = json.load(f) # converts json file to python dictionary
        # print(len(data['items']))
        for item in data['items']:
            title = item["snippet"]['title'].strip()
            video_id = item["snippet"]["resourceId"]["videoId"].strip()
            playlist_pos = item["snippet"]["position"]
            playlist_info[video_id] = {"title":title, "playlist_pos":playlist_pos}

    # print(playlist_info)
    
    ret_playlist_info["playlist_info"] = playlist_info
    
    # print(ret_playlist_info)
    return ret_playlist_info



def get_file_details(download_dir): # passing by location
    print(os.getcwd())
    os.chdir(download_dir)
    file_details = dict()

    for f in os.listdir():
        f_titleId, f_ext = os.path.splitext(f)
        try:
            # ind_und = f_titleId[::-1].index('-')
            ind_und = 11
        except:
            print(f, 'will be skipped')
            continue
        ind_last_und = (len(f_titleId)-ind_und)
        f_title = f_titleId[:(ind_last_und-1)]
        f_id = f_titleId[ind_last_und:]
        file_details[f_id] = [f_title, f, f_ext]
        
    # print(file_details)
    return file_details





def move_files_to_folder(download_dir, file_details, playlist_info):
    # print(file_details.keys())
    # print(playlist_info.keys())
    
    folder_name = playlist_info['folder_name']
    playlist_info = playlist_info['playlist_info']

    dir = os.path.join(download_dir,folder_name)
    os.makedirs(dir)

    for key, value in playlist_info.items():
        # print(key, len(key))
        if key in file_details.keys():
            print(key, ' - key found in file_details')
            # build new_file_name
            f_name = value['title']
            playlist_pos = str(value['playlist_pos']+1).zfill(2)
            f_orig = file_details[key][1]
            f_ext = file_details[key][2]
            # dst = "C:\\Users\\mdari\\Downloads\\python_learning_download\\folder_name\\f_name.f_ext"
            # src = "C:\\Users\\mdari\\Downloads\\python_learning_download\\f_orig"
            # dst = "{}\\{}\\{}_{}{}".format(download_dir, folder_name, playlist_pos, f_name, f_ext)
            # src = "{}\\{}".format(download_dir, f_orig)
            dst_fname = "{}_{}{}".format(playlist_pos, f_name, f_ext)
            dst = os.path.join(download_dir, folder_name, dst_fname)
            src = os.path.join(download_dir, f_orig)
            try:
                new_dest = shutil.move(src, dst)
                print(new_dest, " - move complete.")
            except e:
                print('Exception occurred with: ', e)
        else:
            print(key, ' - key not found in file_details')

      



def renaming_files():
    pass


if __name__ == "__main__":
    load_dotenv()
    # print(os.getenv("MYSECRET"))
    youtube_util()
