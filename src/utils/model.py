from db.base_model import BaseSqlModel


def to_dict(model: BaseSqlModel) -> dict:
    # Convert the SQL model to the simple python dictionary
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}
