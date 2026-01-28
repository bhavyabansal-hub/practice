"""
Database Manager for MySQL Operations
Handles vendor mobile verification updates and other database operations
Production-grade with error handling, transaction management, and logging
"""

import mysql.connector
from mysql.connector import Error
import json
import logging
from datetime import datetime
from typing import Dict, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Production-grade MySQL database manager
    Handles vendor table operations with transaction management
    """
    
    # Database configuration
    DB_CONFIG = {
        'host': '3.6.16.231',
        'port': 3306,
        'user': 'bhavya',
        'password': 'zoFRo2r0t1ucun',
        'database': 'staging',
        'autocommit': False,
        'raise_on_warnings': False
    }
    
    def __init__(self):
        """Initialize database connection"""
        self.connection = None
        self.cursor = None
        self._connect()
    
    def _connect(self) -> bool:
        """
        Establish database connection
        Returns: True if successful, False otherwise
        """
        try:
            self.connection = mysql.connector.connect(**self.DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            logger.info("✅ Database connection established")
            return True
        except Error as err:
            logger.error(f"❌ Database connection failed: {err}")
            return False
    
    def _reconnect(self) -> bool:
        """Reconnect to database if connection lost"""
        try:
            if self.connection is not None:
                self.connection.close()
            return self._connect()
        except Error as err:
            logger.error(f"❌ Reconnection failed: {err}")
            return False
    
    def verify_mobile_for_email(self, email: str) -> Tuple[bool, str]:
        """
        Update mobile_verified = 1 for vendor with given email
        
        Args:
            email: Vendor email to verify
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not email:
            logger.warning("⚠️  Email is empty")
            return False, "Email is empty"
        
        try:
            # Check if connection is alive
            if self.connection is None or not self.connection.is_connected():
                logger.warning("⚠️  Connection lost, attempting reconnect...")
                if not self._reconnect():
                    return False, "Failed to reconnect to database"
            
            # Start transaction
            self.connection.start_transaction()
            logger.info(f"🔄 Starting transaction for email: {email}")
            
            # Check if vendor exists
            check_query = "SELECT email, mobile_verified FROM vendor WHERE email = %s"
            self.cursor.execute(check_query, (email,))
            vendor = self.cursor.fetchone()
            
            if not vendor:
                self.connection.rollback()
                msg = f"❌ Vendor not found with email: {email}"
                logger.warning(msg)
                return False, msg
            
            current_status = vendor['mobile_verified']
            logger.info(f"📋 Found vendor email {email}, current mobile_verified: {current_status}")
            
            # Update mobile_verified to 1
            update_query = """
                UPDATE vendor
                SET mobile_verified = 1
                WHERE email = %s
            """
            self.cursor.execute(update_query, (email,))
            affected_rows = self.cursor.rowcount
            
            if affected_rows == 0:
                self.connection.rollback()
                msg = f"❌ Failed to update mobile_verified for email: {email}"
                logger.error(msg)
                return False, msg
            
            # Verify update was successful
            self.cursor.execute(check_query, (email,))
            updated_vendor = self.cursor.fetchone()
            
            if updated_vendor['mobile_verified'] != 1:
                self.connection.rollback()
                msg = f"❌ Verification failed - mobile_verified is still {updated_vendor['mobile_verified']}"
                logger.error(msg)
                return False, msg
            
            # Commit transaction
            self.connection.commit()
            msg = f"✅ Mobile verification successful for {email}"
            logger.info(msg)
            return True, msg
            
        except Error as err:
            if self.connection:
                self.connection.rollback()
            logger.error(f"❌ Database error during mobile verification: {err}")
            return False, f"Database error: {str(err)}"
        except Exception as err:
            if self.connection:
                self.connection.rollback()
            logger.error(f"❌ Unexpected error: {err}")
            return False, f"Unexpected error: {str(err)}"
    
    def get_vendor_by_email(self, email: str) -> Optional[Dict]:
        """
        Get vendor details by email
        
        Args:
            email: Vendor email
            
        Returns:
            Vendor details dict or None if not found
        """
        try:
            if self.connection is None or not self.connection.is_connected():
                if not self._reconnect():
                    return None
            
            query = "SELECT id, email, mobile_verified, created_at FROM vendor WHERE email = %s"
            self.cursor.execute(query, (email,))
            return self.cursor.fetchone()
            
        except Error as err:
            logger.error(f"❌ Error fetching vendor: {err}")
            return None
    
    def check_mobile_verified_status(self, email: str) -> Tuple[bool, int]:
        """
        Check mobile_verified status for a vendor
        
        Args:
            email: Vendor email
            
        Returns:
            Tuple[bool, int]: (exists, mobile_verified_value)
        """
        try:
            if self.connection is None or not self.connection.is_connected():
                if not self._reconnect():
                    return False, -1
            
            vendor = self.get_vendor_by_email(email)
            if vendor:
                return True, vendor['mobile_verified']
            return False, -1
            
        except Error as err:
            logger.error(f"❌ Error checking status: {err}")
            return False, -1
    
    def reset_mobile_verified(self, email: str) -> Tuple[bool, str]:
        """
        Reset mobile_verified to 0 (for cleanup/testing)
        
        Args:
            email: Vendor email
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            if self.connection is None or not self.connection.is_connected():
                if not self._reconnect():
                    return False, "Failed to reconnect to database"
            
            self.connection.start_transaction()
            
            update_query = "UPDATE vendor SET mobile_verified = 0 WHERE email = %s"
            self.cursor.execute(update_query, (email,))
            
            if self.cursor.rowcount == 0:
                self.connection.rollback()
                return False, f"Vendor not found: {email}"
            
            self.connection.commit()
            msg = f"✅ Mobile verification reset to 0 for {email}"
            logger.info(msg)
            return True, msg
            
        except Error as err:
            if self.connection:
                self.connection.rollback()
            logger.error(f"❌ Error resetting mobile verification: {err}")
            return False, f"Database error: {str(err)}"
    
    def close(self):
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                logger.info("✅ Database connection closed")
        except Error as err:
            logger.error(f"❌ Error closing connection: {err}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure connection is closed"""
        self.close()


# Helper function for quick operations
def verify_mobile_for_vendor(email: str) -> Tuple[bool, str]:
    """
    Quick helper function to verify mobile for a vendor
    
    Usage:
        success, message = verify_mobile_for_vendor("test@example.com")
        if success:
            print("Mobile verified!")
        else:
            print(f"Error: {message}")
    """
    try:
        with DatabaseManager() as db:
            return db.verify_mobile_for_email(email)
    except Exception as err:
        logger.error(f"❌ Error in quick verify: {err}")
        return False, f"Error: {str(err)}"
