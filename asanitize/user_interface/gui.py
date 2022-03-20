import wx
import wx.xrc
import wx.dataview

from asanitize.services.discord.api.client import Client
from asanitize.config import DiscordConfig

class MainFrame(wx.Frame):
    client = None
    discord_config = DiscordConfig()
    guilds = []
    direct_message_channels = []

    def _get_channel_to_sanitize(self):
        channel_to_sanitize = []
        checked_items = self.m_checkList1.GetCheckedStrings()
        for checked_item in checked_items:
            id = checked_item[checked_item.find('(') + 1: checked_item.find(')')]
            channel_to_sanitize.append(id)

        return channel_to_sanitize

    def __init__(self, parent):
        self.config = self.discord_config.get_config('./discord_config.json')

        wx.Frame.__init__ (self, parent, id=wx.ID_ANY, title=u"Asanitize", pos=wx.DefaultPosition, size=wx.Size(507, 265), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, self.config.get('token'), wx.DefaultPosition, wx.Size( 350, -1 ), 0)
        fgSizer1.Add(self.m_textCtrl2, 0, wx.ALL, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"Authenticate", wx.DefaultPosition, wx.Size(120, -1), 0)
        self.m_button2.Bind(wx.EVT_BUTTON, self._onButton2Clicked)
        fgSizer1.Add(self.m_button2, 0, wx.ALL, 5)

        self.m_checkList1Choices = []
        self.m_checkList1 = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(350, 150), self.m_checkList1Choices, 0)
        self.m_checkList1.Bind(wx.EVT_CHECKLISTBOX, self._onCheckListCheckedUnchecked)
        
        
        fgSizer1.Add(self.m_checkList1, 0, wx.ALL, 5)

        self.m_dataViewListCtrl1 = wx.dataview.DataViewListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(120, 150), 0)
        fgSizer1.Add(self.m_dataViewListCtrl1, 0, wx.ALL, 5)

        self.m_gauge1 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(350, 23), wx.GA_HORIZONTAL )
        self.m_gauge1.SetValue(0) 
        fgSizer1.Add(self.m_gauge1, 0, wx.ALL, 5)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"Sanitize", wx.DefaultPosition, wx.Size(120, -1), 0)
        self.m_button3.Bind(wx.EVT_BUTTON, self._onButton3Clicked)
        fgSizer1.Add(self.m_button3, 0, wx.ALL, 5)

        self.SetSizer(fgSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
 
    def _onButton2Clicked(self, event):
        token = self.m_textCtrl2.GetValue()
        self.client = Client(token)

        self.guilds = self.client.get_guilds()
        for guild in self.guilds.channels:
            self.m_checkList1.Append('({}) {}'.format(guild.id, guild.name))

        self.direct_message_channels = self.client.get_direct_message_channels()
        for direct_message_channel in self.direct_message_channels.channels:
            recipients = ', '.join(['{}#{}'.format(recipient.username, recipient.discriminator) for recipient in direct_message_channel.recipients])
            self.m_checkList1.Append('({}) Direct Message with {}'.format(direct_message_channel.id, recipients))

        index_to_check = []
        for index, checked_string in enumerate(self.m_checkList1.GetStrings()):
            id = checked_string[checked_string.find('(') + 1: checked_string.find(')')]

            for channel in self.config.get('channel'):
                if channel == id:
                    index_to_check.append(index)
        
        self.m_checkList1.SetChecked(index_to_check)
                    
        self.discord_config.set_config('./discord_config.json', self.m_textCtrl2.GetValue(), self._get_channel_to_sanitize())

    def _onButton3Clicked(self, event):
        author_id = self.client.get_my_info().id

        for channel_id in self._get_channel_to_sanitize():
            for guild in self.guilds.channels:
                if guild.id == channel_id:
                    guild.sanitize(author_id, False)
            
            for direct_message_channel in self.direct_message_channels.channels:
                if direct_message_channel.id == id:
                    direct_message_channel.sanitize(author_id, False)

    def _onCheckListCheckedUnchecked(self, event):
        self.discord_config.set_config('./discord_config.json', self.m_textCtrl2.GetValue(), self._get_channel_to_sanitize())

    def __del__(self):
        pass
	

def start_app():
    app = wx.App()
    frm = MainFrame(None)
    frm.Show()
    app.MainLoop()