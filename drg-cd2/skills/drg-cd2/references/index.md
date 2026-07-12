# Introduction

This website serves as a reference for Custom Difficulty 2, a mod for [Deep Rock Galactic](https://store.steampowered.com/app/548430/Deep_Rock_Galactic/) which allows the creation of new hazards, or difficulties. Developed by @TheBrain as a successor to the Custom Difficulty mod, CD2 features many improvements over the and possibilities offered to difficulty designers:

* Allows players to a have a much finer control over many aspects of the gameplay by introducing [mutators](mutators.md), control flow structures similar to those found in common programming languages. 
* Exposes many [enemy](enemies.md) controls to change their behaviour, spawning mechanics and even aspect by featuring custom materials replication to clients.
* Allows manipulating the enemy pools live during a mission based on gameplay conditions.
* Offers many features not available in CD1 such as controls for illumination, player scale, the amount of nitra in the map, etc.
* ... and many others.


## Main Sections

* [Basics](basics.md). The basics of CD2.
* [Modules](modules.md). A list of the top level modules for a valid CD2 file.
* [Enemies](enemies.md). Reference for the `Enemies` or `EnemiesNoSync` modules.
* [Direct](direct.md). A compilation of `Direct` enemy controls with default values.
* [Wave Spawners](wavespawners.md). Reference for the `WaveSpawners` module.
* [Projectiles](projectiles.md). Reference for the `Projectile` field of enemy descriptors.
* [Mutators](mutators.md). A list of currently supported mutators.
* [MEV, DEA and EEE](mev-dea.md). A reference for the MEV and DEA mods and links to the EEE reference, used to add new enemy variants into the game.
* [Common Edits](common_edits.md). Reference section for common difficulty edits.
* [Resources](resources.md). Useful links related to Custom Difficulty.

<figure markdown="span">
  ![CD2modhub](pictures/cd2-modhub.png)
  <figcaption>Main CD2 screen in Modhub.</figcaption>
</figure>

## Update Log

* 4-Dec-2024: Updated for CD2-v9: added `ByEscortPhase` and `ByRefineryPhase` mutators.
+ 25-Dec-2024: Updated for CD2-v10: added the [Projectiles](projectiles.md) page, added the [MEV and DEA](mev-dea.md) page, added an explanation for elite and veteran enemies in [Enemies](enemies.md), added the explanation for the new `Spawner` enemy control, and some minor corrections. 
+ 29-Jan-2025: Updated for CD2-v11: added the `Direct` and `UsesBiomeVariants` enemy controls and the `BySaboPhase` mutator.
+ 20-Feb-2025: Partial update for CD2-v12: added the `DefenseProgress` and `ByResuppliesCalled` mutators, added the `Salvage` module and the `BySalvagePhase` mutator.
+ 28-Feb-2025: Added @Carrot's projectile resource to the [Resources](resources.md) and [Projectiles](projectiles.md) tabs, added @Spy's guide to pubbing with CD2 to [Resources](resources.md) and to the FAQ, added EEE's reference to [Projectiles](projectiles.md) and to [MEV, DEA and EEE](mev-dea.md).
+ 11-Mar-2025: Update for CD2-v13: added the legacy pawn stats to [enemy controls](enemies.md), added BySecondary and DwarfCount mutators, added Darkness module descriptions, added Salvage.Minimules.NitraToGive to the Salvage module 
+ 22-Mar-2025: Update for CD2-v14: added the Dense Biozone option to the ByBiome mutator, added descriptions to Movement enemy module provided by @emctwo.
+ 25-May-2025: Update for CD2-v15: added the `Diversity` option to the [wavespawner](wavespawners.md) section, added the new `Trigger` mutators to the [mutators](mutators.md) section, added the `Heal` advanced controls and the new `Outline` control to [enemies](enemies.md).
+ 2-Jun-2025: Clarified the section about the differences between `Enemies` and `EnemiesNoSync` in [Enemies](enemies.md); removed the DEA enemy list from [MEV, DEA and EEE](mev-dea.md) and added a link to the mod in mod.io and to the official list.
+ 23-Jul-2025: Added the [Direct](direct.md) page.
+ 15-Aug-2025: Added the `Usable` table in the `Salvage` module in Modules and some examples.
+ 11-Nov-2025: Update for CD2-v16: added the `Countdown`, `EnemiesRecentlySpawned`, `Int2String`, `Float2String` and the `Join` mutators; added the `Messages` and `SoundCues` module; added the `FallDamageStartVelocity` and `FallDamageModifier` in the `Dwarves` module.
+ 2-Dec-2025: Update for CD2-v17: added the `Vars` module, the `Alert` field on wavespawners, the `DroppodDistance`, `MuleDroppodDistance`, `Nonzero`, `Select`, `EnemyHealth`, `EnemyDistance`, `SecondaryFinished`, `LockFLoat`, `LockBoolean` and `LockString` mutators.
+ 11-Dec-2025: Added the [Common Edits](common_edits.md) section, changed theme to material.
