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

    src_index_key = "twitter_text_"
    dest_index_key = "tea_index_"

    reindex_data = '{ "source": { "index":"' + src_index_key + account + '"},"dest":{ "index":"' + dest_index_key + account +'"}}'

    index_name = "tea_index_" + account
    dest_url = "https://" + elastic_user + ":" + elastic_pass + "@" + es_ipaddress + ":9200/_reindex"
    headers = {'Content-Type': 'application/json'}
    res = requests.post(dest_url, headers=headers, data=reindex_data.encode('utf-8'), verify = False, auth=(elastic_user, elastic_pass))
    print(res.text)
