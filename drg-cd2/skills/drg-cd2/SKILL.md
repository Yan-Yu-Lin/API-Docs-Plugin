---
name: drg-cd2
description: >-
  Unofficial documentation for Deep Rock Galactic Custom Difficulty 2 (CD2), a popular modding
  framework for creating custom difficulty settings. This skill should be used when working with
  CD2 difficulty configurations, enemy scaling parameters, hazard modifiers, special enemy pools,
  or any custom difficulty setup in Deep Rock Galactic. Covers difficulty tier definitions,
  enemy stat scaling formulas, spawn rate modifiers, environmental hazards, and advanced
  customization options for creating challenging or unique gameplay experiences.
---

# Deep Rock Galactic Custom Difficulty 2 (CD2)

Custom Difficulty 2 is a modding framework for Deep Rock Galactic that allows players to create and share custom difficulty settings beyond the base game's Hazard 1-5 system. Developed by @TheBrain as a successor to Custom Difficulty 1, CD2 offers extensive control over enemy behavior, spawning mechanics, mission parameters, and more.

## Key Features

- **Mutators**: Control-flow structures for dynamic values based on game conditions
- **Enemy Customization**: Modify health, damage, speed, appearance, and projectiles
- **Wave Spawners**: Create custom enemy waves triggered by game events
- **Pool Manipulation**: Add/remove enemies from spawn pools dynamically
- **Mission Controls**: Customize resupply costs, lighting, special encounters, and mission-specific mechanics
- **Multiplayer Support**: Works with 4+ player lobbies and Deep Dives

## File Format Basics

CD2 files use **JSON format**. Key rules:

