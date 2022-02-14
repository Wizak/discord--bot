from config import UserConfig, Config

import time
import requests


class Driver:
    def __init__(self, user):
        self.__user = user
        self.clock = 3
        self.__header = {
            'authorization': self.__user.token,
            'content-type': 'application/json'
        }
        self.session = requests.Session()


    def __patch(self, action, target, channel=None):
        url = self.__user.get_server_url() + target
        match action:
            case 'mute':
                data = {'mute': True}
            case 'kick':
                data = {'channel_id': channel}
        resp = self.session.patch(url, json=data, headers=self.__header)
        return resp

    def __post(self, target, channel):
        url = self.__user.get_channel_url(channel)
        data = {'content': f'<@!{target}>'}
        resp = self.session.post(url, json=data, headers=self.__header)
        return resp

    # def __get(self, target, channel=None):
    #     url = self.__user.get_server_url() + target
    #     resp = self.session.patch(url, json=data, headers=self.__header)
    #     return resp

    # def __delete(self, target, channel=None):
    #     url = self.__user.get_message_url(channel, message_id) + target
    #     data = {'channel_id': channel}
    #     resp = self.session.patch(url, json=data, headers=self.__header)
    #     return resp

    def _process(self, method, **kwargs):
        while True:
            response = None
            match method:
                # case 'get':
                #     response = self.session.get(url, headers=self.header)
                case 'post':
                    response = self.__post(kwargs['target'], kwargs['channel'])
                case 'patch':
                    response = self.__patch(kwargs['action'], kwargs['target'])
                # case 'delete':
                #     response = self.session.delete(url, headers=self.header)
            if kwargs['log']:
                print(response.json())
            time.sleep(self.clock)


class Bot(Driver):
    def __init__(self, user, log=True):
        self.__user = user
        Driver.__init__(self, user)
        self.log = log
        self.targets = self.__user.targets
        self.channels = self.__user.channels 

    def kick(self, target, channel=None):
        if channel is not None:
            channel = self.channels[channel]
        target = self.targets[target]
        Driver._process(self, action='kick', method='patch', target=target, channel=channel, log=self.log)

    def mute(self, target):
        target = self.targets[target]
        Driver._process(self, action='mute', method='patch', target=target, log=self.log)

    def spam(self, target, channel):
        channel = self.channels[channel]
        target = self.targets[target]
        Driver._process(self, action='spam', method='post', target=target, channel=channel, log=self.log)

    def clear(self, channel, limit=None):
        channel = self.channels[channel]
        Driver._process(self, action='clear', method='delete', channel=channel, limit=limit, log=self.log)


if __name__ == '__main__':
    token = Config.MY_TOKEN
    server =  Config.ID_SERVER
    channels = Config.CHANNELS
    targets = Config.TARGETS

    user = UserConfig(token, server, channels, targets)
    bot = Bot(user)

    bot.spam('ME', 'privat')