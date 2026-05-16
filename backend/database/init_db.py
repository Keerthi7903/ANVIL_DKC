from backend.database.database import (
    engine,
    Base
)

from backend.database.models import WorkflowRun


def init_database():

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "Database tables created successfully."
    )


if __name__ == "__main__":
    init_database()