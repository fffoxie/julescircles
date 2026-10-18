# Void Leviathan - Geometry Dash 2.2 Insane Level

**Void Leviathan** is an insane-difficulty Geometry Dash level featuring:
- **Insane Realism & Visuals**: Detailed bioluminescent ocean trench environment, layered slate/basalt structures, glowing coral reefs, and custom color channels.
- **Dynamic Transitions**: Camera shakes, flash pulses, high-speed portals (1x to 3x speed), and screen wipe block shutters.
- **Purple Octopus Boss Fight**: A multi-phase interactive boss fight against a massive animated Purple Octopus built from over 150 detailed geometric shapes and glow objects, featuring tentacle slams, sweeps, ink blast projectiles, enrage flashes, and a defeat dissolve sequence.

---

## 📁 Included Level Files & Formats

1. **`Void_Leviathan.gdlvl`**
   - **Format**: Geometry Dash 2.2 Level Export format (Formatted XML Plist matching the `.gmd` / `.gdlvl` specification).
   - **Structure**: Root `<plist version="1.0" gjver="2.0">`, `kCEK=4`, `k2` Level Name string, Base64 `k3` description string, Base64-gzipped `k4` inner level object string, `k5` Creator string, `k16=1`, `k21=2`, `k48=1260`, `k50=45`, `k80=22`, `k101=0`, `kI1=0`, `kI2=0`, `kI3=1`.

2. **`level_string.txt`**
   - **Format**: Uncompressed raw level string starting with header `kS38,...` followed by object key-value pairs.
   - **Usage**: Direct insertion into GD save files (`CCLocalLevels.dat`) or level string tools.

---

## 🚀 How to Import into Geometry Dash 2.2

### Method 1: Native Geometry Dash Level Import
1. Open **Geometry Dash 2.2**.
2. Go to **Create** -> **My Levels**.
3. Click the **Import** button.
4. Select `Void_Leviathan.gdlvl`.
5. The level **Void Leviathan** will appear in your level list, ready to play or edit!

### Method 2: Raw Level String
- Open `level_string.txt` and copy the contents to paste into any custom level tool or GD save file manager.

---

## 🛠️ Building & Validating the Level

### 1. Generate / Rebuild Level Files
To rebuild or modify the level structure and generate `Void_Leviathan.gdlvl`:
```bash
python3 generate_level.py
```

### 2. Run Test Suite
To verify the XML structure, Base64 description, Base64-gzipped `k4` level string, GD 2.2 tags (`k80=22`, `k48=1260`), triggers, boss fight group references, and game mode portals:
```bash
python3 test_level.py
```
