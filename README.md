# Abyssal Kraken - Geometry Dash 2.209 Insane Level

**Abyssal Kraken** is an insane-difficulty Geometry Dash level featuring:
- **Insane Realism & Visuals**: Detailed bioluminescent ocean trench environment, layered slate/basalt structures, glowing coral reefs, and custom color channels.
- **Dynamic Transitions**: Camera shakes, flash pulses, high-speed portals (1x to 3x speed), and screen wipe block shutters.
- **Purple Octopus Boss Fight**: A multi-phase interactive boss fight against a massive animated Purple Octopus built from over 150 detailed geometric shapes and glow objects, featuring tentacle slams, sweeps, ink blast projectiles, enrage flashes, and a defeat dissolve sequence.

---

## 📁 Included Level Files & Formats

This repository contains multiple level formats to ensure 100% compatibility across all Geometry Dash 2.2 / 2.209 setups:

1. **`Abyssal_Kraken.gdlvl`**
   - **Format**: Native Geometry Dash 2.209 Export format (Base64 URL-safe gzipped XML Plist string).
   - **Usage**: Standard native file format exported and imported by vanilla Geometry Dash 2.209.

2. **`Abyssal_Kraken_xml.gdlvl`**
   - **Format**: Raw XML Plist format with `.gdlvl` extension.
   - **Usage**: Alternative native import format for Geometry Dash 2.209 setups expecting raw XML Plist strings.

3. **`Abyssal_Kraken.gmd`**
   - **Format**: Standard GDShare / Geode mod level export format (XML Plist).
   - **Usage**: Import via GDShare or Geode level management tools.

4. **`level_string.txt`**
   - **Format**: Uncompressed raw level string starting with header `kS38,...` followed by object key-value pairs.
   - **Usage**: Direct insertion into GD save files (`CCLocalLevels.dat`) or level string tools.

---

## 🚀 How to Import into Geometry Dash 2.209

### Method 1: Native Geometry Dash 2.209 Import
1. Open **Geometry Dash 2.209**.
2. Go to **Create** -> **My Levels**.
3. Click the **Import** button in the level editor/list menu.
4. Select `Abyssal_Kraken.gdlvl` (or `Abyssal_Kraken_xml.gdlvl`).
5. The level **Abyssal Kraken** will appear in your level list, ready to play or edit!

### Method 2: GDShare / Geode Mod
1. Install **Geode** and the **GDShare** mod.
2. In Geometry Dash, go to **My Levels**.
3. Click **Import Level** and select `Abyssal_Kraken.gmd`.

### Method 3: Raw Level String
- Open `level_string.txt` and copy the contents to paste into any custom level tool or GD save file manager.

---

## 🛠️ Building & Validating the Level

### 1. Generate / Rebuild Level Files
To rebuild or modify the level structure and generate all `.gdlvl`, `.gmd`, and level string files:
```bash
python3 generate_level.py
```

### 2. Run Test Suite
To verify the XML structure, URL-safe Base64 decompression, GD 2.2 tags (`k80=22`, `k45=1260`), triggers, boss fight group references, and game mode portals:
```bash
python3 test_level.py
```
