import subprocess
import time

import pyfiglet;
import pytube;
import os;
import requests;
from pydub import AudioSegment;
import os.path;
from pathlib import Path;
import eyed3;

def download(link, mod, outname, path):

    outname = outname.replace("\\", "").replace("/", "");

    if len(link.split("/@")) > 1:
        chnl_playlist = "";

        try:
            chnl_id = requests.get(link).text.split('header":{"c4TabbedHeaderRenderer":{"channelId":"UC')[1].split('",')[0];
            chnl_playlist = "https://www.youtube.com/playlist?list=UU" + chnl_id;

        except:
            print("", end="");

        if chnl_playlist != "":
            link = chnl_playlist;

    if len(link.split("playlist")) > 1 or len(link.split("list")) > 1:
        pll = pytube.Playlist(link);

        video_num = len(pll.video_urls);

        plname = requests.get(link).text.split("<meta property=\"og:title\" content=\"")[1].split("\">")[0];
        plname = plname.replace("\\", "").replace("/", "");

        tmp = "";
        for j in plname:
            if j != "&" and j != "." and j != "#" and j != "?" and j != ";" and j != "|" and j != ":" and j != "/" and j != "\\" and j != "\"" and j != "\'" and j != "*":
                tmp += j;
        plname = tmp;

        path += plname + "\\";

        try:
            os.mkdir(path);
        except:
            print(end="");

        for i in range(len(pll.video_urls)):
            if i > -1:
                ASCII_art_1 = pyfiglet.figlet_format(str(i+1) + "/" + str(video_num));
                print(ASCII_art_1);

                if outname != "":
                    new_name = outname + str(len(pll.video_urls) - i);
                else:
                    new_name = "";

                e = 0;

                if new_name == "":
                    new_name = requests.get(pll.video_urls[i]).text.split("""<meta name=\"title\" content=\"""")[1].split("""\">""")[0];
                    new_name = new_name.replace("\\", "").replace("/", "");

                    tmp = "";
                    for j in new_name:
                        if j != "&" and j != "." and j != "#" and j != "?" and j != ";" and j != "|" and j != ":" and j != "/" and j != "\\" and j != "\"" and j != "\'" and j != "*":
                            tmp += j;
                    new_name = tmp;

                if not os.path.exists(path + new_name + "\\done.txt"):
                    if mod == 0:
                        e = mp4(pll.video_urls[i], path, new_name, 1);

                    elif mod == 1:
                        e = only_mp3(pll.video_urls[i], path, new_name, requests.get(link).text.split("<meta property=\"og:title\" content=\"")[1].split("\">")[0], i);

                    elif mod == 2:
                        e = loadsubs(pll.video_urls[i], path, new_name, 1);
                else:
                    print("Loaded");

                if e != 0 and e != None:
                    print(e);
                    return e;
                elif mod != 1:
                    Path(path + new_name + "\\done.txt").touch();
                    #with open(path + new_name + "\\done.txt") as f: pass;

    else:
        e = 0;

        if outname == "":
            outname = requests.get(link).text.split("""<meta name=\"title\" content=\"""")[1].split("""\">""")[0];
            outname = outname.replace("\\", "").replace("/", "");
            tmp = "";
            for j in outname:
                if j != "&" and j != "." and j != "#" and j != "?" and j != ";" and j != "|" and j != ":" and j != "/" and j != "\\" and j != "\"" and j != "\'" and j != "*":
                    tmp += j;
            outname = tmp;

        if mod == 0:
            e = mp4(link, path, outname, 0);

        elif mod == 1:
            e = only_mp3(link, path, outname);

        elif mod == 2:
            e = loadsubs(link, path, outname, 0);

        if e != 0 and e != None:
            print(e);
            return e;

    return 0x0;


