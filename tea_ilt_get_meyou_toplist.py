#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import urllib.request
from bs4 import BeautifulSoup

ILT_FILE_DIR = "/home/analyzer/twitter_appli/file_dir/"
ILT_FILE_NAME = ILT_FILE_DIR + "ansible_tea_ilt_collectvars"
TOPLIST_NUM = 10

if __name__ == '__main__':

    args = sys.argv

    targeturl = "https://meyou.jp/ranking/follower_allcat"
    res = urllib.request.urlopen(targeturl)
    soup = soup = BeautifulSoup(res, 'html.parser')

    name_data = soup.select('span[class="author-username"]')

    account_list = []
    exclude_keyword = 'span class="author-username"'
    for thisline in name_data:
        thisname = (thisline.string)
        if exclude_keyword not in thisname:
            acount = thisname.replace('@','').replace(' ','').replace('\n','').replace('\r','').replace('\t','')
            account_list.append(acount)
    account_list_top10 = account_list[0:TOPLIST_NUM]
    print(account_list_top10)

    if 2 <= len(args):
        if args[1] == "file":
            with open(ILT_FILE_NAME, "w") as fd:
                fd.write("account_list:\n")
            for this_val in account_list_top10:
                with open(ILT_FILE_NAME, "a") as fd:
                    fd.write("  - " + this_val.lower() + "\n")
            print("collect data to " + ILT_FILE_NAME)
        else:
            exit()
