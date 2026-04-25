"""
SUID NATS Bridge
Publishes identity events to the Sorabbyngo mesh via NATS.
Every entity creation, audit event, and forensic alert
flows through the sentinel for ecosystem-wide traceability.

Subjects published:
  sorabbyngo.identity.created    — new entity ID created
  sorabbyngo.identity.audit      — audit log entry
  sorabbyngo.identity.tampered   — tamper detection alert
  sorabbyngo.cyberwall.alert     — security escalation
"""
import json
import logging
import os
from datetime import datetime, timezone
from typing import Optional

log = logging.getLogger("suid.nats_bridge")
NATS_URL = os.environ.get("NATS_URL", "nats://localhost:4222")


def _get_nats():
    try:
        import nats
        return nats
    except ImportError:
        return None


class SUIDBridge:
    """
    Async NATS bridge for SUID events.
    Used by Novela, Byngox, CML, and Cyberwall
    to publish identity events into the mesh.
    """

    def __init__(self, service_name: str = "identity-core"):
        self._service = service_name
        self._nc      = None

    async def connect(self) -> bool:
        nats = _get_nats()
        if not nats:
            log.warning("nats-py not installed — bridge disabled")
            return False
        try:
            self._nc = await nats.connect(
                NATS_URL,
                name=self._service,
                reconnect_time_wait=5,
                max_reconnect_attempts=-1,
            )
            log.info("SUID bridge connected to NATS")
            return True
        except Exception as e:
            log.warning("NATS connect failed: %s", e)
            return False

    async def close(self):
        if self._nc:
            await self._nc.close()

    async def _publish(self, subject: str, data: dict):
        if not self._nc:
            return
        try:
            await self._nc.publish(subject, json.dumps(data).encode())
        except Exception as e:
            log.debug("Publish error [%s]: %s", subject, e)

    async def on_created(self, suid: str, actor_id: Optional[str] = None,
                         region: str = "KE047"):
        """Publish entity creation event."""
        from suid.generator import SUID
        parsed = SUID.parse(suid)
        await self._publish("sorabbyngo.identity.created", {
            "suid":        suid,
            "entity_type": parsed.get("prefix_name"),
            "region":      region,
            "actor_id":    actor_id,
            "service":     self._service,
            "timestamp":   datetime.now(timezone.utc).isoformat(),
        })

    async def on_audit(self, entry: dict):
        """Publish audit log entry."""
        await self._publish("sorabbyngo.identity.audit", {
            **entry,
            "service":   self._service,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    async def on_tampered(self, suid: str, context: str = ""):
        """Escalate tamper detection to Cyberwall."""
        from suid.generator import SUID
        parsed = SUID.parse(suid)
        log.critical("TAMPERED SUID detected: %s", suid)

        # Publish to identity subject
        await self._publish("sorabbyngo.identity.tampered", {
            "suid":        suid,
            "entity_type": parsed.get("prefix_name"),
            "region":      parsed.get("region"),
            "context":     context,
            "service":     self._service,
            "timestamp":   datetime.now(timezone.utc).isoformat(),
        })

        # Escalate to Cyberwall as security incident
        await self._publish("sorabbyngo.cyberwall.alert", {
            "level":       "CRITICAL",
            "threat_type": "SUID_TAMPERING",
            "description": f"Tampered SUID detected: {suid} ({parsed.get('prefix_name')})",
            "source":      "identity-core",
            "data": {
                "suid":        suid,
                "entity_type": parsed.get("prefix_name"),
                "region":      parsed.get("region"),
                "context":     context,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
