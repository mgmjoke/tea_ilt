#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import env_twitter as env_obj
import arg_twitter as arg_obj
import sys
import json
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


if __name__ == '__main__':

    try:
        args = sys.argv
        account= args[1]
    except IndexError:
        account = arg_obj.TARGET_ACCOUNT

    es_ipaddress = "172.31.31.247"
    elastic_user = "elastic"
    elastic_pass = "password"

    index_source = '{ "settings": { "index": { "number_of_shards": "2", "number_of_replicas": "1" }, "analysis": { "analyzer": { "ilt_kuromoji_analyzer": { "type": "custom", "char_filter": "kuromoji_iteration_mark", "tokenizer": "kuromoji_tokenizer", "filter": [ "ilt_stop_words_filter","ilt_stop_posfilter" ] } }, "filter": { "ilt_stop_words_filter": { "type": "stop", "ignore_case": true, "stopwords": [ "https", "RT", "CO", "t", "お", "し", "と", "か", "ん","さ","れ" ] }, "ilt_stop_posfilter": { "type": "kuromoji_part_of_speech", "stoptags": [ "記号-アルファベット", "記号-一般", "助詞-接続助詞", "助詞-格助詞", "助詞-格助詞-一般", "助詞-格助詞-連語", "助詞-係助詞", "助詞-終助詞", "助詞-副助詞", "助詞-副詞化", "助詞", "助詞-接続助詞", "助詞-並立助詞", "助詞-連体化","助動詞", "名詞-数" ]          }      }    }  },  "mappings": {    "properties": {      "id": {        "type": "keyword"      },      "retweet_count": {        "type": "long"      },      "text": {        "type": "text",        "fielddata": true,        "analyzer": "ilt_kuromoji_analyzer"      },      "username": {        "type": "keyword"      },      "favorite_count": {        "type": "long"      }    }  }}'
    
    index_name = "tea_index_" + account
    dest_url = "https://" + elastic_user + ":" + elastic_pass + "@" + es_ipaddress + ":9200" + "/" + index_name
    headers = {'Content-Type': 'application/json'}
    res = requests.put(dest_url, headers=headers, data=index_source.encode('utf-8'), verify = False, auth=(elastic_user, elastic_pass))
    print(res.text)