def mp4(url, path, outname, playlist):

    print("---\nStart loading\n---");

    try:
        os.mkdir(path + outname);
    except:
        print(end="");

    path += outname + "\\";

    subprocess.call("yt-dlp.exe --format webm/bestvideo/best --output \"" + path + outname + '.webm\" ' + url, stdin=True);
    subprocess.call("yt-dlp.exe --format m4a/bestaudio/best --output \"" + path + outname + '.m4a\" ' + url, stdin=True);

    print("---\nComments and info:\n---")

    try:
        os.mkdir(path + "comm_info\\");
    except:
        print(end="");

    subprocess.call("yt-dlp.exe --write-comments --write-comments --write-description --write-url-link --skip-download --output \"" + path + "comm_info\\" + outname + "\" " + url, stdin=True);

    print("---\nThumbnails:\n---")

    try:
        os.mkdir(path + "tumb\\");
    except:
        print(end="");

    subprocess.call("yt-dlp.exe --write-all-thumbnails --skip-download --output \"" + path + "tumb\\" + outname + "\" " + url, stdin=True);

    print("---\nSubs:\n---")

    loadsubs(url, path, outname, playlist);

    print("---\nConvert:\n---")

    try:
        subprocess.call(os.getcwd() + '\\ffmpeg\\bin\\ffmpeg.exe -i "' + path + outname + '.webm' + '" -i "' + path + outname + '.m4a' + '" -c copy "' + path + outname + '.mp4"');
    except:
        print(end="");

    print("---\nCleaning:\n---")

    try:
        os.remove(path + outname + '.m4a');
        os.remove(path + outname + '.webm');
    except:
        print(end="");

    return 0x0;

def only_mp3(url, path, outname, playlist = "", num = -1):
    try:
        subprocess.call("yt-dlp.exe --format m4a/bestaudio/best --output \"" + path + outname + '.m4a\" ' + url, stdin=True);

        subprocess.call(os.getcwd() + '\\ffmpeg\\bin\\ffmpeg.exe -i "' + path + outname + '.m4a' + '" -acodec libmp3lame -ab 320k "' + path + outname + '.mp3"');

        os.remove(path + outname + '.m4a');

        if playlist == "" or num == -1:
            Bool = input("Want cut(Y/N): ");
        else:
            Bool = "n";

        if Bool.lower() == "y":
            song = AudioSegment.from_mp3(path + outname + ".mp3");

            From = int(input("From(ms): "));
            To = int(input("To(ms): "));

            song = song[From:To];

            song.export(path + outname + "_cutted.mp3", format="mp3");

            Del = input("Delete not cutted version(Y/N): ");

            if Del.lower() == "y":
                os.remove(path + outname + ".mp3");
                os.rename(path + outname + "_cutted.mp3", path + outname + ".mp3");

        print("---\nThumbnail & tags:\n---")

        subprocess.call("yt-dlp.exe --convert-thumbnails jpg --write-thumbnail --skip-download --output \"" + path + "tmp_tumb" + "\" " + url, stdin=True);

        audio_file = eyed3.load(path + outname + ".mp3");
        audio_file.initTag(version=(2, 3, 0));

        audio_file.tag.artist = requests.get(url).text.split("<link itemprop=\"name\" content=\"")[1].split("\"")[0];
        audio_file.tag.title = outname;
        if playlist != "":
            audio_file.tag.album = playlist;
        if num != -1:
            audio_file.tag.track_num = num;

        with open(path + "tmp_tumb.jpg", "rb") as image_file:
            imagedata = image_file.read()

        audio_file.tag.images.set(3, imagedata, "image/jpeg", u"cover");

        audio_file.tag.save()

        print("---\nCleaning:\n---")

        os.remove(path + "tmp_tumb.jpg");

    except Exception as e:
        return e;

    return 0x0;


def loadsubs(url, path, outname, playlist):

    subprocess.call("yt-dlp.exe --list-subs " + url, stdin=True);

    if not playlist: lang = input("Language: ");
    else: lang = "all";

    if lang != "" and lang != "all":

        subprocess.call("yt-dlp.exe --write-sub --sub-format vtt --sub-langs " + lang + " --skip-download --output \"" + path + outname + "\" " + url, stdin=True);

    elif lang == "all":

        path += "subt\\";

        try:
            os.mkdir(path);
        except:
            print(end="");

        subprocess.call("yt-dlp.exe --no-write-auto-subs --all-subs --write-subs --sub-format vtt --skip-download --output \"" + path + outname + "\" " + url, stdin=True);

while True:

    time.sleep(0.5);

    modded = int(input("Mode(0(download_mp4)/1(download_mp3)/2(subs)): "));

    if (not (modded >= 0)) or (not (modded <= 2)):
        break;

    URL = input("URL: ");

    outname = input("Outname: ");

    path = input("Path: ") + "\\";

    print("---\nStart\n---");

    download(URL, modded, outname, path);


