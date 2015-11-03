#!/usr/bin/env python
# coding: utf-8
import sys
import utils


def main():
    argvs = sys.argv
    if len(argvs) != 4:
        print('usage:\n    delete_all_your_files_in_direct_message.py <Slack Web API token> <Your Slack name> <Target user name>\n')
        exit()

    end_point = 'https://slack.com/api/'
    token, your_name, target_user_name = argvs[1:]
    token = '?token=' + token

    # fetch users.list
    users_list = utils.fetch(end_point + 'users.list' + token)
    your_id = [member['id'] for member in users_list['members'] if member.get('name') == your_name][0]
    target_user_id = [member['id'] for member in users_list['members'] if member.get('name') == target_user_name][0]
    print('your_id: ' + your_id)
    print('target_user_id: ' + target_user_id)

    # fetch im.list
    im_list = utils.fetch(end_point + 'im.list' + token)
    target_im_id = [im['id'] for im in im_list['ims'] if im.get('user') == target_user_id][0]
    print('target_im_id: ' + target_im_id)

    # fetch files.list
    your_files_list = utils.fetch_all_files(end_point + 'files.list' + token + '&user=' + your_id)
    target_ims_your_files_list = [f for f in your_files_list if target_im_id in f.get('ims')]

    # show your files
    for f in target_ims_your_files_list:
        print(f['id'], f['url_private'])

    # files.delete
    print('------------------------------')
    print('{0} 件削除します。よろしいですか？'.format(len(target_ims_your_files_list)))
    ans = utils.prompt()

    if ans == 'y' or ans == 'Y':
        for f in target_ims_your_files_list:
            print(f['id'], f['url_private'])
            delete_status = utils.fetch(end_point + 'files.delete' + token + '&file=' + f['id'])
            print(delete_status)

        print('complete!!')


if __name__ == "__main__":
    main()
