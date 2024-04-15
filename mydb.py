from band import Band 
from musician import Musician
from member import Member
from post import Post
class Mydb():
  def __init__(self):
    self.Member=Member()
    self.Post=Post()
    self.Musician=Musician()
    self.Band=Band()
