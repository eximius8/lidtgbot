import logging
from datetime import datetime, timezone
from typing import Optional, Literal
from google.cloud.firestore import CollectionReference
from lidtgbot.models.question import Question
from lidtgbot.database.firestore_client import firestore_client

logger = logging.getLogger(__name__)


class QuestionRepository:
    """Repository for question operations with Firestore"""
    
    def __init__(self):
        if not firestore_client.is_initialized or firestore_client.db is None:
            raise RuntimeError("Firestore client is not initialized")
        self.collection: CollectionReference = firestore_client.db.collection('questions')
    
    async def create_question(self, num: str, 
                              solution: Literal['a', 'b', 'c', 'd'], 
                              image: str | None = None) -> Question:
        """Create a new question in the database"""
        try:
            now = datetime.now(timezone.utc)
            question_data = {
                'num': num,
                'solution': solution,
                'image': image,
                'created_at': now,
                'updated_at': now,
            }
            
            # Use question number as document ID for easy retrieval
            doc_ref = self.collection.document(str(num))
            doc_ref.set(question_data)
            
            logger.info(f"Question {num} created successfully")
            return Question(**question_data)
        
        except Exception as e:
            logger.error(f"Failed to create question {num}: {e}")
            raise
    
    async def get_question(self, num: str) -> Optional[Question]:
        """Get question by num"""
        try:
            doc_ref = self.collection.document(str(num))
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                if data is None:
                    return None
                
                # Convert Firestore data to Question object
                return Question(
                    num=data['num'],
                    solution=data['solution'],
                    image=data.get('image', None),
                    created_at=data['created_at'],
                    updated_at=data['updated_at']
                )
            return None
        
        except Exception as e:
            logger.error(f"Failed to get question {num}: {e}")
            raise    


# Global instance
question_repository = QuestionRepository()
