"""
SUID Audit Logger
Logs every entity lifecycle event for forensic traceability.
Writes to the sorabbyngo-security hash-chained audit ledger when available.
Falls back to Python logging if the security repo is not on the path.
Every action on every entity produces an immutable audit entry.
Audit IDs are themselves SUIDs — traceable and tamper-detectable.
"""
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

log = logging.getLogger("suid.audit")

# Try to import canonical AuditWriter from sorabbyngo-security
_AuditWriter = None
_SECURITY_PATHS = [
    Path(__file__).parent.parent.parent.parent / "sorabbyngo-security" / "audit",
    Path.home() / "sorabbyngo-security" / "audit",
    Path("/opt/sorabbyngo/security/audit"),
]
for _p in _SECURITY_PATHS:
    if (_p / "audit_writer.py").exists():
        if str(_p) not in sys.path:
            sys.path.insert(0, str(_p))
        try:
            from audit_writer import AuditWriter as _AuditWriter
            log.info(f"[suid.audit] Using canonical AuditWriter from {_p}")
            break
        except ImportError:
            pass

_writer = None

def _get_writer():
    global _writer
    if _writer is None and _AuditWriter is not None:
        try:
            import os
            node_id = os.environ.get("SORABBYNGO_NODE_ID", "unknown")
            _writer = _AuditWriter(node_id=node_id)
        except Exception as e:
            log.warning(f"[suid.audit] AuditWriter init failed: {e}")
    return _writer


class AuditLogger:
    """
    Logs entity lifecycle events tied to SUIDs.
    Every create, update, delete, and access is logged with its own SUID.
    Writes to hash-chained ledger when sorabbyngo-security is available.
    """
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

        # Write to hash-chained ledger if available
        writer = _get_writer()
        if writer is not None:
            try:
                writer.write(
                    actor=actor_id or "system",
                    action=f"data.{action.lower()}",
                    resource=f"entity/{entity_id}",
                    outcome="SUCCESS",
                    metadata={
                        "audit_id":   audit_id,
                        "action":     action,
                        "related_id": related_id,
                        "ip_address": ip_address,
                        **(metadata or {}),
                    },
                    service="identity-core",
                )
            except Exception as e:
                log.warning(f"[suid.audit] Chain write failed: {e}")

        log.info("[AUDIT] %s", json.dumps(entry, default=str))
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
