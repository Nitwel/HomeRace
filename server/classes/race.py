class Race:

    def __init__(self, name: str, adminSessionId: str, lapsToFinish: int):
        self.name = name
        self.players = []
        self.adminSessionId = adminSessionId
        self.carts
        self.lapsToFinish = lapsToFinish
        self.starting = False
        self.started = False
        self.finished = False
