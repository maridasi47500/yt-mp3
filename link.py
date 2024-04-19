# coding=utf-8
import sqlite3
import sys
from pytube import YouTube
import random
import string
import re
from model import Model
import yt_dlp as youtube_dl
import glob # directory operations
import os # interface to os-provided info on files
import sys # interface to command line
from pydub import AudioSegment # only audio operations



# example usage:
# python ytauddown.py https://www.youtube.com/watch?v=8OAPLk20epo 9:51 14:04


class Link(Model):
    def __init__(self):
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists link(
        id integer primary key autoincrement,
        user_id integer,
            url text,
            filename text
                    );""")
        self.con.commit()
        #self.con.close()
    def getall(self):
        self.cur.execute("select * from link")

        row=self.cur.fetchall()
        return row
    def deletebyid(self,myid):

        self.cur.execute("delete from link where id = ?",(myid,))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def getbyid(self,myid):
        self.cur.execute("select * from link where id = ?",(myid,))
        row=dict(self.cur.fetchone())
        print(row["id"], "row id")
        job=self.cur.fetchall()
        return row
    def create(self,params):
        print("ok")
        myhash={}
        for x in params:
            if 'confirmation' in x:
                continue
            if 'envoyer' in x:
                continue
            if 'download' in x:
                continue
            if '[' not in x and x not in ['routeparams']:
                #print("my params",x,params[x])
                try:
                  myhash[x]=str(params[x].decode())
                except:
                  myhash[x]=str(params[x])
        print("M Y H A S H")
        print(myhash,myhash.keys())
        if "MP3" in params["download"]:
          myhash["filename"]=self.main(myhash["url"])
        else:
          myhash["filename"]=self.video(myhash["url"])
        myid=None
        try:
          self.cur.execute("insert into link (user_id,url,filename) values (:user_id,:url,:filename)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["link_id"]=myid
        azerty["notice"]="votre link a été ajouté"
        return azerty
    def newest_mp4_filename(self):
        # lists all mp3s in local directory
        list_of_mp3s = glob.glob('./*.mp4')
        # returns mp3 with highest timestamp value
        return max(list_of_mp3s, key = os.path.getctime)
    def newest_mp3_filename(self):
        # lists all mp3s in local directory
        list_of_mp3s = glob.glob('./*.mp3')
        # returns mp3 with highest timestamp value
        return max(list_of_mp3s, key = os.path.getctime)
    
    def get_video_time_in_ms(self,video_timestamp):
        vt_split = video_timestamp.split(":")
        if (len(vt_split) == 3): # if in HH:MM:SS format
            hours = int(vt_split[0]) * 60 * 60 * 1000
            minutes = int(vt_split[1]) * 60 * 1000
            seconds = int(vt_split[2]) * 1000
        else: # MM:SS format
            hours = 0
            minutes = int(vt_split[0]) * 60 * 1000
            seconds = int(vt_split[1]) * 1000
        # time point in miliseconds
        return hours + minutes + seconds
    
    def get_trimmed(self,mp3_filename, initial, final = ""):
        if (not mp3_filename):
            # raise an error to immediately halt program execution
            raise Exception("No MP3 found in local directory.")
        # reads mp3 as a PyDub object
        sound = AudioSegment.from_mp3(mp3_filename)
        t0 = get_video_time_in_ms(initial)
        print("Beginning trimming process for file ", mp3_filename, ".\n")
        print("Starting from ", initial, "...")
        if (len(final) > 0):
            print("...up to ", final, ".\n")
            t1 = get_video_time_in_ms(final)
            return sound[t0:t1] # t0 up to t1
        return sound[t0:] # t0 up to the end
    
    
    
    # downloads yt_url to the same directory from which the script runs
    def download_audio(self,yt_url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
    
    def video(self,url=""):
        yt = YouTube(url)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
        filename = self.newest_mp4_filename()
        N=10
        newfilename=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))+".mp4"
        os.rename(filename, ("./uploads/"+newfilename))
        return newfilename
    def main(self,arg1=None,arg2=None,arg3=None):
        if (arg1 is None):
            print("Please insert a multimedia-platform URL supported by youtube-dl as your first argument.")
            return
        yt_url = arg1
        self.download_audio(yt_url)
        filename = self.newest_mp3_filename()
        N=10
        newfilename=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))+".mp3"
        os.rename(filename, ("./uploads/"+newfilename))
        if (arg2 is None): # exit if no instants as args
            return newfilename
        initial = arg2
        final = ""
        if (arg3 is not None):
            final = arg3
        filename = self.newest_mp3_filename()
        N=10

        trimmed_file = get_trimmed(filename, initial, final)
        trimmed_filename = "".join([filename.split(".mp3")[0], "- TRIM.mp3"])
        print("Process concluded successfully. Saving trimmed file as ", trimmed_filename)
        # saves file with newer filename
        trimmed_file.export(trimmed_filename, format="mp3")
    
    
    
    
