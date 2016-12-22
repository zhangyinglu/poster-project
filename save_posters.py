# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 10:56:01 2016

@author: admin
"""

import os
import urllib2
import json
import urllib

with open ('tmdb-images_id84615-102800.json','r') as f:
    path = json.load(f)
    for id,poster_path in path.iteritems():
        tobecheckdir =r'E:\CUHKGoodStudy\Research Project\movie_poster_crawl\posters\\'+str(id)
        if os.path.isdir(tobecheckdir) != True:
            os.mkdir(r'E:\CUHKGoodStudy\Research Project\movie_poster_crawl\posters\\'+str(id)) 
        for path_i in poster_path:
            print path_i
            url = 'https://image.tmdb.org/t/p/original' + path_i
            try:
                urllib.urlretrieve(url,'E:\CUHKGoodStudy\Research Project\movie_poster_crawl\posters\\'+str(id)+'\\'+path_i)
            except e:
                print "HTTPError!"
                continue