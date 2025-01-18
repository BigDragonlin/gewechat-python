class Send_message:
    def __init__(self):
        pass

    # def send_msg_to_person(name, message)

    def send_msg_by_wxid(sdlf, wxid, message):
        send_msg_result = client.post_text(app_id, wxid, "你好啊")
        if send_msg_result.get('ret') != 200:
            print("发送消息失败:", send_msg_result)
        return
        print("发送消息成功:", send_msg_result)


# 找到好友，给好友发消息
def send_msg(client, app_id):
    send_msg_nickname = "林木"  # 要发送消息的好友昵称
    # 获取好友列表
    fetch_contacts_list_result = client.fetch_contacts_list(app_id)
    if fetch_contacts_list_result.get('ret') != 200 or not fetch_contacts_list_result.get('data'):
        print("获取通讯录列表失败:", fetch_contacts_list_result)
        return
    # {'ret': 200, 'msg': '操作成功', 'data': {'friends': ['weixin', 'fmessage', 'medianote', le', 'wxid_abcxx'], 'chatrooms': ['1234xx@chatroom'], 'ghs': ['gh_xx']}}
    friends = fetch_contacts_list_result['data'].get('friends', [])
    if not friends:
        print("获取到的好友列表为空")
        return
    print("获取到的好友列表:", friends)

    # 获取好友的简要信息
    friends_info = client.get_brief_info(app_id, friends)
    if friends_info.get('ret') != 200 or not friends_info.get('data'):
        print("获取好友简要信息失败:", friends_info)
        return
    # 找对目标好友的wxid
    friends_info_list = friends_info['data']
    if not friends_info_list:
        print("获取到的好友简要信息列表为空")
        return
    wxid = None
    for friend_info in friends_info_list:
        if friend_info.get('nickName') == send_msg_nickname:
            print("找到好友:", friend_info)
            wxid = friend_info.get('userName')
            break
    if not wxid:
        print(f"没有找到好友: {send_msg_nickname} 的wxid")
        return
    print("找到好友:", wxid)

    # 发送消息
    send_msg_result = client.post_text(app_id, wxid, "你好啊")
    if send_msg_result.get('ret') != 200:
        print("发送消息失败:", send_msg_result)
        return
    print("发送消息成功:", send_msg_result)
    return True
