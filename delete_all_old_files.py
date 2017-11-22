#!/usr/bin/env python
# coding: utf-8
import sys
import utils
from datetime import datetime, timedelta


def main():
    argvs = sys.argv
    if len(argvs) != 2:
        print('usage:\n    delete_all_old_files.py <Slack Web API token>\n')
        exit()

    end_point = 'https://slack.com/api/'
    token= argvs[1]
    token = '?token=' + token

    # fetch files.list
    last_month_timestamp = (datetime.now() + timedelta(days=-30)).strftime('%s')
    files_list = utils.fetch_all_files(end_point + 'files.list' + token + '&ts_to=' + last_month_timestamp)

    # show your files
    for f in files_list:
        print(f['id'], f['url_private'])

    # files.delete
    print('------------------------------')
    print('{0} 件削除します。よろしいですか？'.format(len(files_list)))
    ans = utils.prompt()

    if ans == 'y' or ans == 'Y':
        for f in files_list:
            print(f['id'], f['url_private'])
            delete_status = utils.fetch(end_point + 'files.delete' + token + '&file=' + f['id'])
            print(delete_status)

        print('complete!!')


if __name__ == "__main__":
    main()