- An empty file `{}` equals vanilla Hazard 5
- Missing fields inherit from `BaseHazard` (default: Hazard 5)
- Most numeric fields accept arrays for player-count scaling: `[solo, 2p, 3p, 4p]`
- CD1 files are **not** compatible (use [conversion script](https://github.com/vonacht/cd2ifier))

**Minimal example - Hazard 5x2:**
```json
{
  "Name": "Hazard 5x2",
  "Caps": {
    "MaxActiveSwarmers": [90, 120, 180],
    "MaxActiveEnemies": [90, 120, 180]
  },
  "Resupply": { "Cost": 60 },
  "DifficultySetting": {
    "BaseHazard": "Hazard 5",
    "EnemyCountModifier": [1.7, 1.7, 2.5, 3]
  }
}
```

## Reference Documentation

### Core References

| File | Description |
|------|-------------|
| [basics.md](references/basics.md) | CD2 GUI, file format fundamentals, and simple examples |
| [modules.md](references/modules.md) | All top-level modules (`DifficultySetting`, `Caps`, `Pools`, `Resupply`, `Darkness`, `Warnings`, `Vars`, etc.) |
| [mutators.md](references/mutators.md) | Dynamic value system (`ByPlayerCount`, `IfFloat`, `DuringDread`, triggers, etc.) |

### Enemy System

| File | Description |
|------|-------------|
| [enemies.md](references/enemies.md) | `Enemies`/`EnemiesNoSync` module, descriptor controls, resistances, movement, temperature, spawners, veterans, materials |
| [direct.md](references/direct.md) | Raw UE4 property controls for 50+ enemy types (bulk meatballs, explosion radius, etc.) |
| [projectiles.md](references/projectiles.md) | 140+ vanilla projectiles plus MEV/DEA/EEE mod projectiles for swapping enemy attacks |

### Spawning & Waves

| File | Description |
|------|-------------|
| [wavespawners.md](references/wavespawners.md) | Custom unannounced wave creation with interval, difficulty, and trigger controls |
| [common_edits.md](references/common_edits.md) | Common modifications: enemy count, removing vanilla enemies from pools |

### Expansion Mods

| File | Description |
|------|-------------|
| [mev-dea.md](references/mev-dea.md) | MEV, DEA, and EEE enemy expansion mods - new enemy descriptors and variants |

### Other

| File | Description |
|------|-------------|
| [resources.md](references/resources.md) | Useful links, vanilla descriptor list, external guides |
| [faq.md](references/faq.md) | Common questions about CD2 compatibility, installation, multiplayer |

## Quick Reference Tables

### Essential Modules

| Module | Purpose | Key Fields |
|--------|---------|------------|
| `Name` | Difficulty name (required) | String |
| `DifficultySetting` | Core scaling | `BaseHazard`, `EnemyCountModifier`, `EnemyDamageResistance`, `SpeedModifier` |
| `Caps` | Enemy limits | `MaxActiveEnemies`, `MaxActiveSwarmers`, `MaxActiveCritters` |
| `Resupply` | Nitra cost | `Cost` (supports mutators) |
| `Pools` | Enemy pools | `EnemyPool`, `CommonEnemies`, `DisruptiveEnemies`, `SpecialEnemies`, `StationaryPool` |
| `Enemies` / `EnemiesNoSync` | Enemy customization | See [enemies.md](references/enemies.md) |
| `WaveSpawners` | Custom waves | See [wavespawners.md](references/wavespawners.md) |

### Common Mutators

| Mutator | Returns | Use Case |
|---------|---------|----------|
| `ByPlayerCount` | Any | Scale values by player count |
| `ByTime` | Float | Increase difficulty over time |
| `ByMissionType` | Any | Different settings per mission type |
| `ByBiome` | Any | Biome-specific settings |
| `IfFloat` | Any | Conditional based on numeric comparison |
| `If` | Any | Conditional based on boolean |
| `DuringDread` | Bool | True when dreadnought is active |
| `DuringDefend` | Bool | True during uplink/refuel/black box |
| `DuringExtraction` | Bool | True during extraction phase |
| `EnemyCount` | Int | Count of specific enemy on map |
| `ResuppliesCalled` | Int | Number of resupplies called |
| `DwarvesDown` | Int | Number of downed players |
| `RandomChoice` | Any | Random selection from list |
| `TriggerOnChange` | Bool | Fire when value changes |
| `TriggerDelay` | Bool | Delay a boolean transition |

### Enemy Pools

| Pool | Module Field | Contains |
|------|--------------|----------|
| Common | `CommonEnemies` | Grunts, Praetorians |
| Disruptor | `DisruptiveEnemies` | Menaces, Wardens, Bulks, Stingtails, Shellbacks, Grabbers, Goo Bombers, Stalkers |
| Special | `SpecialEnemies` | Swarmers, Exploders, Web/Acid Spitters, Septics, Mactera Spawns, Trijaws |
| Stationary | `StationaryPool` | Breeders, Nexii, Spitballers, Cave Leeches, Barragers, Scalebrambles |

## Common Tasks

### Increase/Decrease Enemy Count
Modify `EnemyCountModifier` in `DifficultySetting`. May also need to increase `MaxActiveEnemies` in `Caps`.
→ See [common_edits.md](references/common_edits.md)

### Remove Specific Enemies
Use `Pools.<PoolName>.Remove` with the enemy descriptor name.
→ See [common_edits.md](references/common_edits.md), [resources.md](references/resources.md) for descriptor names

### Create Custom Waves
Use `WaveSpawners` with `Enabled`, `Interval`, `Enemies`, `Difficulty`, and trigger mutators.
→ See [wavespawners.md](references/wavespawners.md), [mutators.md](references/mutators.md) for triggers

### Make Difficulty Scale Over Time
Use `ByTime` mutator on `EnemyCountModifier`, `SpeedModifier`, or other fields.
→ See [mutators.md](references/mutators.md)

### Customize Enemy Stats
Use `Enemies` or `EnemiesNoSync` module with controls like `HealthMultiplier`, `AttackDamageMultiplier`, `Scale`, `Movement`, `Resistances`.
→ See [enemies.md](references/enemies.md)

### Change Enemy Projectiles
Use `Projectile` field in enemy descriptors to swap attacks.
→ See [projectiles.md](references/projectiles.md)

### Spawn Enemies from Other Enemies
Use `Spawner` submodule in enemy descriptors (e.g., stingtails that spawn swarmers).
→ See [enemies.md](references/enemies.md) under "Spawner"

### Add MEV/DEA/EEE Enemies
Add their descriptors to `EnemyPool` in `Pools`. Requires the respective mod installed.
→ See [mev-dea.md](references/mev-dea.md)

### Create Deep Dive Chains
Use `NextDifficulty` module to chain difficulties across stages.
→ See [modules.md](references/modules.md) under "NextDifficulty"

### Make Difficulty Pubbable (Non-CD2 Clients)
Use `EnemiesNoSync` instead of `Enemies`. Avoid features requiring replication (Scale, Materials).
→ See [enemies.md](references/enemies.md), [faq.md](references/faq.md)

## Enemies vs EnemiesNoSync

| Feature | `Enemies` | `EnemiesNoSync` |
|---------|-----------|-----------------|
| Client requirement | All need CD2 | Works with any client |
| `Scale` | Synced | Not synced |
| `Materials` | Synced | Not synced |
| Most other controls | Work | Work |

Use `EnemiesNoSync` for pubbable difficulties. See [Spy's pubbing guide](https://docs.google.com/document/d/1ShytNpPJF56XojjrTofA9DCkBXCzqBH2W-aFaLgbk30/) for details.

## Version History

- **CD2-v17** (Dec 2025): `Vars` module, `Alert` on wavespawners, `Select`/`LockFloat`/`LockBoolean`/`LockString` mutators
- **CD2-v16** (Nov 2025): `Messages`/`SoundCues` modules, `Countdown`/`Join`/`Int2String`/`Float2String` mutators
- **CD2-v15** (May 2025): `Diversity` in wavespawners, `Trigger` mutators, `Heal` advanced controls, `Outline`
- **CD2-v14** (Mar 2025): Dense Biozone, Movement descriptions
- **CD2-v13** (Mar 2025): Legacy pawn stats, `BySecondary`, `DwarfCount`, Darkness/Salvage modules
- **CD2-v12** (Feb 2025): `DefenseProgress`, `ByResuppliesCalled`, `Salvage` module, `BySalvagePhase`
- **CD2-v11** (Jan 2025): `Direct` control, `UsesBiomeVariants`, `BySaboPhase`
- **CD2-v10** (Dec 2024): Projectiles, MEV/DEA support, elite/veteran system, `Spawner` control

## External Resources

- [Practical DRG Discord](https://discord.gg/pdrg) - CD2 distribution and community
- [Vanilla Descriptors & Hazard 5 Defaults](https://gist.github.com/trumank/5913a58e7f0f38fbc0b2d9e5cf5f51d7)
- [DRG Hazard Scaling Spreadsheet](https://docs.google.com/spreadsheets/u/0/d/15L6sCaM5WdfuI65X54qDhD5sRDCGpb1Q4fkVkRhbBU4/htmlview)
- [CD1 Guide (DifficultySetting fields)](https://docs.google.com/document/d/131FqOl0FnwiAslvvDSYkV35oBQXYx2kH0oZYwEpjoBI/)
- [Spawn Mechanics Deep Dive](https://docs.google.com/document/d/1g13t4J77OL-R5R72WK9vxErqGPINazwweAvTdi9aOVQ/)
