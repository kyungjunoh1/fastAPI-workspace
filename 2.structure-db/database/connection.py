from sqlmodel import SQLModel, Session, create_engine

database_file = "my-test.db" #sqlite 저장 될 파일(db 파일명)
database_connection_string = f"sqlite:///{database_file}" #데이터베이스 위치 지정

#다중 요청 시 처리
connect_args = {"check_same_thread":False}

engine_url = create_engine( database_connection_string,echo=True,
                                            connect_args=connect_args)
def conn():
    SQLModel.metadata.create_all(engine_url)
def get_session():
    with Session(engine_url) as session:
        yield session