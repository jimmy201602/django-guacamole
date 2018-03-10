

class GuacamoleClientInformation(object):
    def __init__(self):
        self._optimalScreenWidth = 1024
        self._optimalScreenHeight = 768
        self._optimalScreenResolution = 96
        self._audioMimetypes = []
        self._videoMimetypes = []
        self._imageMimetypes = []

    @property
    def optimalScreenWidth(self):
        return self._optimalScreenWidth

    @optimalScreenWidth.setter
    def optimalScreenWidth(self, value):
        self._optimalScreenWidth = value

    @property
    def optimalScreenHeight(self):
        return self._optimalScreenHeight

    @optimalScreenHeight.setter
    def optimalScreenHeight(self, value):
        self._optimalScreenHeight = value

    @property
    def optimalScreenResolution(self):
        return self._optimalScreenResolution

    @optimalScreenResolution.setter
    def optimalScreenResolution(self, value):
        self._optimalScreenResolution = value

    @property
    def audioMimetypes(self):
        return self._audioMimetypes

    @audioMimetypes.setter
    def audioMimetypes(self, value):
        self._audioMimetypes = value

    @property
    def videoMimetypes(self):
        return self._videoMimetypes

    @videoMimetypes.setter
    def videoMimetypes(self, value):
        self._videoMimetypes = value

    @property
    def imageMimetypes(self):
        return self._imageMimetypes

    @imageMimetypes.setter
    def imageMimetypes(self, value):
        self._imageMimetypes = value


