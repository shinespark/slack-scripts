#!/usr/bin/env python
# coding: utf-8
import sys
import utils


def main():
    argvs = sys.argv
    if len(argvs) != 2:
        print('usage:\n    delete_old_files.py <Slack Web API token>\n')
        exit()

    end_point = 'https://slack.com/api/'
    token= argvs[1]
    token = '?token=' + token

    # fetch files.list
    files_list = utils.fetch_all_files(end_point + 'files.list' + token)

    # show your files
    for f in target_files_list:
        print(f['id'], f['url_private'])

    # files.delete
    print('------------------------------')
    print('{0} 件削除します。よろしいですか？'.format(len(target_your_files_list)))
    ans = utils.prompt()

    if ans == 'y' or ans == 'Y':
        for f in target_files_list:
            print(f['id'], f['url_private'])
            delete_status = utils.fetch(end_point + 'files.delete' + token + '&file=' + f['id'])
            print(delete_status)

        print('complete!!')


if __name__ == "__main__":
    main()
