import json

meta = json.load(open("validation/synthetic/metadata.json"))

meta["single_square"]["foreground_area"] = 1024
meta["two_squares"]["foreground_area"] = 256 + 256
meta["three_squares"]["foreground_area"] = 169 + 169 + 169
meta["square_with_hole"]["foreground_area"] = 1600 - 256
meta["ring"]["foreground_area"] = 1257 - 317
meta["three_rings"]["foreground_area"] = 3 * (221 - 61)

with open("validation/synthetic/metadata.json", "w") as f:
    json.dump(meta, f, indent=2)

print("Validation metadata updated")
