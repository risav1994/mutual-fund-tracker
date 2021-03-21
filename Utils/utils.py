def serialize(result_instance, reqd_cols):
    _serialize = {}
    for idx, col in enumerate(reqd_cols):
        _serialize[col.name] = result_instance[idx]
    return _serialize


def db_commit(db_session, instance):
    db_session.execute(instance)
    db_session.commit()
    db_session.close()
    db_session.remove()
