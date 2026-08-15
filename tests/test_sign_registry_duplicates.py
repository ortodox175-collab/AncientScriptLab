from core.registry.sign_registry import SignRecord, SignRegistry


reg = SignRegistry()

a = SignRecord(
    sign_id="SIGN-001",
    category="reference",
    image_path="a.png",
)

reg.add(a)

assert reg.get("SIGN-001") is a

try:
    reg.add(
        SignRecord(
            sign_id="SIGN-001",
            category="other",
        )
    )
    raise AssertionError("Duplicate sign_id was accepted")
except ValueError:
    pass

replacement = SignRecord(
    sign_id="SIGN-001",
    category="reference",
    image_path="b.png",
)

reg.replace(replacement)

assert reg.get("SIGN-001").image_path == "b.png"

try:
    reg.replace(
        SignRecord(
            sign_id="SIGN-999",
            category="reference",
        )
    )
    raise AssertionError("Replacement of missing record was accepted")
except KeyError:
    pass

print("SIGN REGISTRY DUPLICATE POLICY: PASS")
