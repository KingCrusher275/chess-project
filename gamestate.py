class GameState:
    def __init__(self, sharedcontext, display, GameStateMachine):
        self.context = sharedcontext
        self.display = display
        self.GameStateMachine = GameStateMachine
    def enter(self): pass
    def exit(self): pass
    def render(self): pass
    def handleEvent(self, event): pass




