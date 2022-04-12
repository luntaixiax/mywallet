from enum import Enum

class AcctType(Enum):
    ASSET = 0
    LIABILITY = 1

class EntryType(Enum):
    DEBIT = 0
    CREDIT = 1

class CategType(Enum):
    INCOME = 0
    EXPENSE = 1
