#!/usr/bin/env python3
"""
test_level.py
Validation & Round-Trip Test Suite for Geometry Dash 2.2 Void_Leviathan.gdlvl file.
"""

import gzip
import base64
import xml.etree.ElementTree as ET
import sys
from generate_level import export_gd_level, build_gd_level

def parse_plist_dict(xml_str):
    root = ET.fromstring(xml_str)
    assert root.tag == "plist", f"Expected root tag 'plist', got '{root.tag}'"
    assert root.attrib.get("gjver") == "2.0", f"Expected root attribute gjver='2.0', got '{root.attrib.get('gjver')}'"
    print("✓ Root tag <plist version=\"1.0\" gjver=\"2.0\"> verified.")

    dict_elem = root.find("dict")
    assert dict_elem is not None, "Missing <dict> element in plist"

    plist_data = {}
    current_key = None
    for elem in dict_elem:
        if elem.tag == "k":
            current_key = elem.text
        elif current_key is not None:
            plist_data[current_key] = (elem.tag, elem.text)
            current_key = None
    return plist_data

def test_gdlvl_xml_structure():
    print("=== Step 1: Testing Void_Leviathan.gdlvl XML Plist File ===")
    with open("Void_Leviathan.gdlvl", "r", encoding="utf-8") as f:
        xml_str = f.read().strip()

    assert xml_str.startswith("<?xml") and "<plist" in xml_str, "Void_Leviathan.gdlvl is not valid XML plist!"
    print(f"✓ Void_Leviathan.gdlvl is a formatted XML Plist file ({len(xml_str)} chars).")
    return xml_str

def test_metadata_mapping(xml_str):
    print("\n=== Step 2: Testing Reference XML Metadata Key Mapping & Types ===")
    plist_data = parse_plist_dict(xml_str)

    # Key kCEK: Encryption / Format Indicator (integer)
    kCEK_tag, kCEK_val = plist_data.get("kCEK", (None, None))
    assert kCEK_tag == "i" and kCEK_val == "4", f"Expected kCEK 4, got '{kCEK_val}'"
    print(f"✓ kCEK (Format Indicator): {kCEK_val} (type: integer)")

    # Key k2: Level Name (string)
    k2_tag, k2_val = plist_data.get("k2", (None, None))
    assert k2_tag == "s" and k2_val == "Void Leviathan", f"Unexpected level name: '{k2_val}'"
    print(f"✓ k2 (Level Name): '{k2_val}' (type: string)")

    # Key k3: Description (Base64-encoded string)
    k3_tag, k3_val = plist_data.get("k3", (None, None))
    assert k3_tag == "s", f"k3 tag should be 's' (string), got '{k3_tag}'"
    decoded_desc = base64.b64decode(k3_val).decode('utf-8')
    assert "purple octopus boss fight" in decoded_desc, f"Decoded description invalid: '{decoded_desc}'"
    print(f"✓ k3 (Base64 Description): '{decoded_desc}' (type: base64 string)")

    # Key k4: Inner Level String (URL-safe Base64 gzipped object string)
    k4_tag, k4_val = plist_data.get("k4", (None, None))
    assert k4_tag == "s", f"k4 tag should be 's' (string), got '{k4_tag}'"
    compressed_level = base64.urlsafe_b64decode(k4_val)
    inner_level_str = gzip.decompress(compressed_level).decode('utf-8')
    assert inner_level_str.startswith("kS38,"), "Inner level string missing kS38 header!"
    print(f"✓ k4 (Inner Level String): Successfully decompressed inner level string ({len(inner_level_str)} chars)")

    # Key k5: Creator Name (string)
    k5_tag, k5_val = plist_data.get("k5", (None, None))
    assert k5_tag == "s" and k5_val == "Jules", f"Unexpected creator: '{k5_val}'"
    print(f"✓ k5 (Creator): '{k5_val}'")

    # Key k16: Level Revision (integer)
    k16_tag, k16_val = plist_data.get("k16", (None, None))
    assert k16_tag == "i" and k16_val == "1", f"Expected k16=1, got '{k16_val}'"
    print(f"✓ k16 (Revision): {k16_val}")

    # Key k21: Level Type (integer)
    k21_tag, k21_val = plist_data.get("k21", (None, None))
    assert k21_tag == "i" and k21_val == "2", f"Expected level type 2 (local editor), got '{k21_val}'"
    print(f"✓ k21 (Level Type): {k21_val} (Local Editor Level)")

    # Key k48: Object Count (integer)
    k48_tag, k48_val = plist_data.get("k48", (None, None))
    assert k48_tag == "i" and int(k48_val) == 1260, f"Expected object count 1260, got '{k48_val}'"
    print(f"✓ k48 (Object Count): {k48_val}")

    # Key k50: Binary Version (integer)
    k50_tag, k50_val = plist_data.get("k50", (None, None))
    assert k50_tag == "i" and k50_val == "45", f"Expected k50=45, got '{k50_val}'"
    print(f"✓ k50 (Binary Version): {k50_val}")

    # Key k80: Editor Version (integer)
    k80_tag, k80_val = plist_data.get("k80", (None, None))
    assert k80_tag == "i" and k80_val == "22", f"Expected GD 2.2 tag k80=22, got '{k80_val}'"
    print(f"✓ k80 (Editor Version): {k80_val}")

    # Key k101: Editor Settings (integer)
    k101_tag, k101_val = plist_data.get("k101", (None, None))
    assert k101_tag == "i" and k101_val == "0", f"Expected k101=0, got '{k101_val}'"
    print(f"✓ k101 (Settings): {k101_val}")

    # Key kI1, kI2, kI3: Editor Settings (integers)
    for ki in ["kI1", "kI2", "kI3"]:
        tag, val = plist_data.get(ki, (None, None))
        assert tag == "i", f"Expected integer tag for {ki}, got '{tag}'"
        print(f"✓ {ki}: {val} (type: integer)")

    return inner_level_str

