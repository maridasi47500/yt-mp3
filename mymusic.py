from directory import Directory
import os
class Music(Directory):
    def __init__(self,name):
        self.name=name

        self.file_stats = os.stat("."+name)
        self.file_size = self.file_stats.st_size
        self.music={"music":name.split(".")[1], "size":self.file_size}
        self.content=open("."+name, 'rb').read()
    def get_name(self):
        return self.name
    def get_html(self):
        return self.content
