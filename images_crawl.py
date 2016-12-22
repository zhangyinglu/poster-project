import images_tmdb
import json
import os
import time
import random
import urllib2

import logging;
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

def save_jdata(filename, data, disp = False):
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close()
    if disp:
        logging.info('{} saved'.format(filename))

def load_jdata(filename):
    f = open(filename, 'r')
    content = f.read()
    data = json.loads(content)
    f.close()
    return data

def load_dict(filename):
    return load_jdata(filename) if os.path.exists(filename) else dict()

def load_list(filename):
    return load_jdata(filename) if os.path.exists(filename) else list()

def set_encode(encode='utf-8'):
    import sys
    reload(sys)
    sys.setdefaultencoding(encode)

def catch_httperr(imdb_id):
    response = images_tmdb.imdb2tmdb(imdb_id)
    j = json.loads(response)
    tmdb_id = ''
    title = ''
    if len(j['movie_results']) > 0:
        if len(j['movie_results']) != 1:
            logging.info('warning: more than 1 movie result for {}'.format(imdb_id))
        info = j['movie_results'][0]
        if info.has_key('id'):
            tmdb_id = info['id']
        if info.has_key('title'):
            title = info['title']
    logging.info('imbd_id = {}, tmdb_id = {}, title = {}'.format(imdb_id, tmdb_id, title))
    return tmdb_id

import csv

def parse_links(filename = 'links_id84615-102800.csv'):
    # parse link file
    tmdb2imdb = dict()
    tmdb2ml = dict()
    missing_list = list()
    first_line = True
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        # format: ml_id, imdb_id, tmdb_id
        for line in reader:
            if first_line:
                first_line = False
                continue
            if line[-1].isdigit():
                tmdb2imdb[line[-1]] = line[1]
                tmdb2ml[line[-1]] = line[0]
            else:
                missing_list.append(line[0])
    # save missing id list
    filename = 'missing.json'
    save_jdata(filename, missing_list, disp = True)
    return (tmdb2imdb, tmdb2ml)

def crawl_keywords():
    set_encode()
    tmdb2imdb, tmdb2ml = parse_links()
    # load downloaded data
    filename = 'tmdb-keywords.json'
    keywords = load_dict(filename)
    filename = 'tmdb-id2name.json'
    id2name = load_dict(filename)
    # crawl
    complete_ids = keywords.keys()
    revise_list = list()
    for tmdb_id in tmdb2imdb.keys():
        if tmdb_id not in complete_ids:
            logging.info('tmdb_id = {}'.format(tmdb_id))
            try:
                response = images_tmdb.keyword(tmdb_id)
            except urllib2.HTTPError, e:
                logging.info("HTTPError!")
                imdb_id = tmdb2imdb[tmdb_id]
                revise_list.append((tmdb2ml[tmdb_id], imdb_id, catch_httperr(imdb_id), tmdb_id))
                continue
            j = json.loads(response)
            for word in j['keywords']:
                word_id = str(word['id']) # JSON only allows key names to be strings
                word_name = word['name']
                if word_id in id2name.keys():
                    if id2name[word_id] != word_name:
                        logging.info(tmbd_id, word_id, word_name, id2name[word_id])
                else:
                    id2name[word_id] = word_name
            keywords[tmdb_id] = [word['id'] for word in j['keywords']]
            # save intermediate result
            filename = 'cache-tmdb-keywords.json'
            save_jdata(filename, keywords, disp = False)
            filename = 'cache-tmdb-id2name.json'
            save_jdata(filename, id2name, disp = False)
            time.sleep(random.random())
    logging.info('revise information')
    for tup in revise_list:
        print ','.join([str(item) for item in tup])
    # save data
    filename = 'tmdb-keywords.json'
    save_jdata(filename, keywords, disp = True)
    filename = 'tmdb-id2name.json'
    save_jdata(filename, id2name, disp = True)

