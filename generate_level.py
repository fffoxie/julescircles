#!/usr/bin/env python3
"""
generate_level.py
Generates an Insane Realism Geometry Dash 2.2 level according to the proven working GD .gdlvl reference schema:

Working Reference Schema:
- Root element: <plist version="1.0" gjver="2.0">
- kCEK: Encryption / Format Indicator (integer: 4)
- k2: Level Name (string: "Abyssal Kraken")
- k3: Description (Base64-encoded string)
- k4: Inner Level String (URL-safe Base64 gzipped level object string)
- k5: Creator Name (string: "Jules")
- k16: Level Revision (integer: 1)
- k21: Level Type (integer: 2 = Local Editor Level)
- k48: Object Count (integer: 1260)
- k50: Binary Version (integer: 45)
- k80: Editor Version (integer: 22 = GD 2.2)
- k101: Editor Settings (integer: 0)
- kI1: Camera Zoom Setting (integer: 0)
- kI2: Camera Offset Setting (integer: 0)
- kI3: Camera Opacity Setting (integer: 1)

Outer Export Pipeline (.gdlvl):
  XML UTF-8 bytes -> Gzip compression -> URL-safe Base64 encoding -> .gdlvl file

Outputs:
- Abyssal_Kraken.gdlvl (Outer Gzip + URL-safe Base64 encoded XML Plist)
- Abyssal_Kraken.gmd (Raw XML Plist format)
- level_string.txt (Raw uncompressed level object string)
"""

import gzip
import base64

