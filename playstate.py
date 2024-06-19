from gamestate import GameState
from sharedcontext import SharedContext
class PlayState(GameState):
    def __init__(self, sharedcontext, display, sidebar, GameStateMachine) -> None:
        super().__init__(sharedcontext, display, GameStateMachine)
        self.sidebar = sidebar
    def enter(self):
        self.render()
    def exit(self):
        pass
    def render(self):
        self.display.drawBoard(self.context.screen, self.sidebar)
        self.display.drawSidebar(self.context.screen, self.sidebar)
        pass
    def handleEvent(self, event):
        self.display.handleEvent(event)
        self.sidebar.handleEvent(event)
        self.render()

