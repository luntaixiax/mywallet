import uuid

def id_generator(prefix: str, existing_list: list = None):
    new_id = prefix + str(uuid.uuid4())[:8]
    if existing_list:
        if new_id in existing_list:
            new_id = id_generator(prefix, existing_list)
    return new_id