#!/usr/bin/python
#
__author__ = 'author'

try:
  from xml.etree import ElementTree # for Python 2.5 users
except:
  from elementtree import ElementTree

from gdata import service
import gdata
import atom
import getopt
import sys


def main():
  # parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["f=","u=", "p="])
  except getopt.error, msg:
    print ('bg.py --f [file] --u [username] --p [password] | inline')
    sys.exit(2)

  file = ''
  user=''
  password = ''

  # Process options
  for o, a in opts:
    if o == "--f":
      file= a
    elif o == "--u":
      user=a
    elif o == "--p":
      password = a

  if password =="inline":
        print 'enter password:'
	password = sys.stdin.readline()  

  if file == '' or password == '' or user=='':
    print ('python blog.py --f [file] --u [username]  --p [password] | inline ')
    sys.exit(2)
    
  fileHandle = open (file)
  
  #sample = BloggerExample(user, password)
  #sample.CreatePost (fileHandle.readline() ,fileHandle.read() , "bloger", False)
   
  servic = service.GDataService(user, password)
  servic.source = 'Blogger_Python_Sample-1.0'
  servic.service = 'blogger'
  servic.server = 'www.blogger.com'
  servic.ProgrammaticLogin() 


  feed = servic.Get('/feeds/default/blogs')
  self_link = feed.entry[0].GetSelfLink()
  if self_link:
	blog_id = self_link.href.split('/')[-1]

  
  entry = gdata.GDataEntry()
  entry.author.append(atom.Author(atom.Name(text='author')))
  entry.title = atom.Title(title_type='xhtml', text=fileHandle.readline() )
  entry.content = atom.Content(content_type='html', text=fileHandle.read())

#if is_draft:
#  control = atom.Control()
#  control.draft = atom.Draft(text='yes')
#  entry.control = control

# Ask the service to insert the new entry.
  servic.Post(entry, '/feeds/' + blog_id + '/posts/default')

  print('publishing completed')
  fileHandle.close() 

if __name__ == '__main__':
  main()
