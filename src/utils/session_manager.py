"""
SESSION & COOKIE MANAGEMENT
============================

This module manages test sessions across multiple test modules.
Instead of creating a new account for each module, we:
1. Check if session/cookie already exists
2. If YES → Reuse it (save time, reduce server load)
3. If NO → Create account once, save session for future use

PRODUCTION APPROACH:
- Real users don't create accounts every time
- We use existing session/cookie for all test modules
- Only create 1 account per test run
- Much faster & realistic testing

Usage:
    from utils.session_manager import SessionManager
    
    # Check & get session (creates if needed)
    credentials = SessionManager.get_or_create_session()
    email = credentials['email']
    password = credentials['password']
"""

import json
import os
from datetime import datetime
from pathlib import Path


class SessionManager:
    """Manage test sessions across modules"""
    
    SESSION_DIR = "test_sessions"
    SESSION_FILE = f"{SESSION_DIR}/test_session.json"
    
    @staticmethod
    def ensure_session_dir():
        """Create session directory if it doesn't exist"""
        os.makedirs(SessionManager.SESSION_DIR, exist_ok=True)
    
    @staticmethod
    def save_session(email, password, account_type="created"):
        """
        Save session credentials to file
        
        Args:
            email: Test account email
            password: Test account password
            account_type: 'created' (new) or 'existing' (reused)
        """
        SessionManager.ensure_session_dir()
        
        session_data = {
            "email": email,
            "password": password,
            "account_type": account_type,
            "created_at": datetime.now().isoformat(),
            "used_by_modules": ["authentication"]  # Track which modules used this
        }
        
        with open(SessionManager.SESSION_FILE, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"\n✅ Session saved: {email} ({account_type})")
    
    @staticmethod
    def load_session():
        """
        Load existing session credentials
        
        Returns:
            dict with email & password, or None if no session exists
        """
        if not os.path.exists(SessionManager.SESSION_FILE):
            return None
        
        try:
            with open(SessionManager.SESSION_FILE, 'r') as f:
                session_data = json.load(f)
            return session_data
        except:
            return None
    
    @staticmethod
    def get_session():
        """
        Get current session without creating new one
        
        Returns:
            dict with credentials, or None if no session
        """
        return SessionManager.load_session()
    
    @staticmethod
    def session_exists():
        """Check if session file exists"""
        return os.path.exists(SessionManager.SESSION_FILE)
    
    @staticmethod
    def clear_session():
        """Clear session (for debugging/cleanup)"""
        if os.path.exists(SessionManager.SESSION_FILE):
            os.remove(SessionManager.SESSION_FILE)
            print("✅ Session cleared")
    
    @staticmethod
    def get_session_info():
        """Get detailed session info"""
        session = SessionManager.load_session()
        if not session:
            return "No session found"
        
        info = f"""
        📋 CURRENT SESSION INFO:
        ├─ Email: {session['email']}
        ├─ Type: {session['account_type']}
        ├─ Created: {session['created_at']}
        └─ Used by: {', '.join(session['used_by_modules'])}
        """
        return info
    
    @staticmethod
    def add_module_usage(module_name):
        """Track which modules used this session"""
        session = SessionManager.load_session()
        if session:
            if module_name not in session['used_by_modules']:
                session['used_by_modules'].append(module_name)
            
            with open(SessionManager.SESSION_FILE, 'w') as f:
                json.dump(session, f, indent=2)
