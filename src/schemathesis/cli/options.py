from enum import Enum
from typing import List, Optional, Type, Union

import click


class CSVOption(click.Choice):
    def __init__(self, choices: Type[Enum]):
        self.enum = choices
        super().__init__(tuple(choices.__members__))

    def convert(
        self, value: str, param: Optional[click.core.Parameter], ctx: Optional[click.core.Context]
    ) -> List[Enum]:
        items = [item for item in value.split(",") if item]
        invalid_options = set(items) - set(self.choices)
        if not invalid_options and items:
            return [self.enum[item] for item in items]
        # Sort to keep the error output consistent with the passed values
        sorted_options = ", ".join(sorted(invalid_options, key=items.index))
        available_options = ", ".join(self.choices)
        self.fail(f"invalid choice(s): {sorted_options}. Choose from {available_options}")


class NotSet:
    pass


not_set = NotSet()


class OptionalInt(click.types.IntRange):
    def convert(  # type: ignore
        self, value: str, param: Optional[click.core.Parameter], ctx: Optional[click.core.Context]
    ) -> Union[int, NotSet]:
        if value == "None":
            return not_set
        try:
            int(value)
            return super().convert(value, param, ctx)
        except (ValueError, UnicodeError):
            self.fail("%s is not a valid integer or None" % value, param, ctx)
