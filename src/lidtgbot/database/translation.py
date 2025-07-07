import logging
from typing import Optional, Literal
from google.cloud.firestore import CollectionReference
from lidtgbot.models.translation import Translation
from lidtgbot.database.firestore_client import firestore_client

logger = logging.getLogger(__name__)

# Define the language code type for reuse
LanguageCode = Literal['de', 'en', 'tr', 'ru', 'fr', 'ar', 'uk', 'hi']


class TranslationRepository:
    """Repository for Translation operations with Firestore"""
    
    def __init__(self, num: str):
        if not firestore_client.is_initialized or firestore_client.db is None:
            raise RuntimeError("Firestore client is not initialized")
        self.collection: CollectionReference = firestore_client.db.collection(
            'questions').document(num).collection('translations')
    
    async def create_translation(self,
                                language_code: LanguageCode,
                                question: str,
                                context: str,
                                option_a: str,
                                option_b: str,
                                option_c: str,
                                option_d: str) -> Translation:
        """Create a new Translation in the database"""
        try:           
            translation_data = {
                'language_code': language_code,
                'question': question,
                'context': context,
                'option_a': option_a,
                'option_b': option_b,
                'option_c': option_c,
                'option_d': option_d,              
            }
            
            # Use translation language code as document ID for easy retrieval
            doc_ref = self.collection.document(language_code)
            doc_ref.set(translation_data)
            
            logger.info(f"Translation {language_code} created successfully")
            return Translation(
                language_code=language_code,
                question=question,
                context=context,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
            )
        
        except Exception as e:
            logger.error(f"Failed to create translation for {language_code}: {e}")
            raise
    
    async def get_translation(self, language_code: LanguageCode) -> Optional[Translation]:
        """Get Translation by language code"""
        try:
            doc_ref = self.collection.document(language_code)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                if data is None:
                    return None
                
                # Convert Firestore data to Translation object
                return Translation(
                    language_code=data['language_code'],
                    question=data['question'],
                    context=data['context'],
                    option_a=data['option_a'],
                    option_b=data['option_b'],
                    option_c=data['option_c'],
                    option_d=data['option_d'],                   
                )
            return None
        
        except Exception as e:
            logger.error(f"Failed to get translation {language_code}: {e}")
            raise    
