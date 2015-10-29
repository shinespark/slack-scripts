# coding: utf-8
import json
import urllib.request
import yaml


def main():
    end_point = 'https://slack.com/api/'
    conf = yaml.load(open('conf.yaml').read())
    token = '?token=' + conf['token']
    your_name = conf['your_name']
    target_group_name = conf['group_name']

    # fetch users.list
    users_list = fetch(end_point + 'users.list' + token)
    your_id = [member['id'] for member in users_list['members'] if member.get('name') == your_name][0]
    print(your_id)

    # fetch groups.list
    groups_list = fetch(end_point + 'groups.list' + token)
    target_group_id = [group['id'] for group in groups_list['groups'] if group.get('name') == target_group_name][0]
    print(target_group_id)

    # fetch groups.history
    groups_history = fetch_all_history(end_point + 'groups.history' + token + '&channel=' + target_group_id + '&count=1000')
    your_posts_list = [message for message in groups_history if message.get('user') == your_id and message.get('subtype', '') == '']

    for message in your_posts_list:
        print(message['text'], message['ts'])

    # chat.delete
    for message in your_posts_list:
        delete_status = fetch(end_point + 'chat.delete' + token + '&ts=' + message['ts'] + '&channel=' + target_group_id)
        print(delete_status)

    print('complete!!')


def fetch(url):
    print(url)
    res = urllib.request.urlopen(url)
    res_body = json.loads(res.read().decode('utf-8'))
    return res_body


def fetch_all_history(url, base_url='', all_list=[]):
    print(url)

    # init
    if base_url == '':
        base_url = url

    res = urllib.request.urlopen(url)
    res_body = json.loads(res.read().decode('utf-8'))
    all_list += res_body['messages']

    if res_body['has_more']:
        latest = res_body['messages'][-1]['ts']
        url = base_url + '&latest=' + latest
        fetch_all_history(url, base_url, all_list)

    return all_list


if __name__ == "__main__":
    main()
