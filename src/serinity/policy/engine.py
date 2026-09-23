from typing import Dict, Optional

class PolicyEngine:
    """Deterministic security policy engine for controlling agent permissions."""

    DEFAULT_PERMISSIONS = {
        "conversation": True,
        "python_sandbox": True,
        "sandbox_execution": True,
        "file_reader": True,
        "read_file": True,
        "local_research": True,
        "code_generation": True,
    }

    IMMUTABLE_DENIALS = {
        "root_access",
        "system_exec",
        "hard_deny",
        "delete_data",
        "purchases",
        "system_modification",
    }

    def __init__(self, custom_permissions: Optional[Dict[str, bool]] = None):
        self.permissions = self.DEFAULT_PERMISSIONS.copy()
        if custom_permissions:
            self.permissions.update(custom_permissions)

    def is_allowed(self, action_or_permission: str) -> bool:
        if action_or_permission in self.IMMUTABLE_DENIALS:
            return False
        return self.permissions.get(action_or_permission, False)

    def set_permission(self, permission: str, allowed: bool) -> None:
        if permission not in self.IMMUTABLE_DENIALS:
            self.permissions[permission] = allowed

    def update_permissions(self, new_permissions: Dict[str, bool]) -> None:
        for perm, allowed in new_permissions.items():
            self.set_permission(perm, allowed)
