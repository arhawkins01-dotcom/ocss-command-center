from __future__ import annotations

import os
import base64
import hashlib
import hmac
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import streamlit as st


@dataclass(frozen=True)
class AuthResult:
    authenticated: bool
    username: Optional[str] = None
    display_name: Optional[str] = None
    role: Optional[str] = None
    error: Optional[str] = None


def get_auth_mode() -> str:
    """Return active auth mode.

    Modes:
      - none: current behavior (role is selected in sidebar)
      - secrets: username/password validated against st.secrets
      - header: trust identity injected by a reverse proxy / SSO gateway via headers
    """
    return (os.getenv("OCSS_AUTH_MODE") or "none").strip().lower()


def _demo_password() -> str:
    """Demo-mode shared password.

    This is intentionally simple for management demos.
    Do not use demo mode for production security.
    """
    return (os.getenv("OCSS_DEMO_PASSWORD") or "demo").strip()


def _demo_users() -> Dict[str, Dict[str, str]]:
    """Built-in demo users for management demos (no external identity system required)."""
    return {
        "director": {"name": "Director User", "role": "Director"},
        "program": {"name": "Program Officer User", "role": "Program Officer"},
        "supervisor": {"name": "Supervisor User", "role": "Supervisor"},
        "support": {"name": "Support Officer User", "role": "Support Officer"},
        "it": {"name": "IT Administrator User", "role": "IT Administrator"},
    }


def _render_demo_login(supported_roles: Tuple[str, ...]) -> AuthResult:
    st.title("Sign in")
    st.caption("Demo mode (not production authentication).")

    users = _demo_users()
    options = list(users.keys())
    labels = [f"{users[k]['name']} ({users[k]['role']})" for k in options]
    default_index = 0

    with st.form("demo_login_form", clear_on_submit=False):
        picked = st.selectbox("Account", options=options, format_func=lambda k: f"{users[k]['name']} ({users[k]['role']})", index=default_index)
        password = st.text_input("Demo password", type="password")
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Sign in")
        with col2:
            continue_without = st.form_submit_button("Continue without signing in")

    if continue_without:
        return AuthResult(authenticated=False)

    if not submitted:
        st.stop()

    if password != _demo_password():
        return AuthResult(authenticated=False, error="Invalid demo password")

    record = users.get(picked) or {}
    display_name = record.get("name")
    role = record.get("role")

    if not role or role not in supported_roles:
        return AuthResult(authenticated=False, error="Role not supported")

    username = picked
    return AuthResult(authenticated=True, username=username, display_name=display_name, role=role)


