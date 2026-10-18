# Technical Documentation and Implementation Guide: Geometry Dash `.gdlvl` Files

## Objective

Learn, investigate, and document exactly how the Geometry Dash `.gdlvl` file format works, how a level is represented internally, and how to construct a valid `.gdlvl` file from scratch.

Do not rely on guesses or treat the file as a generic compressed document. Use technical documentation, real exported level files, and established implementations to verify the format. Distinguish confirmed facts from assumptions, undocumented behavior, and game-version-specific details.

The final goal is to understand every layer involved in transforming level data into a `.gdlvl` file that Geometry Dash can import and play.

## 1. What is a `.gdlvl` file?

The `.gdlvl` extension is Geometry Dash's level-export file format, available since version 2.209.

According to the community-maintained GD Docs reference, the format is essentially equivalent to the older, unofficial `.gmd` format used by GDShare, except that the entire XML file is compressed using Gzip and encoded with Base64.

When decoded correctly, a `.gdlvl` file contains an XML document describing a level and its associated properties.

A level file is not simply an image, a video, a model, or a collection of graphical assets. It contains structured data that Geometry Dash interprets to construct the level inside its editor and gameplay environment.

The important distinction is that the file has several layers:

1. **The `.gdlvl` container:** the exported file's outer encoding.
2. **The XML document:** the level metadata and properties.
3. **The inner level string:** the settings and serialized object data used to describe the level.
4. **Individual objects:** blocks, decorations, triggers, portals, and other supported level objects, each with properties.
5. **The game interpreter:** Geometry Dash reads the data and reconstructs the level.

These layers must not be confused with one another.

## 2. The outer encoding and decoding process

The outer `.gdlvl` file uses Gzip compression and Base64 encoding.

The general encoding pipeline is:

1. Construct a valid XML document representing the level.
2. Encode the XML as UTF-8 bytes.
3. Compress the XML bytes using Gzip.
4. Encode the resulting compressed bytes using the appropriate Base64 representation.
5. Write the resulting encoded data to a file with the `.gdlvl` extension.

Conceptually:

`XML document → UTF-8 bytes → Gzip compression → Base64 encoding → .gdlvl`

To decode the exported file, reverse these operations:

` .gdlvl → Base64 decoding → Gzip decompression → UTF-8 XML`

The decompressed result should be a readable XML document, not another arbitrary binary file.

Implement both operations carefully. Do not mix up Gzip, raw DEFLATE, and Zlib. Although their underlying compression mechanisms are related, they are not interchangeable file wrappers.

Also, verify the precise Base64 alphabet and padding conventions by examining a real game-generated `.gdlvl`. Do not assume every Geometry Dash encoding uses identical Base64 conventions.

### Important distinction

The outer file encoding is separate from the representation of the level string inside the XML.

The inner level string has its own serialization rules and Base64 encoding. Encoding the entire XML for export does not eliminate the need to serialize the inner level data correctly.

Consult:

- https://boomlings.dev/resources/client/level
- https://boomlings.dev/resources/client/level-components/level-string
- https://boomlings.dev/resources/client/level-components/level-start

## 3. The XML document and metadata

The decoded XML contains key/value pairs identifying the level's properties.

The documented field names use identifiers such as `k1`, `k2`, `k3`, and `k4`. These identifiers are meaningful to Geometry Dash; they are not arbitrary labels.

Important documented fields include:

| Field | Meaning |
|---|---|
| `k1` | Level ID |
| `k2` | Level name |
| `k3` | Description, encoded with Base64 |
| `k4` | Start-level object string containing the playable level data |
| `k5` | Creator name |
| `k6` | Creator user ID |
| `k7` | Level difficulty |
| `k8` | Official song ID |
| `k13` | Editable status |
| `k14` | Verification status |
| `k16` | Level version |
| `k17` | Game version |
| `k23` | Level length |
| `k45` | Custom song ID |
| `k47` | Whether the level has been modified externally |
| `k48` | Object count |

This table describes selected documented fields, not every key in the format.

