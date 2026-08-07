from core.epigraphic_identity import (
    EpigraphicIdentity,
    Orientation,
    SignCategory,
)
from core.identity_registry import IdentityRegistry

registry = IdentityRegistry()

registry.register(
    EpigraphicIdentity(
        asl_id="ASL-SYN-001",
        category=SignCategory.BIRD,
        subcategory="avian",
        orientation=Orientation.RIGHT,
    )
)

registry.register(
    EpigraphicIdentity(
        asl_id="ASL-SYN-002",
        category=SignCategory.BIRD,
        subcategory="avian",
        orientation=Orientation.LEFT,
    )
)

registry.register(
    EpigraphicIdentity(
        asl_id="ASL-SYN-003",
        category=SignCategory.HUMAN,
        subcategory="figure",
        orientation=Orientation.RIGHT,
    )
)

assert registry.size() == 3

birds = registry.by_category(SignCategory.BIRD)
assert len(birds) == 2

right = registry.by_orientation(Orientation.RIGHT)
assert len(right) == 2

bird_right = registry.query(
    category=SignCategory.BIRD,
    orientation=Orientation.RIGHT,
)
assert len(bird_right) == 1

assert registry.get("ASL-SYN-001") is not None
assert registry.get("UNKNOWN") is None

print("PASS: registry size")
print("PASS: category query")
print("PASS: orientation query")
print("PASS: combined query")
print("PASS: identity lookup")
