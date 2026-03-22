import bcrypt
class HashPassword:
    def create_hash(self, password : str) -> str:
        pwd_byte = password.encode("utf-8")
        hashed = bcrypt.hashpw( pwd_byte, bcrypt.gensalt() )
        pwd = hashed.decode("utf-8")
        print("저장할 pwd : ", pwd)
        return pwd
    
    def verify_hash(self, imput_pwd:str, db_pwd: str) -> bool:
        return bcrypt.checkpw(imput_pwd.encode("utf-8"), db_pwd.encode("utf-8"))