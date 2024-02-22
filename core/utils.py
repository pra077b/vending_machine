from core.db import DbSession


def get_db():
    """
    A context manager for providing the db session
    @rtype: object
    """
    db = DbSession()
    try:
        yield db
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()
