# coding: utf-8
import yaml
import utils


def main():
    end_point = 'https://slack.com/api/'
    conf = yaml.load(open('conf.yaml').read())
    token = '?token=' + conf['token']
    your_name = conf['your_name']
    target_group_name = conf['group_name']

    # fetch users.list
    users_list = utils.fetch(end_point + 'users.list' + token)
    your_id = [member['id'] for member in users_list['members'] if member.get('name') == your_name][0]
    print(your_id)

    # fetch groups.list
    groups_list = utils.fetch(end_point + 'groups.list' + token)
    target_group_id = [group['id'] for group in groups_list['groups'] if group.get('name') == target_group_name][0]
    print(target_group_id)

    # fetch groups.history
    groups_history = utils.fetch_all_history(end_point + 'groups.history' + token + '&channel=' + target_group_id + '&count=1000')
    your_posts_list = [message for message in groups_history if message.get('user') == your_id and message.get('subtype', '') == '']

    for message in your_posts_list:
        print(message['text'], message['ts'])

    # chat.delete
    print(' {0} 件削除します'.format(len(your_posts_list)))
    for message in your_posts_list:
        delete_status = utils.fetch(end_point + 'chat.delete' + token + '&ts=' + message['ts'] + '&channel=' + target_group_id)
        print(delete_status)

    print('complete!!')


if __name__ == "__main__":
    main()