def crawl_overview():
    set_encode()
    tmdb2imdb, tmdb2ml = parse_links()
    # load downloaded data
    filename = 'tmdb-overview.json'
    overview = load_dict(filename)
    # crawl
    complete_ids = overview.keys()
    revise_list = list()
    for tmdb_id in tmdb2imdb.keys():
        if tmdb_id not in complete_ids:
            logging.info('tmdb_id = {}'.format(tmdb_id))
            try:
                response = tmdb.basic(tmdb_id)
            except urllib2.HTTPError, e:
                logging.info("HTTPError!")
                imdb_id = tmdb2imdb[tmdb_id]
                revise_list.append((tmdb2ml[tmdb_id], imdb_id, catch_httperr(imdb_id), tmdb_id))
                continue
            j = json.loads(response)
            if j.has_key('overview'):
                overview[tmdb_id] = j['overview']
            else:
                logging.info('{} no overview!'.format(tmdb_id))
            # save intermediate result
            filename = 'tmdb-overview.json.cache'
            save_jdata(filename, overview, disp = False)
            time.sleep(random.random())
    logging.info('revise information')
    for tup in revise_list:
        print ','.join([str(item) for item in tup])
    # save data
    filename = 'tmdb-overview.json'
    save_jdata(filename, overview, disp = True)

def crawl_reviews():
    set_encode()
    tmdb2imdb, tmdb2ml = parse_links()
    # load downloaded data
    filename = 'tmdb-reviews.json'
    reviews = load_dict(filename)
    # crawl
    complete_ids = reviews.keys()
    revise_list = list()
    for tmdb_id in tmdb2imdb.keys():
        if tmdb_id not in complete_ids:
            logging.info('tmdb_id = {}'.format(tmdb_id))
            try:
                response = images_tmdb.reviews(tmdb_id)
            except urllib2.HTTPError, e:
                logging.info("HTTPError!")
                imdb_id = tmdb2imdb[tmdb_id]
                revise_list.append((tmdb2ml[tmdb_id], imdb_id, catch_httperr(imdb_id), tmdb_id))
                continue
            j = json.loads(response)
            if j.has_key('results'):
                reviews[tmdb_id] = ' '.join([j['results'][i]['content'] for i in range(len(j['results']))])
            else:
                logging.info('key "results" not found in {} !'.format(tmdb_id))
            # save intermediate result
            filename = 'tmdb-reviews.json.cache'
            save_jdata(filename, reviews, disp = False)
            time.sleep(random.random())
    logging.info('revise information')
    for tup in revise_list:
        print ','.join([str(item) for item in tup])
    # save data
    filename = 'tmdb-reviews.json'
    save_jdata(filename, reviews, disp = True)

	

def crawl_images():
    set_encode()
    tmdb2imdb, tmdb2ml = parse_links()
    # load downloaded data
    filename = 'tmdb-images.json'
    images = load_dict(filename)
    filename = 'tmdb-id2name.json'
    id2name = load_dict(filename)
    # crawl
    complete_ids = images.keys()
    revise_list = list()
    for tmdb_id in tmdb2imdb.keys():
        if tmdb_id not in complete_ids:
            logging.info('tmdb_id = {}'.format(tmdb_id))
            try:
                response = images_tmdb.images(tmdb_id)
            except urllib2.HTTPError, e:
                logging.info("HTTPError!")
                imdb_id = tmdb2imdb[tmdb_id]
                revise_list.append((tmdb2ml[tmdb_id], imdb_id, catch_httperr(imdb_id), tmdb_id))
                continue
            j = json.loads(response)
            t = 0
            for posters in j['posters']:
                t = t+1
                poster_id = str(tmdb_id)+'_'+str(t)# JSON only allows key names to be strings
                poster_path = posters['file_path']
                if poster_id in id2name.keys():
                    if id2name[poster_id] != poster_path:
                        logging.info(tmbd_id, poster_id, poster_path, id2name[poster_id])
                else:
                    id2name[tmdb_id] = poster_path
            images[tmdb_id]=[poster['file_path'] for poster in j['posters']]
            # save intermediate result
            filename = 'cache-tmdb-images_id84615-102800.json'
            save_jdata(filename, images, disp = False)
            filename = 'cache-tmdb-id2name_id84615-102800.json'
            save_jdata(filename, id2name, disp = False)
            time.sleep(random.random())
    logging.info('revise information')
    for tup in revise_list:
        print ','.join([str(item) for item in tup])
    # save data
    filename = 'tmdb-images_id84615-102800.json'
    save_jdata(filename, images, disp = True)
    filename = 'tmdb-id2name_id84615-102800.json' 
    save_jdata(filename, id2name, disp = True)
	
if __name__ == '__main__':
    import sys
    job_type = 'images'
    if len(sys.argv) > 1:
        job_type = sys.argv[1]
    if job_type == 'keywords':
        crawl_keywords()
    elif job_type == 'overview':
        crawl_overview()
    elif job_type == 'reviews':
        crawl_reviews()
    elif job_type == 'images':
        crawl_images()
    else:
        logging.info('unknown job type: {}'.format(job_type))