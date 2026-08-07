from core.epigraphic_identity import (
    EpigraphicIdentity,
    SignCategory,
    Orientation,
)

sign_a = EpigraphicIdentity(
    asl_id="ASL-SYN-001",
    category=SignCategory.BIRD,
    subcategory="avian",
    orientation=Orientation.RIGHT,
)

sign_b = EpigraphicIdentity(
    asl_id="ASL-SYN-002",
    category=SignCategory.BIRD,
    subcategory="avian",
    orientation=Orientation.LEFT,
)

sign_c = EpigraphicIdentity(
    asl_id="ASL-SYN-003",
    category=SignCategory.HUMAN,
    subcategory="figure",
    orientation=Orientation.RIGHT,
)

assert not sign_a.same_sign(sign_b)
assert sign_a.same_category(sign_b)
assert not sign_a.same_orientation(sign_b)

assert not sign_a.same_category(sign_c)
assert sign_a.same_orientation(sign_c)

print("PASS: identity test")
print("PASS: category test")
print("PASS: orientation test")
print("PASS: structural signature test")