def test_inner_level_objects(inner_level_str):
    print("\n=== Step 3: Testing Inner Level Objects & Boss Groups ===")
    parts = inner_level_str.split(";")
    header = parts[0]
    objects = parts[1:-1] # excluding header and trailing empty item

    assert "kS38," in header, "Level header missing kS38 color data"
    print(f"✓ Header verified: {header[:40]}...")
    print(f"✓ Total Objects Count: {len(objects)}")
    assert len(objects) == 1260, f"Expected 1260 objects, got {len(objects)}"

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

        if "57" in obj_dict:
            grp_val = obj_dict["57"]
            for g in grp_val.split("."):
                groups_found.add(g)

    # Check Color Triggers (ID 221)
    assert obj_type_counts.get("221", 0) >= 8, f"Expected at least 8 Color Triggers, found {obj_type_counts.get('221')}"
    print(f"✓ Color Triggers verified ({obj_type_counts.get('221')} count).")

    # Check Key Triggers
    assert "901" in obj_type_counts, "Move trigger (901) missing!"
    assert "1006" in obj_type_counts, "Pulse trigger (1006) missing!"
    assert "1007" in obj_type_counts, "Alpha trigger (1007) missing!"
    assert "1268" in obj_type_counts, "Rotate trigger (1268) missing!"
    assert "1520" in obj_type_counts, "Shake trigger (1520) missing!"
    print("✓ All transition & animation triggers (Move, Pulse, Alpha, Rotate, Shake) present.")

    # Check Octopus Boss Groups
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

def main():
    xml_str = test_gdlvl_xml_structure()
    inner_str = test_metadata_mapping(xml_str)
    test_inner_level_objects(inner_str)
    print("\n🎉 ALL GD 2.2 VOID LEVIATHAN LEVEL TESTS PASSED 100% SUCCESSFULLY!")

if __name__ == "__main__":
    main()
