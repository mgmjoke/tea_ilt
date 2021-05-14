#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import arg_twitter as arg_obj
import env_twitter as env_obj
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

    kb_ipaddress = "172.31.27.10"
    elastic_user = "elastic"
    elastic_pass = "password"

    index_pattern_key = "tea_index_"
    index_pattern_name = index_pattern_key + account
    index_pattern_data = '{"attributes": {"title":"' + index_pattern_name + '*","timeFieldName": "@timestamp"}}'
    print(index_pattern_data)

    dest_url = "https://" + elastic_user + ":" + elastic_pass + "@" + kb_ipaddress + ":5601/api/saved_objects/index-pattern/" + index_pattern_name
    headers = {'Content-Type': 'application/json', 'kbn-xsrf': 'true'}
    res = requests.post(dest_url, headers=headers, data=index_pattern_data.encode('utf-8'), verify = False, auth=(elastic_user, elastic_pass))
    print(res.text)
