#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 指定アカウントのつぶやきを以下フォーマットでファイルに出力する
# id, retweet_count, like_count, reply_count, quote_count, text, @timestamp

import env_twitter as env_obj
import arg_twitter as arg_obj
import sys
import os
import requests
import json
import logging
from requests_oauthlib import OAuth1Session
from base64 import b64decode, b64encode

global_tw_list = []


# set_tweet_globallist(tweet_dict, account, logfile_path)
# argument:
#   tweet_dict: 
#   account: データ取得対象twitterアカウント
#   logfile_path: 出力対象ログファイル名
# return
#   0: 正常
#   1: データ取得なし
def set_tweet_globallist(tweet_dict, account, logfile_path):

    rtn = 0
    try:
        tw_data_dict = tweet_dict['data']

        for this_tweet in tw_data_dict:
            this_json = {
                "id": this_tweet['id'],
                "retweet_count": this_tweet['public_metrics']['retweet_count'],
                "like_count": this_tweet['public_metrics']['like_count'],
                "reply_count": this_tweet['public_metrics']['reply_count'],
                "quote_count": this_tweet['public_metrics']['quote_count'],
                "text": this_tweet['text'],
                "@timestamp": this_tweet['created_at']
            }
            global_tw_list.insert(0, this_json)
    except KeyError:
        rtn = 1

    return rtn

def write_tweetlog(logfile_path):

    for this_line in global_tw_list:
        with open(logfile_path, 'a') as fd:
            json.dump(this_line, fd, ensure_ascii=False)
            fd.write('\n')


def get_lastid(logfile_path):

    n = 0
    with open(logfile_path, 'r') as fd:
        exist_list = fd.read().split("\n")

    last_json = json.loads(exist_list[-2])
    last_id = last_json['id']

    return last_id


if __name__ == '__main__':

    consumer_key = env_obj.CONSUMER_KEY
    consumer_secret_key = env_obj.CONSUMER_SECRET_KEY
    access_token = env_obj.ACCESS_TOKEN
    access_token_secret = env_obj.ACCESS_TOKEN_SECRET
    twitter = OAuth1Session(consumer_key,
                            consumer_secret_key,
                            access_token,
                            access_token_secret)

    try:
        args = sys.argv
        your_twitter_name = args[1]
    except IndexError:
        your_twitter_name = arg_obj.TARGET_ACCOUNT

    # get userid
    url = "https://api.twitter.com/2/users/by/username/" + your_twitter_name
    res = twitter.get(url)
    user_data_dict = json.loads(res.text)
    user_id = user_data_dict['data']['id']

    url = "https://api.twitter.com/2/users/" + user_id + "/tweets"

    # check exist log
    logfile_path = "/var/log/twitter_appli/" \
                   + your_twitter_name + arg_obj.LOGNMAE_KEYWORD
    chk_res = os.path.exists(logfile_path)

    if chk_res is True:
        # log file exeit patern
        last_tweetid = get_lastid(logfile_path)
        try:
            param_data = {'max_results': '100',
                          'tweet.fields': 'author_id,created_at,public_metrics',
                          'since_id': last_tweetid}
            res = twitter.get(url, params=param_data)
            tweet_data_dict = json.loads(res.text)

            next_token = tweet_data_dict['meta']['next_token']
        except KeyError:
                add_res = set_tweet_globallist(tweet_data_dict,
                                           your_twitter_name,
                                           logfile_path)
                if add_res == 1:
                    print("There is no new data")
                    sys.exit()                
                wrt_res = write_tweetlog(logfile_path)
                print("This adding progress is end")
                sys.exit()
    else:
        # the first take tweet
        param_data = {'max_results': '100',
                      'tweet.fields': 'author_id,created_at,public_metrics'}
        res = twitter.get(url, params=param_data)
        tweet_data_dict = json.loads(res.text)

        next_token = tweet_data_dict['meta']['next_token']
        fst_res = set_tweet_globallist(tweet_data_dict,
                                       your_twitter_name,
                                       logfile_path)

    # get all tweet
    while True:
        if next_token is None:
            print(next_token)
            break;
        else:
            try:
                param_data = {'max_results': '100','tweet.fields': 'author_id,created_at,public_metrics','pagination_token': next_token}
                res = twitter.get(url, params=param_data)
                tweet_data_dict = json.loads(res.text)
                next_token = tweet_data_dict['meta']['next_token']
                fst_res = set_tweet_globallist(tweet_data_dict,
                                               your_twitter_name,
                                               logfile_path)
            except KeyError:
                wrt_res = write_tweetlog(logfile_path)
                print("All loading is finished")
                sys.exit()

