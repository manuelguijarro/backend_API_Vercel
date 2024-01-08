from fastapi import APIRouter,HTTPException

from db.models.user import User
from db.client import db_users_client
from db.schemas.user import user_schema,users_schema
from bson import ObjectId
from functions.utils import search_user,get_user_object
router = APIRouter(
  prefix="/users",
  tags=["users"]
)

@router.get("/", response_model=list[User])
async def get_users():
  try:
    users = db_users_client.user.find()
    return users_schema(users)
  except:
    raise HTTPException(status_code=404, detail="no users found")

@router.get("/{id}", response_model=User)
async def get_user(id : str):
  try:
    return search_user("_id", ObjectId(id))
  except:
    raise HTTPException(status_code=404, detail="user not found")
  

@router.post("/", response_model=User, status_code=201)
async def create_user(user : User):
  if type(search_user("email", user.email)) == User:
    raise HTTPException(status_code=406, detail="user already exists")
  try:
    user_dict = dict(user)
    del user_dict['id']
    #primero lo guardo en la base de datos y obtengo el id despues.
    id = db_users_client.user.insert_one(user_dict).inserted_id
    new_user = user_schema(db_users_client.user.find_one({"_id": id}))
    return User(**new_user)#y devolvemos el nuevo usuario creado
  except:
    raise HTTPException(status_code=400, detail="error creating user")
  
@router.put("/{username}", response_model=User)
async def update_user(username : str, user : User):
  if type(search_user("username", username)) == User:
    try:
      user_dict = dict(user)
      del user_dict['id']
      db_users_client.user.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
      return search_user("_id", ObjectId(user.id))
    except:
      raise HTTPException(status_code=404, detail="user not found")
    
@router.delete("/{id}")
async def delete_user(id : str):
  try:
    user_obj = get_user_object("_id", ObjectId(id))
    db_users_client.user.find_one_and_delete({"_id": ObjectId(id)})
    return {"message": "user deleted", "user": user_obj}
  except:
    raise HTTPException(status_code=404, detail="user not found")