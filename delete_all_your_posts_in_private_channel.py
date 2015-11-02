#!/usr/bin/env python
# coding: utf-8
import sys
import utils


def main():
    argvs = sys.argv
    if len(argvs) != 4:
        print('usage:\n    delete_all_your_posts_in_private_channel.py <Slack Web API token> <Your Slack name> <Private channel name>\n')
        exit()

    end_point = 'https://slack.com/api/'
    token, your_name, target_group_name = argvs[1:]
    token = '?token=' + token

    # fetch users.list
    users_list = utils.fetch(end_point + 'users.list' + token)
    your_id = [member['id'] for member in users_list['members'] if member.get('name') == your_name][0]
    print('your_id: ' + your_id)

    # fetch groups.list
    groups_list = utils.fetch(end_point + 'groups.list' + token)
    target_group_id = [group['id'] for group in groups_list['groups'] if group.get('name') == target_group_name][0]
    print('group_id: ' + target_group_id)

    # fetch groups.history
    groups_history = utils.fetch_all_history(end_point + 'groups.history' + token + '&channel=' + target_group_id + '&count=1000')
    your_posts_list = [message for message in groups_history if message.get('user') == your_id and message.get('subtype', '') == '']

    # show your posts
    for message in your_posts_list:
        print(message['text'].replace('\n', ''), message['ts'])

    # chat.delete
    print('{0} 件削除します。よろしいですか？'.format(len(your_posts_list)))
    while True:
        ans = input('[y/n] > ')
        if ans in 'yYnN' and ans != '':
            break

    if ans == 'y' or ans == 'Y':
        for message in your_posts_list:
            print(message['text'].replace('\n', ''), message['ts'])
            delete_status = utils.fetch(end_point + 'chat.delete' + token + '&ts=' + message['ts'] + '&channel=' + target_group_id)
            print(delete_status)

        print('complete!!')


if __name__ == "__main__":
    main()