def build_gd_level():
    objects = []

    def add_obj(obj_dict):
        # Convert dictionary of keys to GD object string: k1,v1,k2,v2,...
        parts = []
        for k, v in obj_dict.items():
            parts.append(f"{k},{v}")
        objects.append(",".join(parts))

    # --- COLOR SETUP / TRIGGERS ---
    # Setup Color Triggers at X=0
    # Color 1: BG - Deep Abyssal Blue (0, 5, 20)
    add_obj({1: 221, 2: 0, 3: 0, 23: 1000, 7: 0, 8: 5, 9: 20, 10: 0})
    # Color 2: Ground - Dark Violet (10, 5, 25)
    add_obj({1: 221, 2: 0, 3: 0, 23: 1001, 7: 10, 8: 5, 9: 25, 10: 0})
    # Color 3: Main Structures - Dark Basalt (20, 20, 35)
    add_obj({1: 221, 2: 0, 3: 0, 23: 3, 7: 20, 8: 20, 9: 35, 10: 0})
    # Color 4: Bioluminescent Glow - Electric Aqua (0, 255, 220)
    add_obj({1: 221, 2: 0, 3: 0, 23: 4, 7: 0, 8: 255, 9: 220, 10: 0})
    # Color 5: Purple Octopus Body - Deep Royal Purple (140, 20, 210)
    add_obj({1: 221, 2: 0, 3: 0, 23: 5, 7: 140, 8: 20, 9: 210, 10: 0})
    # Color 6: Octopus Details / Suction Cups - Neon Magenta (255, 40, 180)
    add_obj({1: 221, 2: 0, 3: 0, 23: 6, 7: 255, 8: 40, 9: 180, 10: 0})
    # Color 7: Octopus Glowing Eyes - Electric Gold (255, 220, 30)
    add_obj({1: 221, 2: 0, 3: 0, 23: 7, 7: 255, 8: 220, 9: 30, 10: 0})
    # Color 8: Alarm / Laser / Ink - Crimson Red (240, 20, 50)
    add_obj({1: 221, 2: 0, 3: 0, 23: 8, 7: 240, 8: 20, 9: 50, 10: 0})

    # --- SECTION 1: THE ABYSSAL TRENCH (X = 0 to 1800) ---
    # Start Portal & Speed
    add_obj({1: 13, 2: 30, 3: 100}) # Cube Portal
    add_obj({1: 22, 2: 60, 3: 100}) # 1x Speed Portal

    # Ground & Ceiling Basalt Platforms (Realistic layered blocks)
    for x in range(0, 1800, 30):
        # Floor
        add_obj({1: 1, 2: x, 3: 15, 21: 3, 24: 1, 25: 1})
        add_obj({1: 2, 2: x, 3: 30, 21: 4, 24: 3, 25: 2}) # Top outline with aqua glow
        # Ceiling
        add_obj({1: 1, 2: x, 3: 345, 21: 3, 24: 1, 25: 1})
        add_obj({1: 2, 2: x, 3: 330, 21: 4, 24: 3, 25: 2, 5: 1})

    # Background Parallax Oceanic Pillars & Glowing Corals
    for x in range(100, 1700, 150):
        # Parallax Rock Pillar
        for y in range(45, 315, 30):
            add_obj({1: 467, 2: x, 3: y, 21: 3, 24: -5, 25: -10, 32: 1.2, 35: 0.6, 57: 2})
        # Bioluminescent Glow Orb on top/bottom
        add_obj({1: 503, 2: x, 3: 60, 21: 4, 24: -3, 32: 1.5, 35: 0.8})
        add_obj({1: 503, 2: x, 3: 300, 21: 4, 24: -3, 32: 1.5, 35: 0.8})

    # Gameplay Obstacles (Spikes, Jump Pads, Orbs, Ship Portal)
    for x in range(300, 600, 120):
        # Spikes
        add_obj({1: 4, 2: x, 3: 45, 21: 4})
        # Yellow Orb above
        add_obj({1: 47, 2: x - 30, 3: 105})

    # Gamemode Switch to Ship at X=600
    add_obj({1: 12, 2: 600, 3: 180}) # Ship Portal
    add_obj({1: 23, 2: 630, 3: 180}) # 2x Speed

    # Ship Section Tunnel with Realistic Slopes
    for x in range(650, 1200, 200):
        # Top hanging slate overhangs
        add_obj({1: 211, 2: x, 3: 280, 21: 3, 5: 1})
        add_obj({1: 1, 2: x + 30, 3: 280, 21: 3})
        add_obj({1: 212, 2: x + 60, 3: 280, 21: 3, 5: 1})
        add_obj({1: 4, 2: x + 30, 3: 250, 21: 8, 5: 1}) # Hanging Crimson Hazard Spike

        # Bottom underwater slate reefs
        add_obj({1: 211, 2: x + 80, 3: 60, 21: 3})
        add_obj({1: 1, 2: x + 110, 3: 60, 21: 3})
        add_obj({1: 212, 2: x + 140, 3: 60, 21: 3})
        add_obj({1: 4, 2: x + 110, 3: 90, 21: 4})

    # Gamemode Switch to Wave at X=1200
    add_obj({1: 201, 2: 1200, 3: 180}) # Wave Portal

    # Tight Wave Diamond Formations
    for x in range(1250, 1750, 150):
        # Upper wave block cluster
        add_obj({1: 1, 2: x, 3: 240, 21: 3})
        add_obj({1: 1, 2: x + 30, 3: 240, 21: 3})
        add_obj({1: 2, 2: x + 15, 3: 225, 21: 4})
        # Lower wave block cluster
        add_obj({1: 1, 2: x + 75, 3: 100, 21: 3})
        add_obj({1: 1, 2: x + 105, 3: 100, 21: 3})
        add_obj({1: 2, 2: x + 90, 3: 115, 21: 4})

    # --- TRANSITION 1: ABYSSAL RIFT COLLAPSE (X = 1800 to 2200) ---
    # Fast 3x Speed Portal
    add_obj({1: 24, 2: 1800, 3: 180})

    # Heavy Seismic Shake Trigger
    add_obj({1: 1520, 2: 1805, 3: 180, 84: 85, 85: 5, 88: 1.2}) # Shake: Strength 85, Duration 1.2s

    # Flash Pulse Trigger (Cyan to Bright White to Dark Purple)
    add_obj({1: 1006, 2: 1810, 3: 180, 97: 0, 98: 1000, 7: 255, 8: 255, 9: 255, 99: 0.1, 100: 0.2, 101: 0.5})

    # Screen Wipe Shutter Blocks (Group 1) moving rapidly across screen
    for y in range(0, 360, 30):
        add_obj({1: 467, 2: 1500, 3: y, 21: 3, 24: 9, 25: 100, 32: 2.0, 57: 1})
    # Move Trigger for Screen Wipe
    add_obj({1: 901, 2: 1815, 3: 180, 51: 1, 85: 800, 86: 0, 88: 0.5, 87: 6}) # Move X +80 block distance, Bounce Easing

    # Background color shift to Deep Trench Void
    add_obj({1: 221, 2: 1820, 3: 180, 23: 1000, 7: 5, 8: 0, 9: 15, 10: 0.5}) # BG -> Crimson Void Dark Blue

    # --- SECTION 2: NEON TRENCH RUSH (X = 2200 to 3900) ---
    # Fast Wave gameplay through dynamic glowing neon trench
    add_obj({1: 201, 2: 2200, 3: 180}) # Wave Portal

    # Basalt & Cyber Slate Trenches
    for x in range(2200, 3900, 30):
        # Floor
        add_obj({1: 1, 2: x, 3: 15, 21: 3})
        add_obj({1: 2, 2: x, 3: 30, 21: 8}) # Top outline crimson
        # Ceiling
        add_obj({1: 1, 2: x, 3: 345, 21: 3})
        add_obj({1: 2, 2: x, 3: 330, 21: 8, 5: 1})

    # Dynamic Obstacles & Pulsing Lasers
    for x in range(2350, 3800, 180):
        # Top laser barrier
        add_obj({1: 4, 2: x, 3: 280, 21: 8, 5: 1})
        add_obj({1: 503, 2: x, 3: 280, 21: 8, 32: 1.2})
        # Bottom laser barrier
        add_obj({1: 4, 2: x + 90, 3: 80, 21: 8})
        add_obj({1: 503, 2: x + 90, 3: 80, 21: 8, 32: 1.2})
        # Strobe Warning Pulse
        add_obj({1: 1006, 2: x - 30, 3: 180, 97: 0, 98: 1000, 7: 240, 8: 20, 9: 50, 99: 0.05, 100: 0.1, 101: 0.1})

    # Spider Gamemode Transition at X=3200
    add_obj({1: 1755, 2: 3200, 3: 180}) # Spider Portal

    # --- TRANSITION 2: KRAKEN AWAKENING / ARENA LOCK (X = 3900 to 4300) ---
    # Slowdown Portal
    add_obj({1: 25, 2: 3900, 3: 180}) # 0.5x Speed

    # Gamemode Ship / Robot into Boss Lair
    add_obj({1: 12, 2: 3930, 3: 180}) # Ship Portal

    # Alarm Strobes & Audio/Visual Tremors
    for delay_x in range(3950, 4250, 60):
        add_obj({1: 1006, 2: delay_x, 3: 180, 97: 0, 98: 1000, 7: 255, 8: 0, 9: 100, 99: 0.05, 100: 0.15, 101: 0.1})
        add_obj({1: 1520, 2: delay_x, 3: 180, 84: 60, 85: 5, 88: 0.4})

    # Collapsing Submarine Gate (Group 2)
    for y in range(60, 300, 30):
        add_obj({1: 1, 2: 4200, 3: y, 21: 3, 57: 2})
    # Move Gate Down into Lair
    add_obj({1: 901, 2: 3960, 3: 180, 51: 2, 85: 0, 86: -240, 88: 1.5, 87: 6}) # Bounce Out

    # BG Shift to Deep Royal Purple Lair
    add_obj({1: 221, 2: 4000, 3: 180, 23: 1000, 7: 15, 8: 0, 9: 30, 10: 1.0})

    # --- SECTION 3: THE PURPLE OCTOPUS BOSS FIGHT! (X = 4300 to 7300) ---
    # Arena Boundaries (Floor & Ceiling for Ship Fight)
    for x in range(4300, 7300, 30):
        # Arena Floor
        add_obj({1: 1, 2: x, 3: 15, 21: 5, 24: 1})
        add_obj({1: 2, 2: x, 3: 30, 21: 6, 24: 3}) # Magenta glow border
        # Arena Ceiling
        add_obj({1: 1, 2: x, 3: 345, 21: 5, 24: 1})
        add_obj({1: 2, 2: x, 3: 330, 21: 6, 24: 3, 5: 1})

    # --- BOSS ARTWORK CONSTRUCTION ---
    boss_x = 5200
    boss_y = 180

    # 1. Octopus Main Body Dome (Group 10)
    for dx in range(-60, 90, 30):
        for dy in range(-60, 90, 30):
            if dx*dx + dy*dy <= 8100: # Round body shape
                add_obj({1: 1, 2: boss_x + dx, 3: boss_y + dy, 21: 5, 24: 5, 57: 10})
                # Glow ring detail
                if dx*dx + dy*dy >= 4900:
                    add_obj({1: 503, 2: boss_x + dx, 3: boss_y + dy, 21: 6, 24: 6, 32: 0.8, 57: 10})

    # 2. Glowing Menacing Eyes (Group 15 & 10)
    # Left Eye
    add_obj({1: 503, 2: boss_x - 30, 3: boss_y + 20, 21: 7, 24: 8, 32: 1.8, 57: "10.15"})
    add_obj({1: 1, 2: boss_x - 30, 3: boss_y + 20, 21: 8, 24: 9, 32: 0.4, 57: "10.15"}) # Pupil
    # Right Eye
    add_obj({1: 503, 2: boss_x + 30, 3: boss_y + 20, 21: 7, 24: 8, 32: 1.8, 57: "10.15"})
    add_obj({1: 1, 2: boss_x + 30, 3: boss_y + 20, 21: 8, 24: 9, 32: 0.4, 57: "10.15"}) # Pupil

    # 3. Tentacle 1 - Top Left (Group 11)
    t1_coords = [(-90, 60), (-120, 90), (-150, 110), (-180, 120), (-210, 110), (-240, 90)]
    for tx, ty in t1_coords:
        add_obj({1: 1, 2: boss_x + tx, 3: boss_y + ty, 21: 5, 24: 5, 57: 11})
        add_obj({1: 503, 2: boss_x + tx, 3: boss_y + ty - 15, 21: 6, 24: 6, 32: 0.7, 57: 11}) # Suction cup glow
        add_obj({1: 4, 2: boss_x + tx, 3: boss_y + ty - 25, 21: 6, 24: 7, 5: 1, 57: 11}) # Sharp tip/spike hazard

    # 4. Tentacle 2 - Bottom Left (Group 12)
    t2_coords = [(-90, -60), (-130, -80), (-170, -90), (-210, -80), (-250, -60)]
    for tx, ty in t2_coords:
        add_obj({1: 1, 2: boss_x + tx, 3: boss_y + ty, 21: 5, 24: 5, 57: 12})
        add_obj({1: 503, 2: boss_x + tx, 3: boss_y + ty + 15, 21: 6, 24: 6, 32: 0.7, 57: 12})
        add_obj({1: 4, 2: boss_x + tx, 3: boss_y + ty + 25, 21: 6, 24: 7, 57: 12})

    # 5. Tentacle 3 - Top Right (Group 13)
    t3_coords = [(90, 60), (120, 90), (150, 110), (180, 120)]
    for tx, ty in t3_coords:
        add_obj({1: 1, 2: boss_x + tx, 3: boss_y + ty, 21: 5, 24: 5, 57: 13})
        add_obj({1: 503, 2: boss_x + tx, 3: boss_y + ty - 15, 21: 6, 24: 6, 32: 0.7, 57: 13})

    # 6. Tentacle 4 - Bottom Right (Group 14)
    t4_coords = [(90, -60), (130, -80), (170, -90), (210, -80)]
    for tx, ty in t4_coords:
        add_obj({1: 1, 2: boss_x + tx, 3: boss_y + ty, 21: 5, 24: 5, 57: 14})
        add_obj({1: 503, 2: boss_x + tx, 3: boss_y + ty + 15, 21: 6, 24: 6, 32: 0.7, 57: 14})

    # 7. Ink Cannon Projectile (Group 16)
    add_obj({1: 503, 2: boss_x - 60, 3: boss_y - 20, 21: 8, 24: 10, 32: 2.5, 57: 16})
    add_obj({1: 4, 2: boss_x - 60, 3: boss_y - 20, 21: 8, 24: 11, 4: 1, 57: 16})

    # --- BOSS FIGHT ATTACK TRIGGERS & ANIMATIONS ---

    # --- PHASE 1: TENTACLE SLAM (X = 4500) ---
    add_obj({1: 901, 2: 4500, 3: 180, 51: 11, 85: 0, 86: -120, 88: 0.4, 87: 8}) # Bounce Out
    add_obj({1: 1520, 2: 4515, 3: 180, 84: 75, 85: 5, 88: 0.5})
    add_obj({1: 901, 2: 4700, 3: 180, 51: 11, 85: 0, 86: 120, 88: 0.8, 87: 1}) # Ease In Out

    # --- PHASE 2: INK BLAST CANNON (X = 4900) ---
    add_obj({1: 1006, 2: 4850, 3: 180, 97: 1, 98: 15, 7: 255, 8: 0, 9: 0, 99: 0.1, 100: 0.3, 101: 0.2})
    add_obj({1: 901, 2: 4900, 3: 180, 51: 16, 85: -900, 86: 0, 88: 1.0, 87: 0})

    # --- PHASE 3: BOTTOM TENTACLE SWEEP & ROTATION (X = 5300) ---
    add_obj({1: 901, 2: 5300, 3: 180, 51: 12, 85: 0, 86: 100, 88: 0.5, 87: 6})
    add_obj({1: 1268, 2: 5310, 3: 180, 51: 12, 71: 10, 68: -35, 88: 0.6, 87: 1})
    add_obj({1: 901, 2: 5550, 3: 180, 51: 12, 85: 0, 86: -100, 88: 0.6, 87: 1})

    # --- PHASE 4: DUAL TENTACLE CRUSH & ENRAGE (X = 5800 to 6700) ---
    add_obj({1: 1520, 2: 5800, 3: 180, 84: 90, 85: 5, 88: 2.0})
    add_obj({1: 1006, 2: 5810, 3: 180, 97: 1, 98: 15, 7: 255, 8: 220, 9: 0, 99: 0.1, 100: 0.5, 101: 0.2})

    add_obj({1: 901, 2: 6000, 3: 180, 51: 11, 85: -100, 86: -100, 88: 0.5, 87: 8})
    add_obj({1: 901, 2: 6000, 3: 180, 51: 12, 85: -100, 86: 100, 88: 0.5, 87: 8})

    add_obj({1: 901, 2: 6500, 3: 180, 51: 11, 85: 100, 86: 100, 88: 0.8, 87: 1})
    add_obj({1: 901, 2: 6500, 3: 180, 51: 12, 85: 100, 86: -100, 88: 0.8, 87: 1})

    # --- BOSS DEFEAT & DISSOLVE (X = 6900) ---
    for grp in [10, 11, 12, 13, 14, 15, 16]:
        add_obj({1: 1007, 2: 6900, 3: 180, 51: grp, 35: 0.0, 10: 1.2})

    add_obj({1: 1006, 2: 6905, 3: 180, 97: 0, 98: 1000, 7: 255, 8: 255, 9: 255, 99: 0.1, 100: 0.3, 101: 1.0})
    add_obj({1: 1520, 2: 6910, 3: 180, 84: 95, 85: 5, 88: 1.5})

    # --- OUTRO & LEVEL ENDING (X = 7000 to 7500) ---
    for x in range(7100, 7400, 60):
        add_obj({1: 503, 2: x, 3: 180, 21: 4, 24: 5, 32: 2.0})
        add_obj({1: 503, 2: x + 30, 3: 220, 21: 6, 24: 5, 32: 1.5})

    add_obj({1: 13, 2: 7400, 3: 180})

    # Construct complete GD 2.2 Level String
    header = "kS38,1_0_1_0_1_0_1_0_1_0_1_0_1_0_1_0_1_0_1_0_1_0,kA13,0,kA15,0,kA16,0,kA17,0,kA18,0,kS39,0,kA2,0,kA3,0,kA4,0,kA6,0,kA7,0,kA8,0,kA9,0,kA10,0,kA11,0;"
    level_string = header + ";".join(objects) + ";"

    return level_string, len(objects)

