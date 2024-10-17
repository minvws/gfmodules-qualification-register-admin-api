from gfmodules_python_shared.schema.sql_model import SQLModelBase
from .container import get_engine
from .fastapi_application import application_init

if __name__ == "__main__":
    application_init()
    SQLModelBase.metadata.create_all(get_engine())
