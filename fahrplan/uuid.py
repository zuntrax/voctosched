import uuid as _uuid

UUID_NAMESPACE = _uuid.UUID('54dc9c85-9b6a-40bd-9a36-41c004a5829b')


def uuid(uid, name):
    # media.ccc.de uses these uuids to identify talks in the backend
    # UUID_NAMESPACE makes sure no collisions with other tools occur
    return str(_uuid.uuid5(UUID_NAMESPACE, f"{name}{uid}"))
