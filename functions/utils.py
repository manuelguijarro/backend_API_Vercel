from bson import ObjectId
from ..db.models.user import User
from ..db.client import db_users_client
from ..db.schemas.user import user_schema,users_schema


def search_user(key: str, value: str | ObjectId):
  try:
    user = db_users_client.user.find_one({key: value})
    return User(**user_schema(user))
  except:
    return {"error": "user not found"}
  
def get_user_object(key: str, value: str | ObjectId):
  try:
    user = db_users_client.user.find_one({key: value})
    return User(**user_schema(user))
  except:
    return {"error": "user not found"}