"""
SUID Audit Logger
Logs every entity creation and action for forensic traceability.
Integrates with CML audit ledger via NATS.
"""
import json
import logging
from datetime import datetime, timezone
from typing import Optional

log = logging.getLogger(__name__)


class AuditLogger:
    """
    Logs entity lifecycle events tied to SUIDs.
    Every create, update, delete, and access is logged.
    """

    @staticmethod
    def log(
        action: str,
        entity_id: str,
        actor_id: Optional[str] = None,
        related_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        ip_address: Optional[str] = None,
    ) -> dict:
        """
        Log an audit event.

        Args:
            action:     CREATE | READ | UPDATE | DELETE | ACCESS | ALERT | ADMIT | DISCHARGE
            entity_id:  SUID of the entity being acted on
            actor_id:   SUID of the user performing the action
            related_id: SUID of a related entity (e.g. patient linked to admission)
            metadata:   Additional context
            ip_address: Request IP address
        """
        entry = {
            "audit_id":   f"AUD-{datetime.now(timezone.utc).strftime('%Y%m%d')}-KE047-{entity_id[-6:]}",
            "action":     action,
            "entity_id":  entity_id,
            "actor_id":   actor_id,
            "related_id": related_id,
            "timestamp":  datetime.now(timezone.utc).isoformat(),
            "ip_address": ip_address,
            "metadata":   metadata or {},
        }

        log.info("[AUDIT] %s", json.dumps(entry))
        return entry

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
    def admit(patient_id: str, admission_id: str, actor_id: str = None, **kwargs) -> dict:
        return AuditLogger.log("ADMIT", patient_id, actor_id,
                               related_id=admission_id, **kwargs)

    @staticmethod
    def alert(alert_id: str, patient_id: str, **kwargs) -> dict:
        return AuditLogger.log("ALERT", alert_id,
                               related_id=patient_id, **kwargs)

    @staticmethod
    def transaction(txn_id: str, actor_id: str = None, **kwargs) -> dict:
        return AuditLogger.log("TRANSACTION", txn_id, actor_id, **kwargs)
