from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool


class DB(object):
    """mysqldb"""

    def __init__(self, config):
        self.db_config = config
        self.session = None

    def get_session(self):
        if not self.session:
            engine = create_engine(
                self.db_config,
                isolation_level="READ UNCOMMITTED",
                poolclass=NullPool
            )
            Session = scoped_session(sessionmaker(bind=engine))
            self.session = Session

        return self.session
