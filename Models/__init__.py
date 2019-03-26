from .History import History
from .createEngine import engine, Session


# create tables
History.metadata.create_all(engine)
