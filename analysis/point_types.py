from typing import Type


class _ExitOrEntryTypeBase:
    pass


class ExitType(_ExitOrEntryTypeBase):
    pass


class EntryType(_ExitOrEntryTypeBase):
    pass


ENTRY_OR_EXIT_TYPE = Type[_ExitOrEntryTypeBase]
