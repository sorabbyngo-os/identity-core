"""
SUID Audit Logger
Logs every entity lifecycle event for forensic traceability.
Integrates with CML audit ledger via NATS.

Every action on every entity produces an immutable audit entry.
Audit IDs are themselves SUIDs — traceable and tamper-detectable.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Optional

log = logging.getLogger("suid.audit")


class AuditLogger:
    """
    Logs entity lifecycle events tied to SUIDs.
    Every create, update, delete, and access is logged with its own SUID.
    """

    # Valid action types
    ACTIONS = {
        "CREATE", "READ", "UPDATE", "DELETE",
        "ACCESS", "EXPORT", "IMPORT",
        "ADMIT", "DISCHARGE", "TRANSFER",
        "ALERT", "ACKNOWLEDGE", "RESOLVE",
        "LOGIN", "LOGOUT", "AUTH_FAIL",
        "TRANSACTION", "CLAIM", "PAYMENT",
        "VERIFY", "REJECT", "APPROVE",
        "BOOT", "SHUTDOWN", "KERNEL_EVENT",
    }

    @staticmethod
    def log(
        action:     str,
        entity_id:  str,
        actor_id:   Optional[str] = None,
        related_id: Optional[str] = None,
        metadata:   Optional[dict] = None,
        ip_address: Optional[str] = None,
        region:     str = "KE047",
    ) -> dict:
        """
        Log an audit event. Returns the audit entry.

        Args:
            action:     One of ACTIONS (e.g. CREATE, READ, ALERT)
            entity_id:  SUID of the entity being acted on
            actor_id:   SUID of the user performing the action (DOC/NRS/USR)
            related_id: SUID of a related entity (e.g. patient linked to admission)
            metadata:   Additional context dict
            ip_address: Request IP address for network forensics
            region:     Region where action occurred
        """
        # Import here to avoid circular import
        from suid.generator import SUID
        from suid.registry.prefixes import PREFIX

        action = action.upper()
        if action not in AuditLogger.ACTIONS:
            log.warning("[AuditLogger] Unknown action type: %s", action)

        audit_id = SUID.generate(PREFIX.AUDIT, region)

        entry = {
            "audit_id":   audit_id,
            "action":     action,
            "entity_id":  entity_id,
            "actor_id":   actor_id,
            "related_id": related_id,
            "timestamp":  datetime.now(timezone.utc).isoformat(),
            "ip_address": ip_address,
            "region":     region,
            "metadata":   metadata or {},
        }

        log.info("[AUDIT] %s", json.dumps(entry))
        return entry

    # ── Convenience methods ───────────────────────────────────────────────

    @staticmethod
    def create(entity_id: str, actor_id: str = None, **kwargs) -> dict:
        return AuditLogger.log("CREATE", entity_id, actor_id, **kwargs)

    @staticmethod
    def read(entity_id: str, actor_id: str = None, **kwargs) -> dict:
        return AuditLogger.log("READ", entity_id, actor_id, **kwargs)

    @staticmethod
    def update(entity_id: str, actor_id: str = None, **kwargs) -> dict:
        return AuditLogger.log("UPDATE", entity_id, actor_id, **kwargs)

    @staticmethod
    def delete(entity_id: str, actor_id: str = None, **kwargs) -> dict:
        return AuditLogger.log("DELETE", entity_id, actor_id, **kwargs)

    @staticmethod
    def export(entity_id: str, actor_id: str = None, **kwargs) -> dict:
        return AuditLogger.log("EXPORT", entity_id, actor_id, **kwargs)

    @staticmethod
    def admit(patient_id: str, admission_id: str,
              actor_id: str = None, **kwargs) -> dict:
        return AuditLogger.log("ADMIT", patient_id, actor_id,
                               related_id=admission_id, **kwargs)

    @staticmethod
    def discharge(patient_id: str, admission_id: str,
                  actor_id: str = None, **kwargs) -> dict:
        return AuditLogger.log("DISCHARGE", patient_id, actor_id,
                               related_id=admission_id, **kwargs)

    @staticmethod
    def alert(alert_id: str, patient_id: str, **kwargs) -> dict:
        return AuditLogger.log("ALERT", alert_id,
                               related_id=patient_id, **kwargs)

    @staticmethod
    def transaction(txn_id: str, actor_id: str = None, **kwargs) -> dict:
        return AuditLogger.log("TRANSACTION", txn_id, actor_id, **kwargs)

    @staticmethod
    def login(user_id: str, ip_address: str = None, **kwargs) -> dict:
        return AuditLogger.log("LOGIN", user_id,
                               ip_address=ip_address, **kwargs)

    @staticmethod
    def auth_fail(user_id: str, ip_address: str = None, **kwargs) -> dict:
        return AuditLogger.log("AUTH_FAIL", user_id,
                               ip_address=ip_address, **kwargs)

    @staticmethod
    def verify(entity_id: str, actor_id: str = None, **kwargs) -> dict:
        return AuditLogger.log("VERIFY", entity_id, actor_id, **kwargs)