def export_gd_level(level_name, description, creator, level_string, obj_count):
    # 1. Inner Level String Encoding (Gzip -> URL-safe Base64)
    compressed_level = gzip.compress(level_string.encode('utf-8'))
    b64_level_urlsafe = base64.urlsafe_b64encode(compressed_level).decode('utf-8')

    # 2. Description Encoding (Standard Base64)
    b64_description = base64.b64encode(description.encode('utf-8')).decode('utf-8')

    # 3. Build XML Plist Representation using Working Reference Schema:
    # Root element: <plist version="1.0" gjver="2.0">
    # kCEK = 4
    # k2 = Level Name (string)
    # k3 = Base64-encoded description string
    # k4 = Inner Level String (URL-safe Base64 gzipped level object string)
    # k5 = Creator Name (string)
    # k16 = Level Revision (integer: 1)
    # k21 = Level Type (integer: 2 = Local Editor Level)
    # k48 = Object Count (integer)
    # k50 = Binary Version (integer: 45)
    # k80 = Editor Level Version (integer: 22 = GD 2.2)
    # k101 = Editor Settings (integer: 0)
    # kI1 = Camera Zoom Setting (integer: 0)
    # kI2 = Camera Offset Setting (integer: 0)
    # kI3 = Camera Opacity Setting (integer: 1)
    plist_xml = f"""<?xml version="1.0"?>
<plist version="1.0" gjver="2.0">
<dict>
	<k>kCEK</k><i>4</i>
	<k>k2</k><s>{level_name}</s>
	<k>k3</k><s>{b64_description}</s>
	<k>k4</k><s>{b64_level_urlsafe}</s>
	<k>k5</k><s>{creator}</s>
	<k>k16</k><i>1</i>
	<k>k21</k><i>2</i>
	<k>k48</k><i>{obj_count}</i>
	<k>k50</k><i>45</i>
	<k>k80</k><i>22</i>
	<k>k101</k><i>0</i>
	<k>kI1</k><i>0</i>
	<k>kI2</k><i>0</i>
	<k>kI3</k><i>1</i>
</dict>
</plist>"""

    # 4. Outer .gdlvl Export Pipeline (XML UTF-8 bytes -> Gzip -> URL-safe Base64)
    compressed_plist = gzip.compress(plist_xml.encode('utf-8'))
    b64_outer_gdlvl = base64.urlsafe_b64encode(compressed_plist).decode('utf-8')

    return plist_xml, b64_outer_gdlvl

