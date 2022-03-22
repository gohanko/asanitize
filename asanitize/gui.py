import wx
import wx.xrc
import wx.dataview

from asanitize.services.discord.client import Client
from asanitize.config import ConfigurationManager


class MainFrame(wx.Frame):
    client = None
    config_manager = ConfigurationManager()
    guilds = []
    direct_message_channels = []

    def __init__(self, parent):
        self.config = self.config_manager.get_service_config('discord')

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Asanitize", pos=wx.DefaultPosition, size=wx.Size(507, 265), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.authentication_token_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, self.config.token, wx.DefaultPosition, wx.Size( 350, -1 ), 0)
        self.authentication_token_text_ctrl.SetHint('Set Discord authentication token here...')
        fgSizer1.Add(self.authentication_token_text_ctrl, 0, wx.ALL, 5)

        self.authenticate_button = wx.Button(self, wx.ID_ANY, u"Authenticate", wx.DefaultPosition, wx.Size(120, -1), 0)
        self.authenticate_button.Bind(wx.EVT_BUTTON, self._on_authenticate_button_clicked)
        fgSizer1.Add(self.authenticate_button, 0, wx.ALL, 5)

        self.server_list = []
        self.server_check_list = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(350, 150), self.server_list, 0)
        self.server_check_list.Bind(wx.EVT_CHECKLISTBOX, self._on_server_check_list_check_uncheck)
        fgSizer1.Add(self.server_check_list, 0, wx.ALL, 5)

        self.current_user_view_list = wx.dataview.DataViewListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(120, 150), 0)
        fgSizer1.Add(self.current_user_view_list, 0, wx.ALL, 5)

        self.progress_gauge = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(350, 23), wx.GA_HORIZONTAL )
        self.progress_gauge.SetValue(0) 
        fgSizer1.Add(self.progress_gauge, 0, wx.ALL, 5)

        self.sanitize_button = wx.Button(self, wx.ID_ANY, u"Sanitize", wx.DefaultPosition, wx.Size(120, -1), 0)
        self.sanitize_button.Bind(wx.EVT_BUTTON, self._on_sanitize_button_clicked)
        fgSizer1.Add(self.sanitize_button, 0, wx.ALL, 5)

        self.SetSizer(fgSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
        
    def _get_channel_to_sanitize(self):
        channel_to_sanitize = []
        checked_items = self.server_check_list.GetCheckedStrings()
        for checked_item in checked_items:
            id = checked_item[checked_item.find('(') + 1: checked_item.find(')')]
            channel_to_sanitize.append(id)

        return channel_to_sanitize
    def _on_authenticate_button_clicked(self, event):
        token = self.authentication_token_text_ctrl.GetValue()
        self.progress_gauge.SetValue(25)
        self.client = Client(token)
        self.client.get_my_info()

        self.guilds = self.client.get_guilds()
        for index, guild in enumerate(self.guilds.channels):
            self.progress_gauge.SetValue((index / len(self.guilds.channels) * 50))
            self.server_check_list.Append('({}) {}'.format(guild.id, guild.name))

        self.direct_message_channels = self.client.get_direct_message_channels()
        for index, direct_message_channel in enumerate(self.direct_message_channels.channels):
            self.progress_gauge.SetValue((index / len(self.direct_message_channels.channels) * 75))
            recipients = ', '.join(['{}#{}'.format(recipient.username, recipient.discriminator) for recipient in direct_message_channel.recipients])
            self.server_check_list.Append('({}) Direct Message with {}'.format(direct_message_channel.id, recipients))

        index_to_check = []
        check_list_items = self.server_check_list.GetStrings()
        for index, checked_string in enumerate(check_list_items):
            id = checked_string[checked_string.find('(') + 1: checked_string.find(')')]

            for channel in self.config.channels_to_sanitize:
                if channel == id:
                    index_to_check.append(index)

            self.progress_gauge.SetValue((index / len(check_list_items) * 120))
        
        self.server_check_list.SetCheckedItems(index_to_check)
        self.config_manager.set_service_config('discord', token=self.authentication_token_text_ctrl.GetValue(), channels_to_sanitize=self._get_channel_to_sanitize())

    def _on_sanitize_button_clicked(self, event):
        self.progress_gauge.SetValue(0)
        author_id = self.client.current_user_info.id

        channels_to_sanitize = self._get_channel_to_sanitize()
        for index, channel_id in enumerate(channels_to_sanitize):
            for guild in self.guilds.channels:
                if guild.id == channel_id:
                    guild.sanitize(author_id, False)
            
            for direct_message_channel in self.direct_message_channels.channels:
                if direct_message_channel.id == id:
                    direct_message_channel.sanitize(author_id, False)
    
            self.progress_gauge.SetValue((index / len(channels_to_sanitize) * 100))

        self.progress_gauge.SetValue(100)

    def _on_server_check_list_check_uncheck(self, event):
        self.config_manager.set_service_config('discord', token=self.authentication_token_text_ctrl.GetValue(), channels_to_sanitize=self._get_channel_to_sanitize())


def start_app():
    app = wx.App()
    frm = MainFrame(None)
    frm.Show()
    app.MainLoop()