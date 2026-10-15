# Asset pipeline: Blender, Fab, MetaHumans → UEFN

Researched 2026-10-14. Budget: **$0 apart from fees**. Free assets only, and every licence is recorded in `docs/CREDITS.md`.

## 0. What you don't make in Fortnite
- **Player characters are the players' own Fortnite outfits.** Don't build player avatars. I found no supported way to replace a player's outfit with a custom model; only third-party Verse tricks. [?]
- Use custom characters for **NPCs**: guards, shopkeepers, bosses. Spawn them with the NPC Spawner.
- Weapons and items come from Fortnite's item set, through Item Granters, Item Spawners and Class Designer. Custom meshes can dress props and pickups, but the guns' behaviour is Fortnite's.
- Epic's own assets may be used only as UEFN provides them (rule 1.7.1). **No recreated Fortnite skins, characters or music**, in the island or in its thumbnails.

## 1. Import limits and formats
Source: https://dev.epicgames.com/documentation/en-us/fortnite/importing-assets-in-unreal-editor-for-fortnite
- **Models:** FBX, OBJ, **glTF/GLB**.
  - FBX uses the FBX import options. Everything else goes through **Interchange**, which has pipelines for static meshes, skeletal meshes, animation, materials and textures.
- **Textures:** PNG, JPG/JPEG, TGA, PSD, TIF/TIFF, BMP, DDS, EXR, HDR, PCX.
- **Audio:** WAV, OGG, FLAC, AIF.
- **Data:** CSV, JSON. Also `.island` and `.upack`.

Guidance from Epic's FortniteReady best practices (https://dev.epicgames.com/documentation/fortnite/fortniteready-assets-best-practices-in-fortnite). These are guidelines, not hard limits:
- **LOD0 triangles:** about 400–2,500 for simple, 700–6,000 for medium, and 1,200–9,000 for complex objects. Be careful above 20k vertices without LODs.
- **LODs:** about 3, each roughly half the previous one. Since v42.00, imported meshes default to Min LOD 2 on Low/Medium quality, which covers mobile and handhelds.
- **Collision:** at most 10 UCX hulls.
- **Textures:** 2048 px or less, power of two, with mips. Textures with "No Mipmaps" now fail validation. Use 512 px for Switch and mobile.
- **Scale:** units are cm. The build grid is **512 cm** and the player is about **192 cm** tall.
- **Nanite:** enabled per mesh, with a fallback mesh for platforms without Nanite. Lower "Keep Triangle Percent" to save memory.

## 2. The memory budget (it gates publishing)
Source: https://dev.epicgames.com/documentation/en-us/fortnite/memory-management-in-unreal-editor-for-fortnite and the 42.30 notes.
- The budget is **100,000 memory units per streaming area**. From v42.20/42.30 the limit **displays as 300 MB**; the budget itself is unchanged.
- **You can't publish or update an island over the limit**, though you can exceed it while editing.
- How to measure:
  1. Launch Session, then End Game, so the assets get cooked.
  2. Project → **Launch Memory Calculation** → Calculate Memory.
  3. The 100 heaviest assets appear in Window → Message Log ("Memory Test Results").
  4. For runtime memory, use Memory Snapshot and Spatial Profiler.
  - Live edits don't update the cooked numbers. Push before you measure.
- How to cut it:
  - Reuse a few asset variants.
  - Use fewer **device types**. Each type costs memory in every cell; repeat copies are cheap.
  - Spread content out so cells can stream.
  - Use Data Layers.
  - Turn on "Is Spatially Loaded".
  - Use HLODs only for things visible from far away.
  - Use smaller textures.
  - Use Nanite with a low keep percentage.
- Other limits:
  - Project upload size **2 GB**, download size **400 MB**. These come from the MetaHuman template page and may be dated. [?]
  - Fab content: "exceeds 256 MB, you will not be able to deploy." [?]
- **Run the memory calculation after every art batch** and record the number in `docs/NEXT_STEPS.md`. Treat 80% of the budget as the warning line.

