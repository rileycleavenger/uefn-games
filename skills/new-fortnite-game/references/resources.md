# Resources (curated 2026-10-14)

Star counts and dates were checked against the GitHub API on 2026-10-14. Re-check before you depend on anything, because new UEFN repos appear and die fast.

## Official (use these first)
| Resource | Why |
|---|---|
| [UEFN MCP](https://dev.epicgames.com/documentation/fortnite/uefn-mcp) | Setup and toolsets for the editor MCP. |
| [Unreal MCP (UE 5.8)](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor) | The underlying plugin: transport, security, meta-tools. |
| [Verse Language Reference](https://dev.epicgames.com/documentation/en-us/fortnite/verse-language-reference) and [Quick Reference](https://dev.epicgames.com/documentation/en-us/fortnite/verse-language-quick-reference) | The canonical syntax reference. |
| [Book of Verse](https://verselang.github.io/book/) ([source](https://github.com/verselang/book), CC0) | The fullest language book. It tracks Verse's main branch, so a few features may not have shipped in UEFN yet. |
| [Verse API reference](https://dev.epicgames.com/documentation/en-us/fortnite/verse-api) | Generated from the digests. Use it to check that an API exists. |
| Your project's `*.digest.verse` files | **The ground truth** for the exact signatures in the user's build. |
| [Programming with Verse hub](https://dev.epicgames.com/documentation/en-us/fortnite/programming-with-verse-in-unreal-editor-for-fortnite) | Onboarding, creating a device, debugging, Scene Graph. |
| [Persistence](https://dev.epicgames.com/documentation/en-us/fortnite/using-persistable-data-in-verse) and [persistence best practices](https://dev.epicgames.com/documentation/fortnite/verse-persistence-best-practices) | Required reading before you publish any saved data. |
| [Starter templates and feature examples](https://dev.epicgames.com/documentation/en-us/fortnite/unreal-editor-for-fortnite-starter-templates) | Inside UEFN's Project Browser. Most useful: Verse Device, Gunfight (join, rejoin), **Speedway Race with Verse Persistence**, User Interfaces, Procedural Building. |
| [Epic Snippet Repository](https://dev.epicgames.com/community/fortnite/snippets) | Community snippets hosted by Epic. Quality varies, and older snippets may not compile. |
| [Fortnite Data API](https://dev.epicgames.com/documentation/en-us/fortnite/using-fortnite-data-api-in-fortnite) | Public island metrics (players, retention). Use it to check that a genre has an audience. |
| [Fortnite Developer Rules](https://legal.epicgames.com/fortnite/developer-rules) (needs an Epic login) | What gets an island rejected or removed, including the gambling ban (1.11, 1.15.5). See publishing.md. |
| [EpicGames/unreal-engine-skills-for-claude-code-plugin](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin) (MIT) | Epic's Claude Code plugin for full Unreal. Its `unreal-mcp` skill teaches the same list → describe → call flow and safety rules. It doesn't mention UEFN, and `create-toolset` probably doesn't apply there. |

## Claude skills and AI tooling
| Resource | Status | Why |
|---|---|---|
| [magnusenebakk-epic/verse-skill](https://github.com/magnusenebakk-epic/verse-skill) | ~17 stars, active Oct 2026, written for UEFN 42.30; licence not shown | **Install it alongside this skill** (`git clone … ~/.claude/skills/verse`). It's a deep Verse + Scene Graph + editor-MCP reference with error codes and gotchas, apparently by an Epic staffer (unconfirmed). This skill covers the workflow; that one covers the language detail. |
| [KirChuvakov/uefn-mcp-server](https://github.com/KirChuvakov/uefn-mcp-server) | 71 stars, Oct 2026, MIT | The most mature community MCP (110 tools, Verse LSP navigation, crash relaunch). Optional add-on, not a replacement. It exposes `execute_python`: read every script before you run it. |
| [ViggoJonssonF/uefn-claude-automation](https://github.com/ViggoJonssonF/uefn-claude-automation) | New, MIT | A compile → session → in-game Verse self-test → log/screenshot loop driven by Claude. A good pattern for testing-and-review.md. |
| [abafaboy/islandsmith](https://github.com/abafaboy/islandsmith) | New, MIT | Agent skills for an MCP driver, verification, a list of UEFN traps and a pre-publish check. Worth reading for ideas. |
| [novikit/uefn-mcp-pro](https://github.com/novikit/uefn-mcp-pro) | New, MIT | Its README has a frank comparison of Epic's MCP with community bridges. Read it; don't depend on it. |
| [mimmo-the-root/UEFN-dream-bot-team](https://github.com/mimmo-the-root/UEFN-dream-bot-team) | 9 stars, MIT | A multi-agent Claude Code kit with gated reviews. Heavy, but a pattern to borrow from. |
| [vz-creates/uefn](https://github.com/vz-creates/uefn) | 95 stars, active, no licence | The Verse digests for every UEFN version from v24 to v44. **The best way to diff API changes between versions.** Read only. |

## Editor tooling
| Resource | Why |
|---|---|
| Epic's Verse VS Code extension | It comes with UEFN (Verse menu → Open in VS Code). It's the real language server. |
| [vukefn/verse-auto-imports](https://github.com/vukefn/verse-auto-imports) | Adds missing `using { }` lines. The most-used community extension. Its licence is unclear. |
| [quangdang46/verse-lsp](https://github.com/quangdang46/verse-lsp) (MIT) | A standalone language server built from the digests. Niche: for editors other than VS Code, or for CI. |

## Verse libraries and examples
| Resource | Why |
|---|---|
| [sprintermax/UEFNVerseSnippets](https://github.com/sprintermax/UEFNVerseSnippets) (MIT, active) | The best general utility library: maths, strings, JSON, time, concurrency helpers. |
| [Ep8Script/ScreenSpace](https://github.com/Ep8Script/ScreenSpace) (MIT, active) | Viewport and Scene Graph helpers such as world-to-screen and raycasts. |
| [ZeroYaHero/VerseNoise](https://github.com/ZeroYaHero/VerseNoise) (MIT), [VerseVolumes](https://github.com/ZeroYaHero/VerseVolumes) (Apache-2.0) | Small, focused libraries: noise, and trigger volumes in Verse. |
| [simnJS/prism-verse](https://github.com/simnJS/prism-verse) (MIT, alpha) | Generates persistence code from a schema and refuses breaking changes. A good idea to copy; too young to depend on. |
| [VerseMetaVerse/UnrealVerse](https://github.com/VerseMetaVerse/UnrealVerse) (MIT) | A big link list. Some links are stale. |

## Art and assets
| Resource | Why |
|---|---|
| Fab (inside UEFN, or fab.com) | Free assets. Check each asset's licence. See asset-pipeline.md. |
| Blender + Blender MCP | All custom models: headless scripts plus previews. |
| MetaHuman Creator | Realistic characters. See asset-pipeline.md for the UEFN limits. |
| Mixamo | Free humanoid animations (Adobe account). |
| Sketchfab | Use CC0 or CC BY models only, and credit the author. |

## Avoid
- **Anything that breaks Epic's terms:** "Play in Editor" through private Fortnite servers (bc2424/UEFN-PIE, uefn-util), AES-key grabbers, unlockers and DLL injectors (UEFN-AESFinder, UEFN-AES-grabber, UEFN-AES-Loader, UEFN-Unlocker). They risk the account ban and malware.
- **Ripped assets and "community prefabs" of Fortnite or other games' content.** IP risk, and the island gets rejected.
- **Re-uploads with near-identical names**, e.g. copies of UEFN-TOOLBELT that aren't GitHub forks. This is a common malware lure.
- **undergroundrap/UEFN-TOOLBELT:** AGPL-3.0 with an added credit clause. Skip it unless copyleft is fine.
- **Old one-person Python-listener MCPs.** They overlap Epic's MCP, often expose arbitrary Python, and reportedly broke when the MCP beta changed Python start-up.
- **Verse collections from 2023 and 2024** (awesome-verse, VerseReferenceExplorer and similar). They predate Scene Graph and later API changes, and much of their code won't compile.
- **Paid "AI Verse fixer" extensions.** They send your code to third parties. The real compiler diagnostics come from `BuildAll`.
- **Code-generator marketing repos** (e.g. uefncentral examples). Search them for patterns, but never trust their code without building it.
