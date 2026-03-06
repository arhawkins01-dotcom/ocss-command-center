"""
Comprehensive Alert & Notification System
Handles all system alerts, warnings, errors with persistence, tracking, and routing
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
from pathlib import Path
import hashlib


class AlertLevel(Enum):
    """Alert severity levels"""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    
    def color(self) -> str:
        """Return color code for alert level"""
        colors = {
            AlertLevel.DEBUG: "#808080",      # Gray
            AlertLevel.INFO: "#1f77b4",       # Blue
            AlertLevel.WARNING: "#ff7f0e",    # Orange
            AlertLevel.ERROR: "#d62728",      # Red
            AlertLevel.CRITICAL: "#8b0000"    # Dark Red
        }
        return colors.get(self, "#808080")
    
    def emoji(self) -> str:
        """Return emoji for alert level"""
        emojis = {
            AlertLevel.DEBUG: "🐛",
            AlertLevel.INFO: "ℹ️",
            AlertLevel.WARNING: "⚠️",
            AlertLevel.ERROR: "❌",
            AlertLevel.CRITICAL: "🚨"
        }
        return emojis.get(self, "ℹ️")
    
    def badge(self) -> str:
        """Return badge text for alert level"""
        badges = {
            AlertLevel.DEBUG: "DEBUG",
            AlertLevel.INFO: "INFO",
            AlertLevel.WARNING: "WARNING",
            AlertLevel.ERROR: "ERROR",
            AlertLevel.CRITICAL: "CRITICAL"
        }
        return badges.get(self, "INFO")


class Alert:
    """Individual alert object with metadata"""
    
    def __init__(
        self,
        title: str,
        message: str,
        level: AlertLevel = AlertLevel.INFO,
        category: str = "general",
        alert_id: Optional[str] = None,
        dismissible: bool = True,
        persistent: bool = False,
        requires_action: bool = False,
        action_label: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        expires_in_seconds: Optional[int] = None,
        affected_role: Optional[str] = None,
        affected_user: Optional[str] = None
    ):
        """
        Create an alert instance
        
        Args:
            title: Alert title
            message: Alert description/message
            level: AlertLevel enum value
            category: Category for filtering (e.g., 'compliance', 'performance', 'system')
            alert_id: Unique identifier (auto-generated if not provided)
            dismissible: Whether user can dismiss the alert
            persistent: Whether to store in history
            requires_action: Whether alert requires user action
            action_label: Button text if requires_action is True
            metadata: Additional context data
            expires_in_seconds: Time before alert auto-dismisses (None = never)
            affected_role: Specific role this alert targets
            affected_user: Specific user this alert targets
        """
        self.title = title
        self.message = message
        self.level = level if isinstance(level, AlertLevel) else AlertLevel.INFO
        self.category = category
        self.alert_id = alert_id or self._generate_id()
        self.dismissible = dismissible
        self.persistent = persistent
        self.requires_action = requires_action
        self.action_label = action_label or "Action Required"
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(seconds=expires_in_seconds) if expires_in_seconds else None
        self.affected_role = affected_role
        self.affected_user = affected_user
        self.acknowledged = False
        self.acknowledged_by = None
        self.acknowledged_at = None
    
    def _generate_id(self) -> str:
        """Generate unique alert ID"""
        content = f"{self.title}{self.message}{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary for serialization"""
        return {
            'alert_id': self.alert_id,
            'title': self.title,
            'message': self.message,
            'level': self.level.name,
            'category': self.category,
            'dismissible': self.dismissible,
            'persistent': self.persistent,
            'requires_action': self.requires_action,
            'action_label': self.action_label,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'affected_role': self.affected_role,
            'affected_user': self.affected_user,
            'acknowledged': self.acknowledged,
            'acknowledged_by': self.acknowledged_by,
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Alert':
        """Reconstruct alert from dictionary"""
        alert = Alert(
            title=data['title'],
            message=data['message'],
            level=AlertLevel[data.get('level', 'INFO')],
            category=data.get('category', 'general'),
            alert_id=data.get('alert_id'),
            dismissible=data.get('dismissible', True),
            persistent=data.get('persistent', False),
            requires_action=data.get('requires_action', False),
            action_label=data.get('action_label'),
            metadata=data.get('metadata', {}),
            affected_role=data.get('affected_role'),
            affected_user=data.get('affected_user')
        )
        if data.get('expires_at'):
            alert.expires_at = datetime.fromisoformat(data['expires_at'])
        alert.acknowledged = data.get('acknowledged', False)
        alert.acknowledged_by = data.get('acknowledged_by')
        if data.get('acknowledged_at'):
            alert.acknowledged_at = datetime.fromisoformat(data['acknowledged_at'])
        return alert
    
    def is_expired(self) -> bool:
        """Check if alert has expired"""
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at
    
    def acknowledge(self, user: str) -> None:
        """Mark alert as acknowledged"""
        self.acknowledged = True
        self.acknowledged_by = user
        self.acknowledged_at = datetime.now()


class AlertManager:
    """Central alert management system"""
    
    ALERT_STORAGE_PATH = Path("data/alerts")
    ALERT_HISTORY_FILE = ALERT_STORAGE_PATH / "alert_history.jsonl"
    ALERT_CONFIG_FILE = Path("data/alert_config.json")
    
    def __init__(self):
        """Initialize alert manager"""
        self.alerts: Dict[str, Alert] = {}
        self._ensure_storage_dirs()
        self._load_config()
    
    @staticmethod
    def _ensure_storage_dirs() -> None:
        """Ensure alert storage directories exist"""
        AlertManager.ALERT_STORAGE_PATH.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> None:
        """Load alert configuration"""
        if not self.ALERT_CONFIG_FILE.exists():
            self.alert_config = {
                'min_level_to_persist': AlertLevel.WARNING.name,
                'retention_days': 30,
                'max_simultaneous_alerts': 50,
                'default_expires_seconds': 300,
            }
            self._save_config()
        else:
            with open(self.ALERT_CONFIG_FILE) as f:
                self.alert_config = json.load(f)
    
    def _save_config(self) -> None:
        """Save alert configuration"""
        with open(self.ALERT_CONFIG_FILE, 'w') as f:
            json.dump(self.alert_config, f, indent=2)
    
    def alert(
        self,
        title: str,
        message: str,
        level: AlertLevel = AlertLevel.INFO,
        **kwargs
    ) -> Alert:
        """
        Create and register a new alert
        
        Args:
            title: Alert title
            message: Alert message
            level: AlertLevel
            **kwargs: Additional Alert constructor arguments
        
        Returns:
            Alert: The created alert
        """
        alert = Alert(title, message, level, **kwargs)
        self.alerts[alert.alert_id] = alert
        
        # Persist if configured
        if alert.persistent and level.value >= AlertLevel[self.alert_config['min_level_to_persist']].value:
            self._persist_alert(alert)
        
        # Initialize session state tracking
        if 'alert_acknowledgments' not in st.session_state:
            st.session_state.alert_acknowledgments = {}
        
        return alert
    
    def _persist_alert(self, alert: Alert) -> None:
        """Write alert to persistent storage"""
        self.ALERT_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ALERT_HISTORY_FILE, 'a') as f:
            f.write(json.dumps(alert.to_dict()) + '\n')
    
    def acknowledge_alert(self, alert_id: str, user: str) -> bool:
        """
        Mark an alert as acknowledged
        
        Args:
            alert_id: Alert ID to acknowledge
            user: User acknowledging the alert
        
        Returns:
            bool: Success status
        """
        if alert_id not in self.alerts:
            return False
        
        alert = self.alerts[alert_id]
        alert.acknowledge(user)
        
        # Track in session state
        if 'alert_acknowledgments' not in st.session_state:
            st.session_state.alert_acknowledgments = {}
        st.session_state.alert_acknowledgments[alert_id] = {
            'acknowledged_at': alert.acknowledged_at.isoformat(),
            'acknowledged_by': user
        }
        
        return True
    
    def dismiss_alert(self, alert_id: str) -> bool:
        """Remove alert from active display"""
        if alert_id in self.alerts:
            alert = self.alerts.pop(alert_id)
            # Non-persistent alerts can be truly dismissed
            if not alert.persistent:
                return True
            # Persistent alerts are just hidden from immediate view
            return True
        return False
    
    def get_active_alerts(
        self,
        level_min: AlertLevel = AlertLevel.INFO,
        category: Optional[str] = None,
        role: Optional[str] = None,
        user: Optional[str] = None,
        exclude_acknowledged: bool = False
    ) -> List[Alert]:
        """
        Get filtered list of active alerts
        
        Args:
            level_min: Minimum alert level to return
            category: Filter by category
            role: Filter by affected role
            user: Filter by affected user
            exclude_acknowledged: Exclude acknowledged alerts
        
        Returns:
            List[Alert]: Filtered alerts
        """
        alerts = []
        for alert in self.alerts.values():
            # Skip expired alerts
            if alert.is_expired():
                continue
            
            # Level filter
            if alert.level.value < level_min.value:
                continue
            
            # Category filter
            if category and alert.category != category:
                continue
            
            # Role filter
            if role and alert.affected_role and alert.affected_role != role:
                continue
            
            # User filter
            if user and alert.affected_user and alert.affected_user != user:
                continue
            
            # Acknowledged filter
            if exclude_acknowledged and alert.acknowledged:
                continue
            
            alerts.append(alert)
        
        # Sort by level (critical first) then by creation time
        return sorted(alerts, key=lambda a: (-a.level.value, -a.created_at.timestamp()))
    
    def get_alert_counts(self, role: Optional[str] = None) -> Dict[str, int]:
        """
        Get counts of alerts by level
        
        Args:
            role: Optional role filter
        
        Returns:
            Dict with counts by level
        """
        counts = {level.name: 0 for level in AlertLevel}
        
        for alert in self.get_active_alerts(role=role):
            counts[alert.level.name] += 1
        
        return counts
    
    def clear_expired(self) -> int:
        """Remove all expired alerts"""
        expired = [aid for aid, a in self.alerts.items() if a.is_expired()]
        for aid in expired:
            del self.alerts[aid]
        return len(expired)
    
    def get_history(
        self,
        days: int = 7,
        level_min: AlertLevel = AlertLevel.WARNING,
        category: Optional[str] = None
    ) -> List[Alert]:
        """
        Get alert history from persistent storage
        
        Args:
            days: Number of days to look back
            level_min: Minimum level to retrieve
            category: Optional category filter
        
        Returns:
            List[Alert]: Historical alerts
        """
        if not self.ALERT_HISTORY_FILE.exists():
            return []
        
        cutoff_date = datetime.now() - timedelta(days=days)
        history = []
        
        try:
            with open(self.ALERT_HISTORY_FILE) as f:
                for line in f:
                    data = json.loads(line)
                    alert = Alert.from_dict(data)
                    
                    if alert.created_at < cutoff_date:
                        continue
                    if alert.level.value < level_min.value:
                        continue
                    if category and alert.category != category:
                        continue
                    
                    history.append(alert)
        except Exception as e:
            st.warning(f"Error loading alert history: {e}")
        
        return sorted(history, key=lambda a: -a.created_at.timestamp())
    
    def export_history(self, format: str = 'csv') -> bytes:
        """
        Export alert history to file
        
        Args:
            format: 'csv' or 'json'
        
        Returns:
            bytes: File content
        """
        history = self.get_history(days=30)
        
        if format == 'csv':
            data = [{
                'ID': a.alert_id,
                'Timestamp': a.created_at.isoformat(),
                'Level': a.level.name,
                'Category': a.category,
                'Title': a.title,
                'Message': a.message,
                'Acknowledged By': a.acknowledged_by or 'N/A',
                'Acknowledged At': a.acknowledged_at.isoformat() if a.acknowledged_at else 'N/A'
            } for a in history]
            
            df = pd.DataFrame(data)
            return df.to_csv(index=False).encode()
        
        else:  # json
            data = [a.to_dict() for a in history]
            return json.dumps(data, indent=2).encode()


def get_alert_manager() -> AlertManager:
    """Get or create global alert manager in session state"""
    if 'alert_manager' not in st.session_state:
        st.session_state.alert_manager = AlertManager()
    return st.session_state.alert_manager


def create_alert(
    title: str,
    message: str,
    level: AlertLevel = AlertLevel.INFO,
    **kwargs
) -> Alert:
    """
    Convenience function to create an alert via global manager
    
    Args:
        title: Alert title
        message: Alert message
        level: AlertLevel
        **kwargs: Additional Alert arguments
    
    Returns:
        Alert: Created alert object
    """
    manager = get_alert_manager()
    return manager.alert(title, message, level, **kwargs)
