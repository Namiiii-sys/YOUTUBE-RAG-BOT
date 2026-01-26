from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import auth

security = HTTPBearer()

if not firebase_admin._apps:
    import os
    from firebase_admin import credentials
    
    # Check for credentials file
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_service_account.json")
    
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print(f"Firebase Admin initialized with credentials from {cred_path}")
    else:
        # Fallback to default (ADC)
        print("Warning: No 'firebase_service_account.json' found. Attempting default initialization. Token verification may fail if Project ID cannot be determined.")
        try:
            firebase_admin.initialize_app()
        except Exception as e:
            print(f"Failed to initialize Firebase Admin: {e}")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifies the Firebase ID Token sent in the Authorization header.
    Returns the decoded token (user info) if valid, otherwise raises 401.
    """
    token = credentials.credentials
    try:
        # Verify the ID token while checking if the token is revoked.
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )