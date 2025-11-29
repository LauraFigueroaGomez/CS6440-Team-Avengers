from typing import Any, Dict, List, Union
from datetime import datetime
from app.models.immunization import ImmunizationCreate
from app.services.data_parser_service import DataParserService

JsonLike = Union[Dict[str, Any], List[Any], str, None]

class NormalizationService:
    HL7_HINTS = ("MSH|", "PID|", "RXA|")

    def __init__(self) -> None:
        self.parser = DataParserService()

    def _maybe_hl7(self, s: str) -> bool:
        s = s.strip()
        return any(h in s for h in self.HL7_HINTS)

    def _maybe_xml(self, s: str) -> bool:
        return s.lstrip().startswith("<")

    def _unwrap_json_wrapper(self, payload: Dict[str, Any]) -> Any:
        """Prefer common wrapper keys, especially 'data'."""
        for k in ("data", "hl7", "HL7", "xml", "XML", "soap", "SOAP",
                  "payload", "message", "body", "content"):
            if k in payload:
                return payload[k]
        return payload

    def _parse_one(self, payload: JsonLike) -> Dict[str, Any]:
        # If we get a list, treat the first element as a single record
        if isinstance(payload, list):
            if not payload:
                raise ValueError("Empty list payload for normalization")
            return self._parse_one(payload[0])

        # String payload: detect HL7 vs XML vs JSON
        if isinstance(payload, str):
            if self._maybe_hl7(payload):
                return self.parser.parse_hl7(payload)
            if self._maybe_xml(payload):
                return self.parser.parse_xml(payload)
            return self.parser.parse_rest_json(payload)

        # Dict payload: could be a direct JSON record
        if isinstance(payload, dict):
            inner = self._unwrap_json_wrapper(payload)

            # In case someone passes a wrapper-within-wrapper or weird structure
            if isinstance(inner, list):
                if not inner:
                    raise ValueError("Empty list inside JSON wrapper for normalization")
                return self._parse_one(inner[0])

            if isinstance(inner, str):
                if self._maybe_hl7(inner):
                    return self.parser.parse_hl7(inner)
                if self._maybe_xml(inner):
                    return self.parser.parse_xml(inner)
                return self.parser.parse_rest_json(inner)

            if isinstance(inner, dict):
                # Normal REST-style JSON object
                return self.parser.parse_rest_json(inner)

            raise ValueError(f"Unsupported inner payload type: {type(inner)}")

        raise ValueError(f"Unsupported payload type for normalization: {type(payload)}")

    def aggregate(self, **state_payloads: Any) -> List[ImmunizationCreate]:
        out: List[ImmunizationCreate] = []

        for state_code, payload in state_payloads.items():
            if payload is None:
                continue

            # NEW: unwrap top-level wrappers like {"source": "NY", "format": "...", "data": [...]}
            if isinstance(payload, dict):
                payload = self._unwrap_json_wrapper(payload)

            # Now payload can be:
            #  - list of HL7 strings    (NY)
            #  - list of XML strings    (NJ)
            #  - list of dicts (JSON)   (PA)
            #  - or a single item
            items = payload if isinstance(payload, list) else [payload]

            for item in items:
                parsed = self._parse_one(item)
                imm = self.parser.to_immunization_create(parsed)

                # attach source_state from the key (NY/NJ/PA)
                try:
                    imm.source_state = state_code
                except Exception:
                    pass

                # Try to coerce date_administered from raw parsed payload if missing
                if imm.date_administered is None:
                    raw = parsed.get("immunization", {}).get("date_administered")
                    if isinstance(raw, str):
                        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%Y%m%d%H%M%S"):
                            try:
                                imm.date_administered = datetime.strptime(raw, fmt).date()
                                break
                            except Exception:
                                pass

                out.append(imm)

        return out