def _pbkdf2_sha256_hash(password: str, salt: bytes, iterations: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def hash_password_pbkdf2_sha256(password: str, *, iterations: int = 260_000) -> str:
    """Create a portable password hash string.

    Format: pbkdf2_sha256$<iterations>$<salt_b64>$<hash_b64>
    """
    salt = os.urandom(16)
    digest = _pbkdf2_sha256_hash(password, salt, iterations)
    return "pbkdf2_sha256${}${}${}".format(
        iterations,
        base64.urlsafe_b64encode(salt).decode("ascii").rstrip("="),
        base64.urlsafe_b64encode(digest).decode("ascii").rstrip("="),
    )


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored hash.

    Supports:
      - pbkdf2_sha256$iterations$salt_b64$hash_b64
      - plain:<password> (dev-only escape hatch)
    """
    if not stored_hash:
        return False

    stored_hash = str(stored_hash)
    if stored_hash.startswith("plain:"):
        # Dev-only; do not use in production.
        return hmac.compare_digest(password, stored_hash[len("plain:") :])

    parts = stored_hash.split("$")
    if len(parts) != 4:
        return False
    algo, it_s, salt_b64, hash_b64 = parts
    if algo != "pbkdf2_sha256":
        return False

    try:
        iterations = int(it_s)
        salt = base64.urlsafe_b64decode(salt_b64 + "==")
        expected = base64.urlsafe_b64decode(hash_b64 + "==")
    except Exception:
        return False

    actual = _pbkdf2_sha256_hash(password, salt, iterations)
    return hmac.compare_digest(actual, expected)


def _get_headers() -> Dict[str, str]:
    """Best-effort access to request headers across Streamlit versions."""
    headers: Dict[str, str] = {}

    # Streamlit >= 1.29 provides st.context.headers
    try:
        ctx_headers = getattr(getattr(st, "context", None), "headers", None)
        if ctx_headers:
            for k, v in dict(ctx_headers).items():
                headers[str(k).lower()] = str(v)
    except Exception:
        pass

    return headers


def _header_auth() -> AuthResult:
    headers = _get_headers()

    user_header = (os.getenv("OCSS_AUTH_HEADER_USER") or "x-forwarded-user").strip().lower()
    name_header = (os.getenv("OCSS_AUTH_HEADER_NAME") or "x-forwarded-name").strip().lower()
    role_header = (os.getenv("OCSS_AUTH_HEADER_ROLE") or "x-forwarded-role").strip().lower()

    username = headers.get(user_header)
    display_name = headers.get(name_header) or username
    role = headers.get(role_header)

    if not username:
        return AuthResult(authenticated=False, error="Missing SSO user header")

    # Role may be injected by the gateway, or mapped by username via secrets.
    if not role:
        role = _get_user_record(username).get("role")

    if not role:
        return AuthResult(authenticated=False, username=username, display_name=display_name, error="No role mapped")

    return AuthResult(authenticated=True, username=username, display_name=display_name, role=role)


def _get_user_record(username: str) -> Dict[str, Any]:
    try:
        auth_cfg = st.secrets.get("auth", {})
        users = auth_cfg.get("users", {})
        return dict(users.get(username, {}))
    except Exception:
        return {}


def _secrets_auth(username: str, password: str) -> AuthResult:
    record = _get_user_record(username)
    if not record:
        return AuthResult(authenticated=False, error="Invalid username or password")

    stored = record.get("password_hash") or record.get("password")
    if not verify_password(password, str(stored or "")):
        return AuthResult(authenticated=False, error="Invalid username or password")

    role = (record.get("role") or "").strip()
    display_name = (record.get("name") or username).strip()
    if not role:
        return AuthResult(authenticated=False, error="User record missing role")

    return AuthResult(authenticated=True, username=username, display_name=display_name, role=role)


def is_authenticated() -> bool:
    return bool(st.session_state.get("auth_authenticated"))


def get_authenticated_identity() -> AuthResult:
    if not is_authenticated():
        return AuthResult(authenticated=False)
    return AuthResult(
        authenticated=True,
        username=st.session_state.get("auth_username"),
        display_name=st.session_state.get("auth_display_name"),
        role=st.session_state.get("auth_role"),
    )


def logout() -> None:
    for k in [
        "auth_authenticated",
        "auth_username",
        "auth_display_name",
        "auth_role",
        "current_user",
    ]:
        if k in st.session_state:
            del st.session_state[k]


def require_auth(supported_roles: Tuple[str, ...]) -> AuthResult:
    """Enforce authentication depending on OCSS_AUTH_MODE.

    Returns an AuthResult; if authenticated, role is guaranteed to be in supported_roles.
    """
    mode = get_auth_mode()

    if mode == "none":
        return AuthResult(authenticated=False)

    if mode == "demo":
        existing = get_authenticated_identity()
        if existing.authenticated:
            if existing.role not in supported_roles:
                return AuthResult(authenticated=False, username=existing.username, display_name=existing.display_name, error="Role not supported")
            return existing

        result = _render_demo_login(supported_roles)
        if not result.authenticated:
            if result.error:
                st.error(result.error)
                st.stop()
            # user chose to continue without signing in
            return AuthResult(authenticated=False)

        st.session_state["auth_authenticated"] = True
        st.session_state["auth_username"] = result.username
        st.session_state["auth_display_name"] = result.display_name
        st.session_state["auth_role"] = result.role
        st.session_state["current_user"] = result.display_name or result.username
        st.rerun()

    if mode == "header":
        result = _header_auth()
        if result.authenticated and result.role not in supported_roles:
            return AuthResult(authenticated=False, username=result.username, display_name=result.display_name, error="Role not supported")
        return result

    if mode == "secrets":
        # If already authenticated this session, return it.
        existing = get_authenticated_identity()
        if existing.authenticated:
            if existing.role not in supported_roles:
                return AuthResult(authenticated=False, username=existing.username, display_name=existing.display_name, error="Role not supported")
            return existing

        st.title("Sign in")
        st.caption("Use your county-issued credentials.")

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", key="login_username").strip()
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Sign in")

        if not submitted:
            st.stop()

        if not username or not password:
            st.error("Enter username and password.")
            st.stop()

        result = _secrets_auth(username, password)
        if not result.authenticated:
            st.error(result.error or "Sign-in failed")
            st.stop()

        if result.role not in supported_roles:
            st.error("Your account role is not enabled for this app.")
            st.stop()

        st.session_state["auth_authenticated"] = True
        st.session_state["auth_username"] = result.username
        st.session_state["auth_display_name"] = result.display_name
        st.session_state["auth_role"] = result.role
        st.session_state["current_user"] = result.display_name or result.username
        st.rerun()

    # Unknown mode
    return AuthResult(authenticated=False, error=f"Unknown auth mode: {mode}")
