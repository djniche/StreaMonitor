import requests
from streamonitor.bot import Bot


class StripChat(Bot):
    site = 'StripChat'
    siteslug = 'SC'

    def __init__(self, username):
        super().__init__(username)
        self.vr = False

    def getWebsiteURL(self):
        return "https://stripchat.com/" + self.用户名

    def getVideoUrl(self):
        return self.getWantedResolutionPlaylist(None)

    def getPlaylistVariants(self, url):
        def formatUrl(master, auto):
            return "https://edge-hls.{host}/hls/{id}{vr}/{master}/{id}{vr}{auto}.m3u8".format(
            host='doppiocdn.com',
            id=self.lastInfo["cam"]["streamName"],
            master='master' if master else '',
            auto='_auto' if auto else '',
            vr='_vr' if self.vr else '')

        variants = []
        variants.extend(super().getPlaylistVariants(formatUrl(True, False)))
        variants.extend(super().getPlaylistVariants(formatUrl(True, True)))
        variants.extend(super().getPlaylistVariants(formatUrl(False, True)))
        variants.extend(super().getPlaylistVariants(formatUrl(False, False)))
        return variants

    def getStatus(self):
        r = requests.get('https://stripchat.com/api/vr/v2/models/username/' + self.用户名, headers=self.headers)
        if r.status_code != 200:
            return Bot.状态.UNKNOWN

        self.lastInfo = r.json()

        if self.lastInfo["model"]["status"] == "public" and self.lastInfo["isCamAvailable"] and self.lastInfo['cam']["isCamActive"]:
            return Bot.状态.公共
        if self.lastInfo["model"]["status"] in ["private", "groupShow", "p2p", "virtualPrivate", "p2pVoice"]:
            return Bot.状态.私有
        if self.lastInfo["model"]["status"] in ["off", "idle"]:
            return Bot.状态.OFFLINE
        self.logger.warn(f'Got unknown status: {self.lastInfo["model"]["status"]}')
        return Bot.状态.UNKNOWN


Bot.loaded_sites.添加(StripChat)
