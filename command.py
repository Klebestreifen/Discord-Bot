""" Command-Infrastructure

This module contains the [Command] class and provides the
command-infrastructure.
"""

from misc import log
from main_singleton import Main

class Command:
    """ Discordd-Bot-Command

    This class represents a command which was registered with the decorator
    factory.
    See [Command.register(cmd_name, permission)].

    This class also represents the backend for all command functionality.
    """

    commands = []

    @staticmethod
    def register(cmd_name, permission):
        """ Decortaor-Factory to register new discord command

        Decortaor-Factory to create the real decorator with paramethers.

        Returns the decorator.
        
        See [Command.register(cmd_name, permission) => command(cmd_func)]
        """

        def command(cmd_func):
            """ Real decorator to register new commands """

            log(f"Register command {cmd_name}")
            Command.commands.append(Command(cmd_func, cmd_name, permission))

            # Reminder: The return value overwrites the actual defined value.
            return cmd_func

        command.__doc__ += "\n\n"
        command.__doc__ += f"cmd_name   := {cmd_name}\n"
        command.__doc__ += f"permission := {permission}\n"

        return command

    @staticmethod
    def has_user_permission(user, permission):
        """ Is <permission> "in" <user.roles> ?
        
        If the user has a role in which the permission was stored in the
        config, then this returns <True>. Otherwise <False>.
        """

        try:
            return permission in Command.get_permission_from_roles(user.roles)
        except AttributeError:
            return False

    @staticmethod
    def get_permission_from_roles(roles):
        """ Returns a list of all permissions of the specified roles. """

        permissions = []
        
        for _r in roles:
            # Concat lists
            permissions += Command.get_role_permissions(_r.id)

        # Remove dublicats
        permissions = list(dict.fromkeys(permissions))
        
        return permissions

    @staticmethod
    def get_role_permissions(rid):
        """ Returns a list with the permissions of a single role. """
        permissions = []
        try:
            for tag in Main.i().config["tags"][str(rid)]:
                permissions.append(tag.strip().lower())
        except KeyError:
            pass
        return permissions

    def __init__(self, func, name, permission):
        self.func = func
        self.name = name.lower()
        self.permission = permission.lower()

    async def execute(self, msg):
        """ Executes the command.

        Called by [Bot.on_message(self, msg) => execute(msg)].
        """
        if Command.has_user_permission(msg.author, self.permission):
            await self.func(msg)
        else:
            await msg.channel.send("Du hast da keinen Zugriff drauf. Wenn das unerwartet kommt, dann melde dich bei Klebi!")

###########################################################################################

