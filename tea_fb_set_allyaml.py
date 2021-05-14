#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys

ILT_FILE_DIR = "/home/analyzer/twitter_appli/file_dir/"
CREATE_FB_CONF_NAME = ILT_FILE_DIR + "all_filebeat.yml"
ANS_TOP_LIST = ILT_FILE_DIR + "ansible_tea_ilt_collectvars"


if __name__ == '__main__':

    max_size = 11
    with open(ANS_TOP_LIST, 'r') as fd:
        fb_list0 = fd.read().replace('  - ', '').split("\n")
    fb_list = fb_list0[1:max_size]

    with open(CREATE_FB_CONF_NAME, 'w') as fd:
        fd.write("filebeat.inputs:\n")
        for account in fb_list:
            fd.write("- type: log\n")
            fd.write("  enabled: true\n")
            fd.write("  paths:\n")
            fd.write("    - /var/log/twitter_appli/" + account + "_Tweet.log\n")
            fd.write("  tags: ['" + account + "']\n")
            fd.write("  json.keys_under_root: true\n")
            fd.write("  json.overwrite_keys: true\n")
            fd.write("  json.add_error_key: true\n")
            fd.write("  processors:\n")
            fd.write("    - decode_json_fields:\n")
            fd.write('        fields: ["message"]\n')
            fd.write("        process_array: false\n")
            fd.write("        max_depth: 2\n")
            fd.write("        overwrite_keys: true\n")

        fd.write("\n")
        fd.write("output.elasticsearch:\n")
        fd.write("  hosts: ['https://172.31.31.247:9200']\n")
        fd.write("  indices:\n")
        for account in fb_list:
            index_str = "    - index: twitter_text_" + account
            fd.write(index_str + "\n")
            fd.write("      when.contains:\n")
            fd.write("        tags: " + account + "\n")
            
        fd.write("\n")
        fd.write('  ssl.certificate_authorities: ["/etc/filebeat/certs/elastic-filebeat-certificates-ca.pem"]\n')
        fd.write("  ssl.verification_mode: none\n")
        fd.write("  username: elastic\n")
        fd.write("  password: password\n")
        fd.write("logging.level: info\n")
        fd.write("logging.to_files: true\n")
        fd.write("logging.files:\n")
        fd.write("  path: /var/log/filebeat\n")
        fd.write("  name: filebeat\n")
        fd.write("  keepfiles: 7\n")
        fd.write("  permissions: 0644\n")
