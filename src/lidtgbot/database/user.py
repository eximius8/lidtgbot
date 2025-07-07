import logging
from datetime import datetime, timezone
from google.cloud.firestore import CollectionReference
from lidtgbot.models.user import User
from lidtgbot.database.firestore_client import firestore_client

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for user operations with Firestore - Single call optimization"""
    
    def __init__(self):
        if not firestore_client.is_initialized or firestore_client.db is None:
            raise RuntimeError("Firestore client is not initialized")
        self.collection: CollectionReference = firestore_client.db.collection('users')
    
    async def ensure_user(self, user_id: int, first_name: str, username: str | None = None,
                         last_name: str | None = None, language_code: str | None = None,
                         update_activity: bool = False) -> User:
        """
        Ensure user exists with a single Firestore operation.
        This method uses set() with merge=True to either create or update the user.
        
        Args:
            user_id: Telegram user ID
            first_name: User's first name
            username: User's username (optional)
            last_name: User's last name (optional)
            language_code: User's language code (optional)
            update_activity: Whether to update the updated_at timestamp
            
        Returns:
            User object
        """
        try:
            now = datetime.now(timezone.utc)
            doc_ref = self.collection.document(str(user_id))
            
            # Data that should always be updated
            user_data = {
                'user_id': user_id,
                'first_name': first_name,
                'username': username,
                'last_name': last_name,
                'language_code': language_code,
            }
            
            if update_activity:
                user_data['updated_at'] = now
            
            # Data that should only be set on creation
            creation_data = {
                'created_at': now,
                'total_questions_answered': 0,
            }
            
            # First, try to get the document to see if it exists
            doc = doc_ref.get()
            
            if doc.exists:
                # User exists - only update the changeable fields
                doc_ref.update(user_data)
                
                # Get the updated document data
                existing_data = doc.to_dict()
                if existing_data is None:
                    raise ValueError(f"User document {user_id} exists but has no data")
                
                # Merge the updated data
                existing_data.update(user_data)
                
                logger.debug(f"User {user_id} updated")
                return User(
                    user_id=existing_data['user_id'],
                    first_name=existing_data['first_name'],
                    created_at=existing_data['created_at'],
                    updated_at=existing_data.get('updated_at', existing_data['created_at']),
                    total_questions_answered=existing_data.get('total_questions_answered', 0),
                    username=existing_data.get('username'),
                    last_name=existing_data.get('last_name'),
                    language_code=existing_data.get('language_code')
                )
            else:
                # User doesn't exist - create with all data
                all_data = {**user_data, **creation_data}
                if not update_activity:
                    all_data['updated_at'] = now
                
                doc_ref.set(all_data)
                logger.info(f"User {user_id} created successfully")
                return User(**all_data)
        
        except Exception as e:
            logger.error(f"Failed to ensure user {user_id}: {e}")
            raise
    
    # Keep original methods for backward compatibility
    async def get_user(self, user_id: int) -> User | None:
        """Get user by ID"""
        try:
            doc_ref = self.collection.document(str(user_id))
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                if data is None:
                    return None
                
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
    
    async def get_or_create_user(self, user_id: int, first_name: str, username: str | None = None,
                                last_name: str | None = None, language_code: str | None = None) -> User:
        """Backward compatibility method - delegates to ensure_user"""
        return await self.ensure_user(user_id, first_name, username, last_name, language_code, update_activity=False)
    
    async def update_user_activity(self, user_id: int) -> None:
        """Update user's last activity timestamp"""
        try:
            doc_ref = self.collection.document(str(user_id))
            doc_ref.update({
                'updated_at': datetime.now(timezone.utc)
            })
            logger.debug(f"Updated activity for user {user_id}")
        
        except Exception as e:
            logger.error(f"Failed to update activity for user {user_id}: {e}")
            raise

# Global instance
user_repository = UserRepository()