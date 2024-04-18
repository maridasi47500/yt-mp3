# coding=utf-8
import sqlite3
import sys
import re
from model import Model
from bs4 import BeautifulSoup
class Post(Model):
    def get_text(self,hey):
        return BeautifulSoup(hey).get_text()
    def __init__(self):
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.con.create_function("GET_TEXT",1,self.get_text)
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists post(
        id integer primary key autoincrement,
        title text,
            content text,
            user_id integer,
            band_id integer
                    );""")
        self.con.commit()
        #self.con.close()
    def search(self,search):
        s="%"+search.replace(" ","%")+"%"
        t=search.split(" ")[0]
        self.cur.execute("select *, GET_TEXT(content) as mycontent, INSTR(lower(GET_TEXT(content)), ?) position1, INSTR(lower(GET_TEXT(title)),?) position2 from post where lower(GET_TEXT(title)) like ? or lower(GET_TEXT(content)) like ?", (t,t,s,s))
        row=self.cur.fetchall()
        return row
    def getall(self):
        self.cur.execute("select * from post")
        row=self.cur.fetchall()
        return row
    def deletebyid(self,myid):
        self.cur.execute("delete from post where id = ?",(myid,))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def getbyid(self,myid):
        self.cur.execute("select * from post where id = ?",(myid,))
        row=dict(self.cur.fetchone())
        print(row["id"], "row id")
        job=self.cur.fetchall()
        return row
    def update(self,params):
        print("ok")
        myhash={}
        for x in params:
            if 'confirmation' in x:
                continue
            if 'envoyer' in x:
                continue
            if '[' not in x and x not in ['routeparams']:
                #print("my params",x,params[x])
                try:
                  myhash[x]=str(params[x].decode())
                except:
                  myhash[x]=str(params[x])
        print("M Y H A S H")
        print(myhash,myhash.keys())
        myid=None
        try:
          self.cur.execute("update post set title = :title,content=:content where id = :id",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["post_id"]=myid
        azerty["notice"]="votre post a été modifié"
        return azerty




    def create(self,params):
        print("ok")
        myhash={}
        for x in params:
            if 'confirmation' in x:
                continue
            if 'envoyer' in x:
                continue
            if '[' not in x and x not in ['routeparams']:
                #print("my params",x,params[x])
                try:
                  myhash[x]=str(params[x].decode())
                except:
                  myhash[x]=str(params[x])
        print("M Y H A S H")
        print(myhash,myhash.keys())
        myid=None
        try:
          self.cur.execute("insert into post (title,content,user_id,band_id) values (:title,:content,:user_id,:band_id)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["post_id"]=myid
        azerty["notice"]="votre post a été ajouté"
        return azerty




