import json
def personal_message_handler(data):
    # 检查 'Data' 键是否存在
    if "Data" not in data:
        print("Error: 'Data' key is missing in the input data.")
        return
    # 获取 'PushContent'
    push_content = data["Data"].get("MsgType")
    
    # 检查 'PushContent' 是否为预期类型
    if isinstance(push_content, int) and push_content == 1:
        push_content_str = data["Data"].get("PushContent")  # 假设 PushContentStr 是消息内容的键
        if push_content_str and " : " in push_content_str:
            sender, message = push_content_str.split(" : ", 1)
            print(f"发送者: {sender}")
            print(f"发送内容: {message}")
        else:
            print("Error: Invalid format for 'PushContentStr'.")
    else:
        print("Error: 'PushContent' is not equal to 1 or is not an integer.")