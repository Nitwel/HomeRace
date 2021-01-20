class Player(Player):

    def __init__(self, ssid: str, name: str, selectedCart: str):
        self.ssid = ssid
        self.name = name
        self.selectedCart = selectedCart
        self.laps = 0
        self.times = []
        self.ready = False