def main():
    print("Generating Insane Realism GD 2.2 Level with Purple Octopus Boss Fight...")
    level_str, obj_count = build_gd_level()
    print(f"Generated raw level string with length: {len(level_str)} characters across {obj_count} objects.")

    level_name = "Abyssal Kraken"
    description = "Insane realistic underwater level with dynamic transitions and a purple octopus boss fight!"
    creator = "Jules"

    plist_xml, b64_outer_gdlvl = export_gd_level(level_name, description, creator, level_str, obj_count)

    # Output 1: Abyssal_Kraken.gdlvl (Outer Gzip + URL-safe Base64 encoded XML Plist string)
    with open("Abyssal_Kraken.gdlvl", "w", encoding="utf-8") as f:
        f.write(b64_outer_gdlvl)
    print("Successfully saved Abyssal_Kraken.gdlvl (Outer Gzip + URL-safe Base64 .gdlvl export)!")

    # Output 2: Abyssal_Kraken.gmd (Raw XML Plist format)
    with open("Abyssal_Kraken.gmd", "w", encoding="utf-8") as f:
        f.write(plist_xml)
    print("Successfully saved Abyssal_Kraken.gmd (Raw XML Plist format)!")

    # Output 3: level_string.txt (Raw level object string)
    with open("level_string.txt", "w", encoding="utf-8") as f:
        f.write(level_str)
    print("Successfully saved level_string.txt!")

if __name__ == "__main__":
    main()
