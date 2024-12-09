from typing import Type

from pydantic import BaseModel

from db.base_model import BaseSqlModel
from utils.model import to_dict


def from_sql_model(source: BaseSqlModel, target: Type[BaseModel]) -> BaseModel:
    # Convert the sql model to the Pydantic schema
    return target(**to_dict(source))
