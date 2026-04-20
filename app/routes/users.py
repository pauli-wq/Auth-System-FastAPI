from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_pass_hash
from app.database.database import get_db
from app.models.user import User as UserModel
from app.routes.auth import get_current_active_user
from app.schemas.user import User, UserCreate, UserUpdate
from app.schemas.user import User as UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


# obtener informacion del usuario autenticado
@router.get("/profile", response_model=UserResponse)
async def read_user_profile(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return current_user


# crear nuevo usuario
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # verifica si el email ya existe
    db_user_email = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email alredy registered")

    # verifica si el username ya existe
    db_username = (
        db.query(UserModel).filter(UserModel.username == user.username).first()
    )
    if db_username:
        raise HTTPException(status_code=400, detail="Username alredy existed")

    # creamos usuario con password hasheado
    hashed_password = get_pass_hash(user.password)
    db_user = UserModel(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# obtener lista de usuarios (require estar autenticado)
@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users


# obtener usuario por ID
@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# actualizar usuario (propio usuario o admin)
@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verificar permisos (solo editar el propio perfil o ser admin)
    if str(current_user.id) != user_id and not bool(current_user.is_superuser):
        raise HTTPException(
            status_code=403, detail="Not authorized to update this user"
        )

    # Actualizar campos
    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_pass_hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# borrar usuario (el propio usuario o admin)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verificar permisos
    if int(current_user.id) != int(user_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this user"
        )
    db.delete(db_user)
    db.commit()
    return None
