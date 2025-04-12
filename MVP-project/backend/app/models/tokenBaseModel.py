from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RefreshToken(BaseModel):
    token_id: str
    user_id: str
    expires_at: datetime
    is_active: Optional[bool] = True

class TokenRefreshRequest(BaseModel):
    refresh_token: str