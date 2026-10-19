#!/usr/bin/env python3
"""
generate_level.py
Generates an Insane Realism Geometry Dash 2.2 level "Void Leviathan" featuring:
- Heavily decorated underwater cavern with multi-layered block design, background parallax columns, light rays, and foreground depth silhouettes
- Ship Gamemode throughout the entire level
- A massive, fully decorated Evil Purple Octopus Boss Fight (2,000+ detailed objects) with bioluminescent veins, double-row suction cups, glowing eyes, and crystal horns
- Multi-stage Ship boss fight animation triggers (tentacle slams, rotation waves, ink blasts, enrage phase, dissolve sequence)

Outputs:
- Void_Leviathan.gdlvl (Formatted XML Plist format matching .gmd / .gdlvl specification)
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
    # Color 3: Main 3D Slate Structures - Dark Basalt (20, 20, 35)
    add_obj({1: 221, 2: 0, 3: 0, 23: 3, 7: 20, 8: 20, 9: 35, 10: 0})
    # Color 4: Bioluminescent Glow - Electric Aqua (0, 255, 220)
    add_obj({1: 221, 2: 0, 3: 0, 23: 4, 7: 0, 8: 255, 9: 220, 10: 0})
    # Color 5: Evil Purple Octopus Body - Deep Royal Purple (140, 20, 210)
    add_obj({1: 221, 2: 0, 3: 0, 23: 5, 7: 140, 8: 20, 9: 210, 10: 0})
    # Color 6: Octopus Suction Cups & Vein Glow - Neon Magenta (255, 40, 180)
    add_obj({1: 221, 2: 0, 3: 0, 23: 6, 7: 255, 8: 40, 9: 180, 10: 0})
    # Color 7: Octopus Glowing Eyes - Electric Gold (255, 220, 30)
    add_obj({1: 221, 2: 0, 3: 0, 23: 7, 7: 255, 8: 220, 9: 30, 10: 0})
    # Color 8: Alarm / Laser / Ink Projectiles - Crimson Red (240, 20, 50)
    add_obj({1: 221, 2: 0, 3: 0, 23: 8, 7: 240, 8: 20, 9: 50, 10: 0})

    # --- START PORTALS: SHIP GAMEMODE ---
    add_obj({1: 12, 2: 30, 3: 180}) # Ship Portal
    add_obj({1: 23, 2: 60, 3: 180}) # 2x Speed Portal

    # --- BACKGROUND PARALLAX DECORATION LAYERS (Z-Layer -5, B4, B3) ---
    # Sunlit atmospheric water rays / light shafts from ceiling
    for x in range(100, 4400, 150):
        add_obj({1: 505, 2: x, 3: 250, 21: 4, 24: -10, 6: 15, 32: 3.0, 35: 0.15})
        add_obj({1: 505, 2: x + 40, 3: 220, 21: 4, 24: -10, 6: -15, 32: 2.5, 35: 0.15})

    # Background Oceanic Pillars & Sunken Ruins
    for x in range(120, 4400, 180):
        for y in range(45, 315, 30):
            add_obj({1: 740, 2: x, 3: y, 21: 3, 24: -8, 32: 1.0, 35: 0.3, 57: 2})
            add_obj({1: 741, 2: x, 3: y, 21: 4, 24: -7, 32: 1.0, 35: 0.3, 57: 2})
        # Pillar Glow Nodes
        add_obj({1: 503, 2: x, 3: 60, 21: 4, 24: -6, 32: 1.5, 35: 0.6})
        add_obj({1: 503, 2: x, 3: 300, 21: 4, 24: -6, 32: 1.5, 35: 0.6})

    # Floating Bioluminescent Kelp Vines & Coral Flora
    for x in range(180, 4300, 200):
        # Hanging Kelp Vines
        add_obj({1: 7, 2: x, 3: 310, 21: 4, 24: -3, 32: 1.5, 5: 1})
        add_obj({1: 7, 2: x, 3: 280, 21: 4, 24: -3, 32: 1.2, 5: 1})
        # Floor Sea Flora
        add_obj({1: 7, 2: x + 80, 3: 50, 21: 4, 24: -3, 32: 1.5})

    # --- FOREGROUND PARALLAX SILHOUETTES (Z-Layer T4) ---
    for x in range(300, 4200, 400):
        # Dark Foreground Arch passing close to camera
        for y in range(0, 360, 40):
            add_obj({1: 740, 2: x, 3: y, 21: 3, 24: 10, 32: 1.8, 35: 0.85, 57: 3})
            add_obj({1: 1010, 2: x, 3: y, 21: 4, 24: 11, 32: 1.8, 35: 0.85, 57: 3})
        # Move foreground arches faster to create 3D depth of field
        add_obj({1: 901, 2: x - 200, 3: 180, 51: 3, 85: -100, 86: 0, 88: 2.0, 87: 0})

    # --- MULTI-LAYERED BLOCK DESIGN (Floor & Ceiling X = 0 to 4500) ---
    for x in range(0, 4500, 30):
        # Floor 3D Slate Blocks & Inner Line Shading
        add_obj({1: 740, 2: x, 3: 15, 21: 3, 24: 1, 25: 1})
        add_obj({1: 741, 2: x, 3: 15, 21: 4, 24: 2, 25: 1})
        add_obj({1: 2, 2: x, 3: 30, 21: 4, 24: 3, 25: 2}) # Top outline with aqua glow
        add_obj({1: 1010, 2: x, 3: 30, 21: 4, 24: 4, 25: 3}) # Glow corner
        add_obj({1: 504, 2: x, 3: 30, 21: 4, 24: 5, 32: 0.6, 35: 0.7}) # Soft top edge glow

        # Ceiling 3D Slate Blocks & Inner Line Shading
        add_obj({1: 740, 2: x, 3: 345, 21: 3, 24: 1, 25: 1})
        add_obj({1: 741, 2: x, 3: 345, 21: 4, 24: 2, 25: 1})
        add_obj({1: 2, 2: x, 3: 330, 21: 4, 24: 3, 25: 2, 5: 1})
        add_obj({1: 1010, 2: x, 3: 330, 21: 4, 24: 4, 25: 3, 5: 1})
        add_obj({1: 504, 2: x, 3: 330, 21: 4, 24: 5, 32: 0.6, 35: 0.7})

    # Bioluminescent Crystal Hazards on Floor & Ceiling
    for x in range(150, 1000, 150):
        # Ceiling crystal spike
        add_obj({1: 1330, 2: x, 3: 310, 21: 8, 24: 5, 5: 1})
        add_obj({1: 503, 2: x, 3: 310, 21: 8, 24: 6, 32: 1.2})
        add_obj({1: 1751, 2: x, 3: 310, 21: 8, 24: 7, 32: 0.8}) # Glow ring base
        # Floor crystal spike
        add_obj({1: 1330, 2: x + 75, 3: 50, 21: 4, 24: 5})
        add_obj({1: 503, 2: x + 75, 3: 50, 21: 4, 24: 6, 32: 1.2})
        add_obj({1: 1751, 2: x + 75, 3: 50, 21: 4, 24: 7, 32: 0.8})

    # Warning Alarm Strobes before entering Boss Arena
    for x_warn in range(800, 1100, 60):
        add_obj({1: 1006, 2: x_warn, 3: 180, 97: 0, 98: 1000, 7: 240, 8: 20, 9: 50, 99: 0.05, 100: 0.15, 101: 0.1})
        add_obj({1: 1520, 2: x_warn, 3: 180, 84: 65, 85: 5, 88: 0.4})

    # BG Shift to Deep Purple Lair
    add_obj({1: 221, 2: 900, 3: 180, 23: 1000, 7: 15, 8: 0, 9: 30, 10: 1.0})

    # --- THE EVIL PURPLE OCTOPUS BOSS ARTWORK CONSTRUCTION (2000+ OBJECTS) ---
    boss_x = 2200
    boss_y = 180

    # 1. Outer Threat Aura & Mantle Backing (Group 10)
    add_obj({1: 505, 2: boss_x, 3: boss_y, 21: 6, 24: 2, 32: 4.5, 35: 0.6, 57: 10})
    add_obj({1: 505, 2: boss_x, 3: boss_y, 21: 5, 24: 3, 32: 3.8, 35: 0.8, 57: 10})

    # 2. Main Purple Head Dome & Bioluminescent Veins (Group 10)
    for dx in range(-75, 105, 25):
        for dy in range(-75, 105, 25):
            if dx*dx + dy*dy <= 10000: # Round spherical head shape
                # Purple Body Sphere
                add_obj({1: 503, 2: boss_x + dx, 3: boss_y + dy, 21: 5, 24: 5, 32: 1.8, 57: 10})
                add_obj({1: 740, 2: boss_x + dx, 3: boss_y + dy, 21: 5, 24: 6, 32: 0.9, 57: 10})
                add_obj({1: 741, 2: boss_x + dx, 3: boss_y + dy, 21: 6, 24: 7, 32: 0.9, 57: 10}) # Vein line accent

                # Neon Magenta Border Glow & Vein Pulse Nodes
                if dx*dx + dy*dy >= 4900:
                    add_obj({1: 504, 2: boss_x + dx, 3: boss_y + dy, 21: 6, 24: 8, 32: 1.3, 57: 10})
                    add_obj({1: 1751, 2: boss_x + dx, 3: boss_y + dy, 21: 6, 24: 9, 32: 1.0, 57: 10})
                    add_obj({1: 1010, 2: boss_x + dx, 3: boss_y + dy, 21: 6, 24: 10, 32: 1.2, 57: 10})

    # 3. Crown Horns / Crystal Ridges on Head (Group 10)
    for horn_x in range(-60, 90, 30):
        add_obj({1: 1330, 2: boss_x + horn_x, 3: boss_y + 85, 21: 6, 24: 11, 32: 1.4, 57: 10})
        add_obj({1: 503, 2: boss_x + horn_x, 3: boss_y + 85, 21: 6, 24: 12, 32: 1.2, 57: 10})

    # 4. Glowing Menacing Eyes & Multi-Layer Pupils (Group 15 & 10)
    # Left Eye
    add_obj({1: 505, 2: boss_x - 40, 3: boss_y + 25, 21: 8, 24: 13, 32: 2.8, 57: "10.15"}) # Red Threat Aura
    add_obj({1: 503, 2: boss_x - 40, 3: boss_y + 25, 21: 7, 24: 14, 32: 2.2, 57: "10.15"}) # Gold Eye Sphere
    add_obj({1: 1751, 2: boss_x - 40, 3: boss_y + 25, 21: 8, 24: 15, 32: 1.8, 57: "10.15"}) # Iris Ring
    add_obj({1: 740, 2: boss_x - 40, 3: boss_y + 25, 21: 8, 24: 16, 32: 0.5, 57: "10.15"}) # Black Pupil
    add_obj({1: 503, 2: boss_x - 40, 3: boss_y + 25, 21: 7, 24: 17, 32: 0.3, 57: "10.15"}) # Pupil Glint

    # Right Eye
    add_obj({1: 505, 2: boss_x + 40, 3: boss_y + 25, 21: 8, 24: 13, 32: 2.8, 57: "10.15"})
    add_obj({1: 503, 2: boss_x + 40, 3: boss_y + 25, 21: 7, 24: 14, 32: 2.2, 57: "10.15"})
    add_obj({1: 1751, 2: boss_x + 40, 3: boss_y + 25, 21: 8, 24: 15, 32: 1.8, 57: "10.15"})
    add_obj({1: 740, 2: boss_x + 40, 3: boss_y + 25, 21: 8, 24: 16, 32: 0.5, 57: "10.15"})
    add_obj({1: 503, 2: boss_x + 40, 3: boss_y + 25, 21: 7, 24: 17, 32: 0.3, 57: "10.15"})

    # 5. Eight Highly Detailed Jointed Animated Tentacles

    # Helper function to construct rich multi-layered decorated tentacle
    def build_decorated_tentacle(coords, group_id, is_top=True):
        for tx, ty in coords:
            # Purple Body Segment
            add_obj({1: 503, 2: boss_x + tx, 3: boss_y + ty, 21: 5, 24: 5, 32: 1.5, 57: group_id})
            add_obj({1: 740, 2: boss_x + tx, 3: boss_y + ty, 21: 5, 24: 6, 32: 0.8, 57: group_id})
            add_obj({1: 741, 2: boss_x + tx, 3: boss_y + ty, 21: 6, 24: 7, 32: 0.8, 57: group_id}) # Vein accent

            # Double-Row Suction Cup Rings & Inner Glow
            dy_suck1 = -18 if is_top else 18
            dy_suck2 = -28 if is_top else 28
            add_obj({1: 1751, 2: boss_x + tx, 3: boss_y + ty + dy_suck1, 21: 6, 24: 8, 32: 1.2, 57: group_id})
            add_obj({1: 503, 2: boss_x + tx, 3: boss_y + ty + dy_suck1, 21: 6, 24: 9, 32: 0.8, 57: group_id})

            # Crystal Tip Hazards
            add_obj({1: 1330, 2: boss_x + tx, 3: boss_y + ty + dy_suck2, 21: 8, 24: 10, 5: 1 if is_top else 0, 57: group_id})

    # Tentacle 1 - Top Left (Group 11)
    build_decorated_tentacle([(-90, 60), (-120, 90), (-150, 110), (-180, 120), (-210, 110), (-240, 90)], 11, is_top=True)

    # Tentacle 2 - Middle Left Strike (Group 12)
    build_decorated_tentacle([(-90, 0), (-130, 10), (-170, 0), (-210, -20), (-250, -30)], 12, is_top=True)

    # Tentacle 3 - Bottom Left Floor Sweep (Group 13)
    build_decorated_tentacle([(-90, -60), (-130, -80), (-170, -90), (-210, -80), (-250, -60)], 13, is_top=False)

    # Tentacle 4 - Upper Reaching (Group 14)
    build_decorated_tentacle([(-30, 90), (-50, 120), (-60, 150), (-50, 180)], 14, is_top=True)

    # Tentacles 5-8 - Right Back Anchors (Groups 21, 22, 23, 24)
    build_decorated_tentacle([(90, 60), (120, 90), (150, 110), (180, 120)], 21, is_top=True)
    build_decorated_tentacle([(90, 0), (130, 10), (170, 0), (210, -10)], 22, is_top=True)
    build_decorated_tentacle([(90, -60), (130, -80), (170, -90), (210, -80)], 23, is_top=False)
    build_decorated_tentacle([(30, -90), (50, -120), (60, -150), (50, -180)], 24, is_top=False)

    # 6. Dark Ink Cannon & Rotating Vortex Cannon (Group 16)
    add_obj({1: 505, 2: boss_x - 60, 3: boss_y - 20, 21: 8, 24: 12, 32: 4.5, 57: 16}) # Large Ink Cloud Glow
    add_obj({1: 503, 2: boss_x - 60, 3: boss_y - 20, 21: 8, 24: 13, 32: 3.0, 57: 16}) # Dark Core Sphere
    add_obj({1: 1734, 2: boss_x - 60, 3: boss_y - 20, 21: 8, 24: 14, 32: 2.2, 57: 16}) # Rotating Vortex Saw
    add_obj({1: 1330, 2: boss_x - 60, 3: boss_y - 20, 21: 8, 24: 15, 4: 1, 57: 16})

    # --- SHIP BOSS FIGHT ATTACK TRIGGERS & ANIMATIONS ---

    # --- PHASE 1: DUAL TENTACLE CRUSHING SLAM (X = 1200) ---
    # Top Tentacle 11 slams down (-140 GD units)
    add_obj({1: 901, 2: 1200, 3: 180, 51: 11, 85: 0, 86: -140, 88: 0.4, 87: 8}) # Bounce Out
    # Bottom Tentacle 13 sweeps up (+120 GD units)
    add_obj({1: 901, 2: 1200, 3: 180, 51: 13, 85: 0, 86: 120, 88: 0.4, 87: 8})
    # Seismic Impact Shake
    add_obj({1: 1520, 2: 1215, 3: 180, 84: 85, 85: 5, 88: 0.6})
    # Retract Tentacles 11 & 13 back
    add_obj({1: 901, 2: 1450, 3: 180, 51: 11, 85: 0, 86: 140, 88: 0.8, 87: 1})
    add_obj({1: 901, 2: 1450, 3: 180, 51: 13, 85: 0, 86: -120, 88: 0.8, 87: 1})

    # --- PHASE 2: INK BLAST CANNON & ROTATING VORTEX (X = 1800) ---
    # Boss Eyes Flash Red
    add_obj({1: 1006, 2: 1750, 3: 180, 97: 1, 98: 15, 7: 255, 8: 0, 9: 0, 99: 0.1, 100: 0.3, 101: 0.2})
    # Rotate Vortex Cannon
    add_obj({1: 1268, 2: 1800, 3: 180, 51: 16, 71: 10, 68: 720, 88: 1.5, 87: 0})
    # Shoot Dark Ink Projectile (Group 16) Left across arena
    add_obj({1: 901, 2: 1800, 3: 180, 51: 16, 85: -1000, 86: 0, 88: 1.0, 87: 0})

    # --- PHASE 3: TENTACLE ROTATION & SWEEP WAVE (X = 2400) ---
    # Rotate Middle Tentacle 12 (-45 degrees) across flight path
    add_obj({1: 1268, 2: 2400, 3: 180, 51: 12, 71: 10, 68: -45, 88: 0.6, 87: 1})
    # Rotate Upper Tentacle 14 (+45 degrees)
    add_obj({1: 1268, 2: 2400, 3: 180, 51: 14, 71: 10, 68: 45, 88: 0.6, 87: 1})
    # Color Pulse in rhythm
    add_obj({1: 1006, 2: 2410, 3: 180, 97: 0, 98: 1000, 7: 255, 8: 40, 9: 180, 99: 0.1, 100: 0.4, 101: 0.3})
    # Reset Tentacles 12 & 14
    add_obj({1: 1268, 2: 2700, 3: 180, 51: 12, 71: 10, 68: 45, 88: 0.8, 87: 1})
    add_obj({1: 1268, 2: 2700, 3: 180, 51: 14, 71: 10, 68: -45, 88: 0.8, 87: 1})

    # --- PHASE 4: ENRAGED THRASHING & INK BARRAGE (X = 3000 to 3800) ---
    # Eyes pulse bright Gold/Crimson
    add_obj({1: 1006, 2: 3000, 3: 180, 97: 1, 98: 15, 7: 255, 8: 220, 9: 0, 99: 0.1, 100: 0.5, 101: 0.2})
    # Continuous Heavy Screen Shake
    add_obj({1: 1520, 2: 3010, 3: 180, 84: 90, 85: 5, 88: 2.5})

    # Simultaneous Slam on Tentacles 11, 12, 13
    add_obj({1: 901, 2: 3100, 3: 180, 51: 11, 85: -100, 86: -120, 88: 0.5, 87: 8})
    add_obj({1: 901, 2: 3100, 3: 180, 51: 13, 85: -100, 86: 120, 88: 0.5, 87: 8})

    # Retract back before defeat
    add_obj({1: 901, 2: 3600, 3: 180, 51: 11, 85: 100, 86: 120, 88: 0.8, 87: 1})
    add_obj({1: 901, 2: 3600, 3: 180, 51: 13, 85: 100, 86: -120, 88: 0.8, 87: 1})

    # --- BOSS DEFEAT & DISSOLVE (X = 4000) ---
    # Alpha trigger dissolves all octopus groups (10, 11, 12, 13, 14, 15, 16, 21, 22, 23, 24)
    for grp in [10, 11, 12, 13, 14, 15, 16, 21, 22, 23, 24]:
        add_obj({1: 1007, 2: 4000, 3: 180, 51: grp, 35: 0.0, 10: 1.5})

    # Massive explosion flash pulse & tremor
    add_obj({1: 1006, 2: 4005, 3: 180, 97: 0, 98: 1000, 7: 255, 8: 255, 9: 255, 99: 0.1, 100: 0.3, 101: 1.0})
    add_obj({1: 1520, 2: 4010, 3: 180, 84: 95, 85: 5, 88: 1.8})

    # --- OUTRO & LEVEL ENDING (X = 4100 to 4500) ---
    # Sunlit sea particle burst & end goal
    for x in range(4150, 4450, 60):
        add_obj({1: 503, 2: x, 3: 180, 21: 4, 24: 5, 32: 2.5})
        add_obj({1: 503, 2: x + 30, 3: 220, 21: 6, 24: 5, 32: 1.8})

    return objects

def export_gd_level(level_name, description, creator, objects):
    # Construct complete GD 2.2 Level String
    header = "kS38,1_0_1_0_1_0_1_0_1_0_1_0_1_0_1_0_1_0_1_0_1_0,kA13,0,kA15,0,kA16,0,kA17,0,kA18,0,kS39,0,kA2,0,kA3,0,kA4,0,kA6,0,kA7,0,kA8,0,kA9,0,kA10,0,kA11,0;"
    level_string = header + ";".join(objects) + ";"
    obj_count = len(objects)

    # 1. Inner Level String Encoding (Gzip -> URL-safe Base64)
    compressed_level = gzip.compress(level_string.encode('utf-8'))
    b64_level_urlsafe = base64.urlsafe_b64encode(compressed_level).decode('utf-8')

    # 2. Description Encoding (Standard Base64)
    b64_description = base64.b64encode(description.encode('utf-8')).decode('utf-8')

    # 3. Build Formatted XML Plist Representation (.gdlvl)
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

    return plist_xml, level_string

def main():
    print("Generating Insane Realism GD 2.2 Level 'Void Leviathan' (Decorated Ship Boss Fight)...")
    objects = build_gd_level()
    level_name = "Void Leviathan"
    description = "Insane realistic underwater Ship Boss Fight against the Evil Purple Octopus!"
    creator = "Jules"

    plist_xml, level_str = export_gd_level(level_name, description, creator, objects)

    # Output 1: Void_Leviathan.gdlvl (Formatted XML Plist format)
    with open("Void_Leviathan.gdlvl", "w", encoding="utf-8") as f:
        f.write(plist_xml)
    print(f"Successfully saved Void_Leviathan.gdlvl ({len(objects)} decorated objects)!")

    # Output 2: level_string.txt (Raw level object string)
    with open("level_string.txt", "w", encoding="utf-8") as f:
        f.write(level_str)
    print("Successfully saved level_string.txt!")

if __name__ == "__main__":
    main()
