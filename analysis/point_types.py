from dataclasses import dataclass


@dataclass
class EntryOrExitType:
    str: str

    def __repr__(self):
        return self.str


EXIT_TYPE = EntryOrExitType('EXIT')

ENTRY_TYPE = EntryOrExitType('ENTRY')

NON_CRIT_TYPE = EntryOrExitType('NORMAL')
