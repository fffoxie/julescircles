#!/usr/bin/env python3
"""
test_level.py
Validation script for Geometry Dash .gmd level file and level string integrity.
"""

import gzip
import base64
import xml.etree.ElementTree as ET
import sys

def test_level_file():
    print("=== Testing Abyssal_Kraken.gmd ===")

    # 1. Parse XML
    tree = ET.parse("Abyssal_Kraken.gmd")
    root = tree.getroot()
    assert root.tag == "plist", f"Expected root tag 'plist', got '{root.tag}'"
    print("✓ Valid XML plist root element.")

    # 2. Extract key-value pairs from plist dict
    dict_elem = root.find("dict")
    assert dict_elem is not None, "Missing <dict> element in plist"

    plist_data = {}
    current_key = None
    for elem in dict_elem:
        if elem.tag == "k":
            current_key = elem.text
        elif current_key is not None:
            plist_data[current_key] = elem.text
            current_key = None

    print(f"✓ Parsed plist keys: {list(plist_data.keys())}")
    assert plist_data.get("k1") == "Abyssal Kraken", f"Unexpected level name: {plist_data.get('k1')}"
    print(f"✓ Level Name (k1): {plist_data.get('k1')}")

    # 3. Decode base64 gzip level string from k4
    k4_b64 = plist_data.get("k4")
    assert k4_b64 is not None and len(k4_b64) > 0, "k4 level string is empty!"

    compressed_bytes = base64.b64decode(k4_b64)
    decompressed_str = gzip.decompress(compressed_bytes).decode('utf-8')
    print(f"✓ Successfully decompressed k4 level string ({len(decompressed_str)} chars).")

    # 4. Verify level header and objects
    parts = decompressed_str.split(";")
    header = parts[0]
    objects = parts[1:-1] # excluding header and trailing empty item

    assert "kS38," in header, "Level header missing kS38 color data"
    print(f"✓ Header verified: {header[:40]}...")
    print(f"✓ Total Objects Count: {len(objects)}")
    assert len(objects) >= 300, f"Object count too low ({len(objects)}), expected rich level design."

    # 5. Parse objects and verify object types & groups
    obj_type_counts = {}
    groups_found = set()

    for obj_str in objects:
        if not obj_str.strip():
            continue
        pairs = obj_str.split(",")
        obj_dict = {}
        for i in range(0, len(pairs)-1, 2):
            obj_dict[pairs[i]] = pairs[i+1]

        obj_id = obj_dict.get("1")
        if obj_id:
            obj_type_counts[obj_id] = obj_type_counts.get(obj_id, 0) + 1

        # Check group IDs (key 57)
        if "57" in obj_dict:
            grp_val = obj_dict["57"]
            for g in grp_val.split("."):
                groups_found.add(g)

    print(f"✓ Object type diversity count: {len(obj_type_counts)} unique object IDs.")

    # Check Color Triggers (ID 221)
    assert obj_type_counts.get("221", 0) >= 8, f"Expected at least 8 Color Triggers, found {obj_type_counts.get('221')}"
    print(f"✓ Color Triggers verified ({obj_type_counts.get('221')} count).")

    # Check Key Triggers (Move 901, Pulse 1006, Alpha 1007, Rotate 1268, Shake 1520)
    assert "901" in obj_type_counts, "Move trigger (901) missing!"
    assert "1006" in obj_type_counts, "Pulse trigger (1006) missing!"
    assert "1007" in obj_type_counts, "Alpha trigger (1007) missing!"
    assert "1268" in obj_type_counts, "Rotate trigger (1268) missing!"
    assert "1520" in obj_type_counts, "Shake trigger (1520) missing!"
    print("✓ All transition & animation triggers (Move, Pulse, Alpha, Rotate, Shake) present.")

    # Check Octopus Boss Groups (10: Head, 11: Tentacle 1, 12: Tentacle 2, 13: Tentacle 3, 14: Tentacle 4, 15: Eyes, 16: Ink Cannon)
    expected_boss_groups = {"10", "11", "12", "13", "14", "15", "16"}
    for grp in expected_boss_groups:
        assert grp in groups_found, f"Boss group {grp} not found in level objects!"
    print(f"✓ Boss fight groups verified: {expected_boss_groups.intersection(groups_found)}")

    # Check Portals
    assert "13" in obj_type_counts, "Cube portal (13) missing"
    assert "12" in obj_type_counts, "Ship portal (12) missing"
    assert "201" in obj_type_counts, "Wave portal (201) missing"
    assert "1755" in obj_type_counts, "Spider portal (1755) missing"
    print("✓ Game mode portals (Cube, Ship, Wave, Spider) verified.")

    print("\n🎉 ALL LEVEL VERIFICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_level_file()
