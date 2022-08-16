from figmapy.session import current


class FigmaPyBase:
    def __init__(self, token, oauth2=False):
        current.figma_session = self
        self.api_uri = 'https://api.figma.com/v1/'
        self.token_uri = 'https://www.figma.com/oauth'
        self.api_token = token
        self.oauth2 = oauth2