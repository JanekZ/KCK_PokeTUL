import constants as c
"""
COMMANDS:
    Classes that represent key press actions with execute method.
EXECUTE:
    Class method that calls game state function to process user input.
    
    :param actor: Game state object used for access to its methods.
    :param action: Text variable that represents what type of action has to be executed.
"""
class UpCommand:
    def execute(self, actor, action):
        actor.user_input(action, c.UP)

class LeftCommand:
    def execute(self, actor, action):
        actor.user_input(action, c.LEFT)

class RightCommand:
    def execute(self, actor, action):
        actor.user_input(action, c.RIGHT)

class DownCommand:
    def execute(self, actor, action):
        actor.user_input(action, c.DOWN)