## 3. Blender → UEFN (the default for custom props)
This mirrors Casino Royale's pipeline. Models are **Python scripts**, run headless and re-runnable, so they can be diffed and reviewed. Each run writes a `.glb` plus a preview render. Templates: `templates/tools/blender/`
- `uefn_common.py`: scene reset, materials, boxes, joins, finishing, budget checks, glTF export, a preview with a 1.92 m scale pillar.
- `build_models.py`: the runner.
- `example_prop.py`: a 5.12 m market stall.
- `contact_sheet.py`: tiles previews into one labelled image (needs Pillow).

```
blender --background --factory-startup --python tools/blender/build_models.py -- example_prop
py tools/blender/contact_sheet.py SM_ build/models/sheet.png
```
The template was checked on 2026-10-14 with Blender 5.2.2: it printed `MODEL SM_MarketStall tris=552 size_cm=(512, 229, 283)` and rendered a preview.

Rules carried over from Casino Royale's LESSONS:
- 1 Blender unit = 1 m. Z-up. Put the pivot where the object meets the floor.
- glTF import keeps orientation: Blender X/Y/Z extents = Unreal X/Y/Z extents, and metres become cm. Check the printed `size_cm` against the GDD.
- **Surfaces need texture maps, not flat colours.** The director rejected flat-coloured models. Generate tiling PBR maps (Casino Royale's `textures.py` does it with numpy inside Blender) and keep every texture a power of two and ≤ 2048 px.
- Smooth by angle plus face-area weighted normals. Plain smoothing darkens big flat faces.
- **Check the preview before importing.** Look at the contact sheet. Compare scale with the 1.92 m pillar.
- Re-importing over an existing asset can keep stale material instances. Delete the asset's old materials and textures first, or import into a fresh folder.
- Never import while a session is running.
- Use the **Blender MCP** (`uvx blender-mcp`, the `blender` server in `.mcp.json`) for interactive look-dev. Once a look is approved, write it into a script.

Import into UEFN:
1. Preferred: the human drags `build/models/*.glb` into the Content Browser folder `/<Project>/Models/<Group>`. Interchange settings: static mesh, generate collision (simple), Nanite on for dense meshes. Takes about a minute.
2. Automated: [?] Python Editor Scripting is on (it's needed for the MCP), and the MCP has `AssetTools`, `StaticMeshTools` and `ProgrammaticToolset`. Run `describe_toolset` and look for an import function first. If there isn't one, don't fake it: ask the human to drag the files in.
3. After the import, `StaticMeshTools` / `ObjectTools` can read the bounds and set Nanite and collision (confirm the tools with `describe_toolset`). Place one in the level next to a player spawner and capture a viewport screenshot to check scale.

Optional: skinned meshes from Blender. Retarget animations to Fortnite's mannequin with IK Rig / IK Retargeter, using `FN_Mannequin` from the Animation 101 template. Play them with the Animated Mesh device or Sequencer. Sources:
- https://dev.epicgames.com/documentation/en-us/fortnite/transfer-character-animations-in-unreal-editor-for-fortnite
- https://dev.epicgames.com/documentation/en-us/fortnite/import-and-play-mesh-animations-in-unreal-editor-for-fortnite

Don't build human characters out of rigid Blender primitives. The director said they look "like Roblox characters". Use MetaHumans (below).

## 4. MetaHumans (realistic NPCs)
Source: https://dev.epicgames.com/documentation/en-us/fortnite/metahuman-overview-in-unreal-editor-for-fortnite
- Supported and free in UEFN since March 2024.
- Create the character in **MetaHuman Creator for Unreal Engine** (inside UE 5.6+). The old web app is being discontinued. This needs the free full Unreal Engine install, and the user already has UE 5.8.
- Assemble with the **UEFN Export** option. Close UEFN while exporting.
- In UEFN, open Window (or right-click in the Content Browser) → **MetaHuman Importer**.
- **Memory:** about **60 MB** each in UEFN, versus about 800 MB–1 GB in full UE. Body and face have 4 LODs each.
  - Export quality: High for close-ups, Medium, or Low for crowds (hair cards, no correctives).
  - Epic: MetaHumans "are memory intensive… limit how many". Budget 2–4 unique MetaHumans and re-run the memory calculation after each one.
- **NPC setup:**
  1. Create an NPC Character Definition: Type = Custom (Verse `npc_behavior`); Cosmetic Modifier → Character Look = **Custom Character** (your MetaHuman Blueprint); Animation Preset `AnimPreset_MetaHumanLocomotion`.
  2. Place an NPC Spawner and give it that definition.
  - Source: https://dev.epicgames.com/documentation/en-us/fortnite/using-the-npc-spawner-with-animations-in-unreal-editor-for-fortnite
- **Animation:**
  - Locomotion comes preloaded.
  - Custom FBX clips can be imported against `metahuman_base_skel`.
  - In Verse, use `Play()` and `PlayAndAwait()`. The clips must appear in `Assets.digest.verse`.
  - NPC animation is **Early Access**.
  - While Sequencer drives an NPC, its behaviour is paused.
- **Clothing and themed outfits:** build them in MetaHuman Creator (its own wardrobe), or fit Blender garments to the MetaHuman body. The second path is untested in UEFN [?]. Prototype one NPC end to end before planning a cast.
- **Conversations (LLM-voiced NPCs)** launched as **Experimental** in April 2026, and experimental features can't be published. Don't build the core loop on it. Rule 1.22 restricts personas.

## 5. Fab (free assets)
Source: https://dev.epicgames.com/documentation/fortnite/import-from-fab-in-unreal-editor-for-fortnite
- **In UEFN:** Window → Fab, or the Fab button in the Content Browser. Accept the Fab EULA. Filter Included formats → **UEFN**. Imports land in a Referenced Content folder.
- **Referenced vs Modifiable:**
  - **Referenced:** used by path, auto-updated, faster moderation. You can't change LODs or collision, and it's **not compatible with Scene Graph**.
  - **Modifiable:** editable, but detached from updates, and moderation is slower.
  - New "UEFN Source" assets (fully editable projects) open on Fab from 2026-10-15.
- **Licences** (https://dev.epicgames.com/documentation/fab/licenses-and-pricing-in-fab):
  - Each listing states its licence. Free listings are usually **CC BY 4.0** (credit the author, link the licence, note your changes) or Fab's **Standard** licence.
  - "Regardless of license type, you must provide attribution to third party assets used on your island when you publish." Use the Creator Portal **Attribution** step and keep `docs/CREDITS.md` in sync.
- **Browsing Fab with computer use** (the user allows this, through the Epic Games Launcher or fab.com):
  - Filter by Free and by the UEFN format.
  - **Never click Buy on anything with a price.** "Add to My Library" on a $0 item is fine. Stop and ask if a checkout or payment screen appears.
  - Screenshot each candidate's licence panel and save its URL into CREDITS.
  - Prefer Fab's limited-time free monthly assets only after the licence check: what you add to your library while free stays yours.
- Rule from the field reports: **don't build a chair from scratch.** Pull an asset and let Claude arrange it. Model in Blender only what Fab doesn't have, or what needs the game's own style.

## 6. Other free sources
- **Sketchfab:** CC0 or CC BY only. No NC ("non-commercial"), because islands earn Engagement Payouts. No "editorial" or brand models. Download FBX or glTF, clean up in Blender (scale, pivot, tris, textures), then follow section 3.
- **Mixamo:** free humanoid animations and characters with an Adobe account. Adobe's terms allow use in projects but not redistribution of the raw files. Retarget to `FN_Mannequin` or the MetaHuman skeleton. Credit it in CREDITS.
- **Audio:** synthesise simple SFX with a script (Casino Royale's `tools/audio/make_sounds.py` approach), or use CC0 sources. Use WAV or OGG.
- **AI-generated assets:** record the tool, model version, its licence and your clean-up in CREDITS. Casino Royale's notes:
  - Hunyuan3D's licence excludes the EU, UK and South Korea.
  - TRELLIS.2 is MIT, but its default background remover is non-commercial.
  - Meshy's free-plan outputs are CC BY 4.0.
- **Never use:** ripped game assets, AES-key extracted Fortnite content, "fan" recreations of brands or characters, or real logos.
