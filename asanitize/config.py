import os
import json
from dataclasses import dataclass, field

@dataclass
class DiscordConfig(object):
    token: str = ''
    channel: list[str] = field(default_factory=list)

    def save_config(self, filename):
        config = {
            'token': self.token,
            'channel': self.channel,
        }

        file = open(filename, 'w')
        json.dump(config, file, indent=4)
        file.close()

    def set_config(self, filename, token, channel):
        self.token = token
        self.channel = channel
        self.save_config(filename)

    def load_config(self, filename):
        if not os.path.exists(filename):
            open(filename, 'w').close()
        
        file = open(filename, 'r')
        data = json.load(file)

        self.token = data.get('token')
        self.channel = data.get('channel')
        file.close()
    
    def get_config(self, filename):
        self.load_config(filename)
        return { 'token': self.token, 'channel': self.channel }