Some values concern the level's contents, while others describe its creator, editor state, local progress, or other metadata. Not every field is equally important when constructing a new local level, and some values may be assigned or adjusted by the game itself.

### XML implementation requirements

Investigate the precise XML representation and value types using a valid `.gdlvl` exported by the game.

Determine:

- The exact root element and dictionary structure.
- How XML keys and their associated values are represented.
- Which fields are required for a working level.
- Which fields are optional, generated, or specific to a particular game version.
- How integers, strings, booleans, and other values are encoded.
- How special characters are escaped in XML.
- Whether unknown keys must be preserved when editing an existing file.

Use a proper XML parser and serializer rather than fragile string replacement.

Do not fabricate metadata values simply because the format contains a documented key. Some fields may be irrelevant to a newly created local level, while others may influence how Geometry Dash interprets it.

## 4. The inner level string

The inner level string is where the actual level configuration and objects are represented.

According to GD Docs, the start-level string is Base64-encoded. Its decoded representation has the following general structure:

`{level_start};{object_string}`

The first component describes the initial state and settings of the level. The second contains the serialized objects.

The start-level section is special. It is not an ordinary block object and does not use an ordinary object ID.

Its properties use identifiers such as:

- `kA1`: Audio track.
- `kA2`: Starting game mode.
- `kA3`: Mini mode.
- `kA4`: Starting speed.
- `kA6`: Background texture ID.
- `kA7`: Ground texture ID.
- `kA8`: Dual mode.
- `kA11`: Gravity flip.
- `kA13`: Song offset.
- `kA22`: Platformer mode.
- `kA28`: Mirror mode.
- `kA29`: Rotated gameplay.

These are examples of documented properties. Consult the complete reference for the rest of the start-level settings and their valid values.

The inner string is then Base64-encoded according to the documented level-string representation. Determine the exact value stored in XML field `k4` by decoding an actual exported file instead of assuming that the raw representation and stored representation are identical.

## 5. How individual objects are serialized

The object section consists of objects separated by semicolons.

The general syntax is:

`{object};{object};{object};...`

Each object consists of comma-separated property key/value pairs:

`{propertyKey},{propertyValue},{propertyKey},{propertyValue},...`

For example, the following is a documented object string:

`1,1,2,15,3,15,21,3,24,7;`

It describes a standard block with:

- Object ID `1`.
- X position `15`.
- Y position `15`.
- Main color channel ID `3`.
- Z layer `7`.

This illustrates the format's fundamental structure. It is not, by itself, a complete level file.

### Essential properties

Every ordinary object must contain at least these three properties:

| Property key | Meaning |
|---|---|
| `1` | Object ID |
| `2` | X position |
| `3` | Y position |

The coordinate values are represented as numbers. Even when an object's X or Y coordinate is zero, the corresponding properties should still be included.

Other property identifiers represent object-specific settings. Examples include:

| Property key | Meaning |
|---|---|
| `4` | Horizontal flip |
| `5` | Vertical flip |
| `6` | Rotation |
| `20` | Editor Layer 1 |
| `21` | Main color channel ID |
| `22` | Secondary color channel ID |
| `24` | Z layer |
| `25` | Z order |
| `32` | Object scaling |
| `33` | Single group ID |
| `35` | Opacity |
| `57` | Group IDs |

This is only a subset of the documented properties. Geometry Dash 2.2 introduced many more properties, and triggers, portals, animated objects, and other object types have their own settings.

### Property value formats

The documented representation uses the following conventions:

- Integers are written as decimal numbers.
- Boolean values are represented by `1` or `0`.
- Floating-point values use a period as the decimal separator.
- Integer arrays use periods between values.
- HSV data follows a special multi-value representation.
- Strings are represented without adding quotation marks around the values.

For instance, an object rotation is represented by its numeric rotation property. A group assignment uses a group identifier. Color-channel assignments are represented by their respective properties.

The exact valid values depend on the relevant object type and property.

### Object IDs and validity

An object ID identifies which game object Geometry Dash should instantiate. It is not merely a descriptive name.

