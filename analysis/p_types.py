from dataclasses import dataclass


@dataclass
class PointType:
    entry_exit: str = ""
    mouse_key: str = ""

    def __str__(self):
        return f"{self.mouse_key} {self.entry_exit}"


class EntryOrExitOrNormal(PointType):
    pass


class EntryOrExit(EntryOrExitOrNormal):
    pass


ENTRY_OR_EXIT = EntryOrExit()


class Exit(EntryOrExit):
    entry_exit = "Exit"


EXIT = Exit()


class Entry(EntryOrExit):
    entry_exit = "Entry"


ENTRY = Entry()


class NonEntryExit(EntryOrExitOrNormal):
    entry_exit = "Intermediate"


NOT_ENTRY_EXIT = NonEntryExit()


# ----------------------------------------------------------------
class KeyOrMouse(PointType):
    pass


KEY_OR_MOUSE = KeyOrMouse()


class Mouse(KeyOrMouse):
    mouse_key = "Mouse"


MOUSE = Mouse()


class Key(KeyOrMouse):
    mouse_key = "Key"


KEY = Key()
