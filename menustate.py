from gamestate import GameState
class MenuState(GameState):
    def __init__(self, sharedcontext, display, GameStateMachine):
        super().__init__(sharedcontext, display, GameStateMachine)
    def enter(self):
        self.render()
    def exit(self):
        pass
    def render(self):
        self.display.draw(self.context.screen)
    def handleEvent(self, event): pass