Using a valid object ID is therefore essential. An arbitrary ID does not automatically produce a useful or supported block.

Investigate which object IDs correspond to the blocks, decorations, triggers, portals, and other assets intended for use.

When creating a file programmatically, maintain an internal object representation first and serialize it afterward. This is much safer than attempting to construct the entire serialized string through unstructured text concatenation.

## 6. Constructing a `.gdlvl` file from scratch

Use the following general workflow.

### Step 1: Obtain a valid reference file

Create a minimal test level in Geometry Dash and export it as `.gdlvl`.

Keep the file unchanged as a reference. It is the best way to establish the actual XML structure, metadata defaults, and inner encoding used by the target version of the game.

### Step 2: Decode the file

Read the file as bytes.

Base64-decode its contents and decompress the resulting bytes with a Gzip decoder. Validate the resulting UTF-8 XML document.

Report meaningful errors when decoding, decompressing, or parsing fails.

Do not silently replace corrupted data with an empty level.

### Step 3: Inspect the XML

Parse the XML and identify:

- The metadata fields.
- The level name.
- The inner level data in `k4`.
- The starting configuration.
- The object string.
- The way the game represents empty or optional fields.

Document the actual observed structure before attempting to create a new file.

### Step 4: Construct the level configuration

Define the initial level settings, such as the starting game mode, speed, background, ground, and other relevant options.

Use documented enumeration values and validate them.

Do not confuse the starting configuration with a normal in-level trigger. They are represented differently.

### Step 5: Construct the objects

Represent each intended level object with an object ID, X/Y coordinates, and its required properties.

Assign valid values to properties such as rotation, scale, color channels, Z order, and groups when applicable.

Serialize each object into comma-separated property/value pairs, then join the objects with semicolons. Follow the required delimiters exactly.

Preserve a trailing semicolon where required by the documented format.

### Step 6: Serialize the inner level string

Combine the serialized starting configuration with the object section using the documented delimiter.

Apply the inner level-string encoding expected by the XML field. Verify this against the reference file so the data is not accidentally encoded twice or placed at the wrong level.

### Step 7: Construct the XML

Insert the correctly serialized level data into the XML document.

Set the level's name and any necessary metadata. Follow the real file's element and value conventions, and ensure the XML is syntactically valid.

Use a reliable XML library to handle escaping and serialization.

### Step 8: Encode the outer file

Encode the XML as UTF-8 bytes, compress the bytes with Gzip, and Base64-encode the compressed result.

Save the output with the `.gdlvl` extension.

### Step 9: Import and test the file

Import the exported file through Geometry Dash's own level-import workflow.

Confirm that the level appears in the editor, contains the expected objects, preserves the intended settings, and can be played.

A file that successfully decompresses is not necessarily a valid Geometry Dash level. Only an actual game import and subsequent inspection can verify practical compatibility.

## 7. How triggers and advanced objects work

A level's objects can be more than static blocks.

The serialized object representation also supports triggers and other interactive objects that change level behavior.

Depending on the supported game version, objects may configure or activate effects such as:

- Movement and rotation.
- Color changes, pulses, and fades.
- Group activation.
- Opacity changes.
- Spawn behavior.
- Player mode, speed, and gravity changes.
- Camera behavior and other advanced effects.

These features depend on the relevant object IDs and their properties. A trigger is not implemented merely by assigning an arbitrary property to a standard block.

To support such features, consult the object-property documentation and verify the intended object's supported properties. Preserve group identifiers, color channels, activation properties, timing values, and target references when applicable.

For any level format implementation, distinguish between successfully serializing a trigger and producing the behavior that the game actually expects.

## 8. Compatibility and common mistakes

Investigate and guard against the following problems.

**Incorrect compression:** A Gzip-compressed XML document is not the same thing as a raw XML file, a ZIP archive, or a Zlib stream.

**Incorrect Base64 handling:** The outer `.gdlvl` file and its inner level string have separate encoding requirements.

**Malformed XML:** Missing elements, improperly escaped characters, incorrect value types, or malformed dictionaries may cause import failures.

