from src.entities.entity import Session
def check_range(value, upper_bound, lower_bound):
    if upper_bound < value or value < lower_bound:
        raise ValueError("Value is not in range.")

def check_required(posted_item, required_attributes):
    for attr in required_attributes:
        if attr not in posted_item:
            raise AttributeError(f'Attribute "{attr}" is required.')

def check_duplicate(entity, attribute, value):
    session = Session()
    # Check if value already exists
    if (
            session.query(entity)
                    .filter(getattr(entity, attribute) == value)
                    .first()
            is not None
    ):
        session.close()
        raise NameError
    session.close()

def check_existence(entity, attribute, value):
    session = Session()
    # Check if food category id is valid
    if (
            session.query(entity)
                    .filter(getattr(entity, attribute) == value)
                    .first()
            is None
    ):
        session.close()
        raise KeyError
    session.close()

def update_attribute(item, attribute, new_value_dict):
    if attribute in new_value_dict:
        setattr(item, attribute, new_value_dict[attribute])
