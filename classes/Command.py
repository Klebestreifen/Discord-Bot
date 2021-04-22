from util import config

class Command:
    """
        Command registry
    """
    commands = []

    @staticmethod
    def register(cmd_name, permission):
        def command(cmd_func):
            Command.commands.append(Command(cmd_func, cmd_name, permission))
            return cmd_func
        return command

    @staticmethod
    def has_user_permission(user, permission):
        # is permission in user.roles ?
        try:
            return permission in Command.get_permission_from_roles(user.roles)
        except AttributeError:
            return False

    @staticmethod
    def get_permission_from_roles(roles):
        permissions = []
        
        for r in roles:
            # concat lists
            permissions += Command.get_group_permissions(r.id)

        # remove dublicats
        permissions = list(dict.fromkeys(permissions))
        
        return permissions

    @staticmethod
    def get_group_permissions(id):
        permissions = []
        try:
            for tag in config["tags"][str(id)]:
                permissions.append(tag.strip().lower())
        except KeyError:
            pass
        return permissions

    def __init__(self, func, name, permission):
        self.func = func
        self.name = name.lower()
        self.permission = permission.lower()

    async def execute(self, msg):
        if Command.has_user_permission(msg.author, self.permission):
            await self.func(msg)
        else:
            await msg.channel.send("Du hast da keinen Zugriff drauf. Wenn das unerwartet kommt, dann melde dich bei Klebi!")
