from abc import ABC, abstractmethod, abstractproperty


class Config:
    MY_TOKEN = ''
    API_DISCORD = 'https://discord.com/api/v9'
    TARGETS = {
        'IVAN':      '762631268805902338', 
        'SEMEN':     '687394809702645778', 
        'ME':        '275216402258984962', 
        'Mysonya':   '706458826685022258', 
        'ebrayshin': '388405374044078083', 
        'Pihva':     '278495383506780160', 
        'stoyak':    '271196329009479681',
        'minimapa':  '294200733539237888'
    }
    CHANNELS = {
        'pingme':       '939299932798603300',
        'kvadrat':      '939299932798603299',
        'zapreschenka': '939300973304758372',
        'privat':       '939598269959536701'
    }
    ID_SERVER = '939299932324634625'
    

class DiscordConfig(ABC):
    @abstractmethod
    def get_server_url(self, id_server):
        pass
        # return f'https://discord.com/api/v9/guilds/{id_server}/members/'

    @abstractmethod
    def get_channel_url(self, id_channel):
        return f'https://discord.com/api/v9/channels/{id_channel}/messages'

    @abstractmethod
    def get_message_url(self, id_channel, message_id):
        return f'https://discord.com/api/v9/channels/{id_channel}/messages/{message_id}'


class UserConfig(DiscordConfig):
    def __init__(self, token, id_server, channels, targets):
        self.token = token
        self.id_server = id_server
        self.channels = channels
        self.targets = targets

    def __repr__(self):
        return f'<User {self.token}>'

    def get_server_url(self):
        url = super().get_server_url(self.id_server)
        return url
    
    def get_channel_url(self, channel):
        url = super().get_channel_url(channel)
        return url

    def get_message_url(self, channel, message_id):
        url = super().get_message_url(channel, message_id)
        return url


if __name__ == '__main__':
    user = UserConfig(1, 2, 3, 4)
    req = user.get_server_url()

    print(req)