**Malformed object strings:** Missing commas, missing coordinates, invalid delimiters, or malformed property pairs can make the level data unreadable.

**Invalid object IDs:** A syntactically valid object does not guarantee that Geometry Dash can instantiate it.

**Unsupported properties:** A property documented for a particular version or object type may not work universally.

**Incorrect metadata:** Do not assume that local identifiers, creator information, verification fields, or other metadata can be copied blindly between levels.

**Unverified assumptions:** Community documentation can contain incomplete or version-specific information. Compare uncertain fields with exports created by the exact game version being targeted.

**Testing only the encoding:** Successful Base64 decoding and Gzip decompression demonstrate only that the outer container is readable. The resulting XML, inner level string, objects, and in-game behavior must also be checked.

## 9. Implementation requirements for Jules

Investigate the existing format thoroughly and produce a reliable implementation rather than merely writing a superficial explanation.

The implementation should include:

1. A `.gdlvl` reader that decodes Base64, decompresses Gzip, and parses the resulting XML.
2. A clear representation of level metadata and settings.
3. An inner level-string parser capable of separating the start-level configuration from the object list.
4. An object parser that reads property/value pairs and preserves valid object properties.
5. A serializer that can construct objects and the inner level string from structured data.
6. An XML writer that produces correctly structured, well-formed output.
7. A `.gdlvl` exporter that performs the correct outer compression and encoding.
8. Validation and useful error reporting.
9. Round-trip tests comparing an original file with a decoded and re-encoded version.
10. A final test that imports a generated file into Geometry Dash and verifies that the expected level appears and behaves correctly.

Do not assume that every field must be regenerated. For maximum compatibility, preserve unknown but valid properties when modifying an existing level, unless there is a documented reason to change them.

When creating a file from scratch, begin with a minimal level and add features incrementally. This makes it easier to isolate malformed metadata, serialization errors, unsupported properties, and import problems.

## 10. Testing strategy

Build a small test suite that includes:

- A level containing a single standard block.
- A level containing multiple blocks at different positions.
- A level using different rotations, colors, layers, and object properties.
- A level containing a nontrivial starting configuration.
- A level containing a supported trigger, once basic serialization works.
- A level containing escaped text or other special characters in applicable metadata fields.
- An existing file that is decoded, re-encoded, and compared with the original.

For round-trip testing, distinguish byte-for-byte equivalence from semantic equivalence. Gzip output and XML serialization may differ while still representing the same level. Compare decoded XML and parsed level data as well as the original bytes.

For the final test, use Geometry Dash itself as the authority on whether a generated file is genuinely importable.

## 11. Primary technical references

Use these references as the starting point for research:

**GD Docs — Client Level Resource**

https://boomlings.dev/resources/client/level

Documents level metadata, XML fields, and the `.gdlvl` format.

**GD Docs — Level String Resource**

https://boomlings.dev/resources/client/level-components/level-string

Documents object serialization, property identifiers, value formats, and object delimiters.

**GD Docs — Level Start Resource**

https://boomlings.dev/resources/client/level-components/level-start

Documents how the starting level configuration is represented.

**GD Docs — Enumerations**

https://boomlings.dev/resources/client/level-components/enumerations

Documents enumeration values used by various level properties.

**GDShare-CLI**

https://github.com/HJfod/GDShare-CLI

Provides an established reference for working with Geometry Dash level data and legacy interchange formats. Check which formats the implementation actually supports; do not assume that every GDShare format has identical encoding or capabilities.

## Final objective

By the end of the investigation, be able to explain precisely how a `.gdlvl` file moves through the following stages:

**Exported bytes → Base64 decoding → Gzip decompression → XML parsing → inner level-string decoding → starting configuration and object parsing → structured level representation.**

Also implement the reverse process and demonstrate that a newly generated file can be imported into the actual game.

Keep every conclusion grounded in the documentation, observed files, or tested behavior. Where the format is undocumented, explicitly identify the uncertainty and investigate it instead of inventing details.
