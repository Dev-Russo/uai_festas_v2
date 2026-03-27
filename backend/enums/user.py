from enums import Enum

class UserRole(str, Enum):
    producer = "producer"
    consumer = "consumer"
    admin = "admin"