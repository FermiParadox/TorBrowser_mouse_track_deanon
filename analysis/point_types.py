from dataclasses import dataclass


@dataclass
class EntryExitType:
    str: str

    def __repr__(self):
        return self.str


EXIT_TYPE = EntryExitType('EXIT')

ENTRY_TYPE = EntryExitType('ENTRY')

NON_CRIT_TYPE = EntryExitType('NORMAL')
