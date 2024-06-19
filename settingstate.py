from gamestate import GameState
class SettingState(GameState):
    def enter(self):
        self.render()
        pass
    def exit(self):
        pass
    def render(self):
        pass
    def handleEvent(self, event): pass

