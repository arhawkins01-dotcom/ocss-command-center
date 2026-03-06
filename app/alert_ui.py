"""
Alert UI Components
Streamlit-based UI for displaying, managing, and interacting with alerts
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Optional, Callable
from app.alert_system import Alert, AlertLevel, AlertManager, get_alert_manager


def render_alert_banner(alert: Alert, container=None) -> Optional[str]:
    """
    Render a single alert with Streamlit message container
    
    Args:
        alert: Alert to render
        container: Streamlit container (defaults to main)
    
    Returns:
        str: The alert ID
    """
    if container is None:
        container = st
    
    # Format message with icon and styling
    emoji = alert.level.emoji()
    badge = alert.level.badge()
    
    message = f"**{emoji} {badge}**: {alert.title}\n\n{alert.message}"
    
    if alert.metadata:
        metadata_str = "\n\n**Details:**\n"
        for key, value in alert.metadata.items():
            metadata_str += f"- {key}: {value}\n"
        message += metadata_str
    
    # Display based on level
    if alert.level == AlertLevel.DEBUG:
        pass  # Don't display debug in UI
    elif alert.level == AlertLevel.INFO:
        container.info(message)
    elif alert.level == AlertLevel.WARNING:
        container.warning(message)
    elif alert.level == AlertLevel.ERROR or alert.level == AlertLevel.CRITICAL:
        container.error(message)
    
    return alert.alert_id


def render_alert_with_action(
    alert: Alert,
    on_action: Callable[[str], None],
    on_dismiss: Callable[[str], None],
    container=None
) -> None:
    """
    Render alert with action button and dismiss option
    
    Args:
        alert: Alert to render
        on_action: Callback for action button click
        on_dismiss: Callback for dismiss
        container: Streamlit container
    """
    if container is None:
        container = st
    
    emoji = alert.level.emoji()
    badge = alert.level.badge()
    
    # Create container for alert
    with container.container(border=True):
        col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
        
        with col1:
            st.markdown(f"### {emoji} {alert.title}")
            st.markdown(alert.message)
            
            if alert.metadata:
                with st.expander("📋 Details"):
                    for key, value in alert.metadata.items():
                        st.write(f"**{key}**: {value}")
        
        with col2:
            if alert.requires_action:
                if st.button(alert.action_label, key=f"action_{alert.alert_id}", use_container_width=True):
                    on_action(alert.alert_id)
                    st.rerun()
        
        with col3:
            if alert.dismissible:
                if st.button("✕", key=f"dismiss_{alert.alert_id}", use_container_width=True):
                    on_dismiss(alert.alert_id)
                    st.rerun()


def render_alert_toast(
    state_key: str,
    max_alerts: int = 5,
    auto_dismiss: bool = True
) -> None:
    """
    Render toast notifications for non-critical alerts
    
    Args:
        state_key: Session state key to store toast state
        max_alerts: Maximum toasts to show
        auto_dismiss: Whether toasts auto-dismiss
    """
    if state_key not in st.session_state:
        st.session_state[state_key] = []
    
    manager = get_alert_manager()
    info_alerts = manager.get_active_alerts(level_min=AlertLevel.INFO, exclude_acknowledged=True)
    
    for idx, alert in enumerate(info_alerts[:max_alerts]):
        if alert.level in [AlertLevel.INFO, AlertLevel.DEBUG]:
            st.toast(
                f"{alert.level.emoji()} {alert.title}: {alert.message}",
                icon=alert.level.emoji()
            )


def render_alert_badge(
    position: str = "sidebar",
    container=None
) -> None:
    """
    Render alert count badge in header or sidebar
    
    Args:
        position: 'sidebar', 'header', or 'custom'
        container: Custom container if position is 'custom'
    """
    manager = get_alert_manager()
    counts = manager.get_alert_counts()
    
    # Calculate alert indicator
    critical = counts.get('CRITICAL', 0)
    errors = counts.get('ERROR', 0)
    warnings = counts.get('WARNING', 0)
    
    if critical > 0:
        badge = f"🚨 {critical}"
        color = "#8b0000"
    elif errors > 0:
        badge = f"❌ {errors}"
        color = "#d62728"
    elif warnings > 0:
        badge = f"⚠️ {warnings}"
        color = "#ff7f0e"
    else:
        badge = "✅ Good"
        color = "#2ca02c"
    
    if position == "sidebar":
        st.sidebar.markdown(f"<div style='background-color:{color}; padding:8px; border-radius:4px; text-align:center; color:white; font-weight:bold;'>{badge}</div>", unsafe_allow_html=True)
    elif position == "header":
        st.markdown(f"<div style='background-color:{color}; padding:8px; border-radius:4px; text-align:center; color:white; font-weight:bold;'>{badge}</div>", unsafe_allow_html=True)
    elif position == "custom" and container:
        container.markdown(f"<div style='background-color:{color}; padding:8px; border-radius:4px; text-align:center; color:white; font-weight:bold;'>{badge}</div>", unsafe_allow_html=True)


def render_active_alerts(
    manager: AlertManager,
    role: Optional[str] = None,
    exclude_acknowledged: bool = False,
    show_actions: bool = True,
    container=None
) -> None:
    """
    Render panel of all active alerts
    
    Args:
        manager: AlertManager instance
        role: Optional role filter
        exclude_acknowledged: Skip acknowledged alerts
        show_actions: Show action buttons
        container: Streamlit container
    """
    if container is None:
        container = st
    
    alerts = manager.get_active_alerts(role=role, exclude_acknowledged=exclude_acknowledged)
    
    if not alerts:
        container.info("✅ No active alerts")
        return
    
    container.subheader(f"📢 Active Alerts ({len(alerts)})")
    
    # Group by level
    by_level = {}
    for alert in alerts:
        level_name = alert.level.name
        if level_name not in by_level:
            by_level[level_name] = []
        by_level[level_name].append(alert)
    
    # Display by level (critical first)
    level_order = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
    for level_name in level_order:
        if level_name not in by_level:
            continue
        
        level_alerts = by_level[level_name]
        with container.expander(f"{AlertLevel[level_name].emoji()} {level_name} ({len(level_alerts)})", expanded=(level_name in ['CRITICAL', 'ERROR'])):
            for alert in level_alerts:
                if show_actions and alert.requires_action:
                    render_alert_with_action(
                        alert,
                        on_action=lambda aid: manager.acknowledge_alert(aid, st.session_state.get('current_user', 'Unknown')),
                        on_dismiss=lambda aid: manager.dismiss_alert(aid),
                        container=st
                    )
                else:
                    col1, col2 = st.columns([0.9, 0.1])
                    with col1:
                        st.markdown(f"**{alert.title}**")
                        st.write(alert.message)
                    with col2:
                        if alert.dismissible:
                            if st.button("✕", key=f"dismiss_{alert.alert_id}", help="Dismiss this alert"):
                                manager.dismiss_alert(alert.alert_id)
                                st.rerun()
                st.divider()


def render_alert_dashboard(
    manager: AlertManager,
    container=None
) -> None:
    """
    Render comprehensive alert dashboard
    
    Args:
        manager: AlertManager instance
        container: Streamlit container
    """
    if container is None:
        container = st
    
    # Summary metrics
    counts = manager.get_alert_counts()
    
    col1, col2, col3, col4, col5 = container.columns(5)
    with col1:
        container.metric("🚨 Critical", counts.get('CRITICAL', 0))
    with col2:
        container.metric("❌ Errors", counts.get('ERROR', 0))
    with col3:
        container.metric("⚠️ Warnings", counts.get('WARNING', 0))
    with col4:
        container.metric("ℹ️ Info", counts.get('INFO', 0))
    with col5:
        container.metric("Total", sum(counts.values()))
    
    container.divider()
    
    # Active alerts
    render_active_alerts(manager, show_actions=True, container=container)
    
    container.divider()
    
    # History
    container.subheader("📜 Alert History (Last 7 Days)")
    history = manager.get_history(days=7, level_min=AlertLevel.WARNING)
    
    if history:
        history_data = [{
            'Time': a.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'Level': a.level.emoji() + ' ' + a.level.name,
            'Category': a.category,
            'Title': a.title,
            'Acknowledged': '✓' if a.acknowledged else '✗'
        } for a in history]
        
        df = pd.DataFrame(history_data)
        container.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export button
        col1, col2 = container.columns(2)
        with col1:
            csv_data = manager.export_history(format='csv')
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name=f"alerts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        with col2:
            json_data = manager.export_history(format='json')
            st.download_button(
                label="📥 Download as JSON",
                data=json_data,
                file_name=f"alerts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    else:
        container.info("No alerts in history")


def render_category_alerts(
    manager: AlertManager,
    category: str,
    title: Optional[str] = None,
    container=None
) -> int:
    """
    Render alerts for specific category
    
    Args:
        manager: AlertManager instance
        category: Category to filter
        title: Optional section title
        container: Streamlit container
    
    Returns:
        int: Number of alerts displayed
    """
    if container is None:
        container = st
    
    alerts = [a for a in manager.get_active_alerts() if a.category == category]
    
    if not alerts:
        return 0
    
    if title:
        container.subheader(title)
    
    for alert in alerts:
        emoji = alert.level.emoji()
        with container.container(border=True):
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.markdown(f"{emoji} **{alert.title}**")
                st.caption(alert.message)
            with col2:
                if st.button("✕", key=f"dismiss_cat_{alert.alert_id}"):
                    manager.dismiss_alert(alert.alert_id)
                    st.rerun()
    
    return len(alerts)


def render_alert_preferences(
    manager: AlertManager,
    container=None
) -> None:
    """
    Render alert preferences/configuration UI
    
    Args:
        manager: AlertManager instance
        container: Streamlit container
    """
    if container is None:
        container = st
    
    container.subheader("⚙️ Alert Preferences")
    
    col1, col2 = container.columns(2)
    
    with col1:
        min_persist = st.selectbox(
            "Minimum level to persist",
            options=[level.name for level in AlertLevel],
            index=AlertLevel.WARNING.value,
            key="alert_min_persist"
        )
    
    with col2:
        retention = st.number_input(
            "Retention days",
            min_value=1,
            max_value=365,
            value=manager.alert_config.get('retention_days', 30),
            key="alert_retention"
        )
    
    col3, col4 = container.columns(2)
    
    with col3:
        max_alerts = st.number_input(
            "Max simultaneous alerts",
            min_value=1,
            max_value=500,
            value=manager.alert_config.get('max_simultaneous_alerts', 50),
            key="alert_max"
        )
    
    with col4:
        default_expire = st.number_input(
            "Default expiration (seconds)",
            min_value=0,
            step=60,
            value=manager.alert_config.get('default_expires_seconds', 300),
            key="alert_expire"
        )
    
    if st.button("💾 Save Preferences", use_container_width=True):
        manager.alert_config['min_level_to_persist'] = min_persist
        manager.alert_config['retention_days'] = retention
        manager.alert_config['max_simultaneous_alerts'] = max_alerts
        manager.alert_config['default_expires_seconds'] = default_expire
        manager._save_config()
        st.success("✅ Alert preferences saved")
