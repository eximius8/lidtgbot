import os
import json
import logging
from typing import Optional
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client

logger = logging.getLogger(__name__)


class FirestoreClient:
    """Simple Firestore client for Leben in Deutschland test bot"""
    
    def __init__(self):
        self.db: Optional[Client] = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase connection"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                service_account_key = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')
                if not service_account_key:
                    raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY environment variable not set")
                
                service_account_info = json.loads(service_account_key)
                cred = credentials.Certificate(service_account_info)
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            logger.info("Firebase initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            raise
    
    @property
    def is_initialized(self) -> bool:
        """Check if Firebase is properly initialized"""
        return self.db is not None

# Global instance
firestore_client = FirestoreClient()
