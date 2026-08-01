from fastapi import Depends , HTTPException , status
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from users.models import User_model, User_type
from core.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import jwt
from core.config import settings
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidSignatureError, ImmatureSignatureError



# 401: not athrizied , 403:authrized but dont access. set auto_error to change 403 to 401  
# in new version fastapi return 401 in default. but set auto_error=False to handle msg better.
security = HTTPBearer(scheme_name='token', auto_error=False)

# -- Dependency <user> --
def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db:Session = Depends(get_db)  ) :
    
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Authorization failed: Token missing'
        )
        
    token = credentials.credentials
    try:
        decoded = jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=['HS256'], leeway=30)
        user_id = decoded.get("user_id")
        if not user_id :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization  failed , userid not found in payload')
        if decoded.get('type')!='access' :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization  failed , token type not valid')
        '''
        # do not need. hwt check it automatically:
        if datetime.now() > datetime.fromtimestamp(decoded.get("exp")) :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization  failed , token expired')
        '''
        user_obj = db.query(User_model).filter_by(id=user_id).first()
        # user_id is in token and valid but maybe user deleted from database
        if not user_obj:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Authorization failed: User not found in database'
            )
        return user_obj  
        
    except ExpiredSignatureError :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorize failed : token has expire')
    except ImmatureSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed: token is not yet valid")
    except DecodeError :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorize failed : decode failed')
    except Exception as e  :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Authorize failed : {e}')


# -- Dependency <admin> --
def get_authenticated_admin(user:User_model = Depends(get_authenticated_user)):
    if user.user_type == User_type.ADMIN:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden access to endpoint",
    )



# -- generate token --
def generate_access_token(user_id: int, expires_in: int = 60*5) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
        "type":'access'
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


# -- refresh token --
def generate_refresh_token(user_id: int, expires_in: int = 3600*24) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
        "type":'refresh'
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


# -- decode refresh token -- 
def decode_refresh_token(token) :
    try:
        decoded = jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=['HS256'], leeway=30)
        user_id = decoded.get("user_id")
        if not user_id :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authorized failed , userid not found in payload')
        if decoded.get('type')!='refresh' :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authorized failed , token type not valid')
        
        return user_id  
        
    except ExpiredSignatureError :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorize failed : Token has expire')
    except DecodeError :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorize failed : decode failed')
    except Exception as e  :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Authorize failed : {e}')
