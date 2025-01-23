class MessageGroupProcessor:
    def __init__(self, client, app_id):
        self.client = client
        self.app_id = app_id
        self.self_profile = client._personal_api.get_profile(app_id)