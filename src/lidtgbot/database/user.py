import logging
from datetime import datetime, timezone
from typing import Optional
from google.cloud.firestore import CollectionReference
from lidtgbot.models.user import User
from lidtgbot.database.firestore_client import firestore_client

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for user operations with Firestore"""
    
    def __init__(self):
        if not firestore_client.is_initialized or firestore_client.db is None:
            raise RuntimeError("Firestore client is not initialized")
        self.collection: CollectionReference = firestore_client.db.collection('users')
    
    async def create_user(self, user_id: int, first_name: str, username: Optional[str] = None, 
                         last_name: Optional[str] = None, language_code: Optional[str] = None) -> User:
        """Create a new user in the database"""
        try:
            now = datetime.now(timezone.utc)
            user_data = {
                'user_id': user_id,
                'first_name': first_name,
                'username': username,
                'last_name': last_name,
                'language_code': language_code,
                'created_at': now,
                'updated_at': now,
                'total_questions_answered': 0
            }
            
            # Use user_id as document ID for easy retrieval
            doc_ref = self.collection.document(str(user_id))
            doc_ref.set(user_data)
            
            logger.info(f"User {user_id} created successfully")
            return User(**user_data)
        
        except Exception as e:
            logger.error(f"Failed to create user {user_id}: {e}")
            raise
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            doc_ref = self.collection.document(str(user_id))
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                if data is None:
                    return None
                
                # Convert Firestore data to User object
                return User(
                    user_id=data['user_id'],
                    first_name=data['first_name'],
                    created_at=data['created_at'],
                    updated_at=data['updated_at'],
                    total_questions_answered=data.get('total_questions_answered', 0),
                    username=data.get('username'),
                    last_name=data.get('last_name'),
                    language_code=data.get('language_code')
                )
            return None
        
        except Exception as e:
            logger.error(f"Failed to get user {user_id}: {e}")
            raise
    
    async def get_or_create_user(self, user_id: int, first_name: str, username: Optional[str] = None,
                                last_name: Optional[str] = None, language_code: Optional[str] = None) -> User:
        """Get existing user or create new one"""
        user = await self.get_user(user_id)
        if user:
            return user
        
        return await self.create_user(user_id, first_name, username, last_name, language_code)
    
    async def update_user_activity(self, user_id: int) -> None:
        """Update user's last activity timestamp"""
        try:
            doc_ref = self.collection.document(str(user_id))
            doc_ref.update({
                'updated_at': datetime.utcnow()
            })
            logger.info(f"Updated activity for user {user_id}")
        
        except Exception as e:
            logger.error(f"Failed to update activity for user {user_id}: {e}")
            raise

# Global instance
user_repository = UserRepository()
