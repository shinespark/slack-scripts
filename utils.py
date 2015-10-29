# coding: utf-8
import json
import urllib.request


def fetch(url):
    print(url)
    res = urllib.request.urlopen(url)
    res_body = json.loads(res.read().decode('utf-8'))
    return res_body


def fetch_all_history(url, base_url=None, all_list=None):
    print(url)

    # init
    if not base_url:
        base_url = url

    if not all_list:
        all_list = []

    res = urllib.request.urlopen(url)
    res_body = json.loads(res.read().decode('utf-8'))
    all_list += res_body['messages']

    if res_body['has_more']:
        latest = res_body['messages'][-1]['ts']
        url = base_url + '&latest=' + latest
        fetch_all_history(url, base_url, all_list)

    return all_list


def fetch_all_files(url, base_url=None, all_list=None):
    print(url)

    # init
    if not base_url:
        base_url = url

    if not all_list:
        all_list = []

    res = urllib.request.urlopen(url)
    res_body = json.loads(res.read().decode('utf-8'))
    all_list += res_body['files']

    if res_body['paging']['page'] < res_body['paging']['pages']:
        page = res_body['paging']['page'] + 1
        url = base_url + '&page=' + str(page)
        fetch_all_files(url, base_url, all_list)

    return all_list
