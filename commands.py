import constants as c

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

class SpaceCommand:
    def execute(self, actor, action):
        actor.user_input(action)