from __future__ import annotations

from typing import Dict, Optional, Iterable

from core.sign import SignReference


class SignLibrary:
    """
    Universal Sign Registry

    AncientScriptLab v8

    Stores only objective information about signs.

    No semantics.
    No translations.
    No hypotheses.
    """

    def __init__(self):

        self._signs: Dict[int, SignReference] = {}

    # --------------------------------------------------

    def add(self, sign: SignReference):

        self._signs[sign.id] = sign

    # --------------------------------------------------

    def get(self, sign_id: int) -> Optional[SignReference]:

        return self._signs.get(sign_id)

    # --------------------------------------------------

    def exists(self, sign_id: int) -> bool:

        return sign_id in self._signs

    # --------------------------------------------------

    def remove(self, sign_id: int):

        if sign_id in self._signs:
            del self._signs[sign_id]

    # --------------------------------------------------

    def clear(self):

        self._signs.clear()

    # --------------------------------------------------

    def all(self) -> Iterable[SignReference]:

        return self._signs.values()

    # --------------------------------------------------

    def ids(self):

        return sorted(self._signs.keys())

    # --------------------------------------------------

    def summary(self):

        return {
            "total_signs": len(self._signs)
        }

    # --------------------------------------------------

    def __len__(self):

        return len(self._signs)

    # --------------------------------------------------

    def __contains__(self, item):

        return item in self._signs

