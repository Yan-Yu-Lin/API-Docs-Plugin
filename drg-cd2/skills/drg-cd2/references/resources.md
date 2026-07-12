# Resources

## Useful links

* [A Quick and Dirty Guide to Custom Difficulty for Deep Rock Galactic](https://docs.google.com/document/d/131FqOl0FnwiAslvvDSYkV35oBQXYx2kH0oZYwEpjoBI/edit?tab=t.0), a CD1 guide explaining most of the fields inside CD2's `DifficultySettings`.
* [Vanilla descriptors](https://gist.github.com/trumank/5913a58e7f0f38fbc0b2d9e5cf5f51d7) and default values for Hazard 5.
* [Materials Guide](media/Materials-1.pdf) by @TheBrain on how to test new enemy materials in Sandbox Utilities.
* [Vanilla projectiles compilation](https://docs.google.com/spreadsheets/d/10NqPL5Z1zkU6hn4XMbxtirZBM9rf6nrCNKI3HSv6FtE/edit?gid=0#gid=0) by @Carrot, categorizing the vanilla projectiles by category, type and damage. 
* [On Pubbing With CD2](https://docs.google.com/document/d/1ShytNpPJF56XojjrTofA9DCkBXCzqBH2W-aFaLgbk30/edit?tab=t.0#heading=h.ithv7n4jcboa) a guide by @Spy detailing which parts of CD2 are safe to be used when designing difficulties made for pubbing (so clients are not expected to have CD2).
* [DRG Hazard Scaling](https://docs.google.com/spreadsheets/u/0/d/15L6sCaM5WdfuI65X54qDhD5sRDCGpb1Q4fkVkRhbBU4/htmlview) file, for the values of the fields in `DifficultySetting` for the vanilla Hazards and some others. 
* [Grouped cooldowns tutorial](https://markdownpastebin.com/?id=2044a6586b4d4735a0fe150325ee9285) by @theBrain.
* [On Deep Rock Galactic Spawn Mechanics](https://docs.google.com/document/d/1g13t4J77OL-R5R72WK9vxErqGPINazwweAvTdi9aOVQ/edit?tab=t.0), a guide that goes into more detail about the pool system and how the spawn points system works.

## Enemy Descriptors

Original list [here](https://github.com/trumank/drg-custom-difficulties/blob/master/DATA.md), updated here for S5.

| Descriptor | In-game name |
| ---------- |--------------| 
| ED_Barrage_Infector | Barrage Infector |
| ED_Bomber_Explosive| 	Mactera Fire Bomber|
| ED_Bomber_Ice| 	Mactera Frost Bomber|
| ED_Bomber_Rockpox_Plague| 	Rockpox infected Mactera Goo Bomber|
| ED_Bomber| 	Mactera Goo Bomber|
| ED_Butterfly| 	Hexawing Gniffer|
| ED_CaveLeech| 	Cave Leech|
| ED_Crawler | Crawler |
| ED_EggSpider| 	Glyphid Swarmer from breakable eggs|
| ED_FacilityTurret_Barrier| 	Repulsion Turret|
| ED_FacilityTurret_Burst| 	Burst Turret|
| ED_FacilityTurret_Sniper| 	Sniper Turret|
| ED_Flea| 	Fester Flea|
| ED_FlyingSmartRock| 	Flying Rocks from phase 2/3 of the Ommoran Heartstone (do not attack the player and will remain stationary if not on an escort mission)|
| ED_Grabber| 	Mactera Grabber|
| ED_GreatEggHunt_SpringBunny| 	Spring Bunny|
| ED_HydraWeed| 	Korlok Tyrant Weed|
| ED_InfectedMule| 	BET-C (Cannot be activated or trigger a fight)|
| ED_InfestationLarva| 	Parasite|
| ED_InsectSwarm_Spawner| 	Broken|
| ED_JellyBreeder_RockpoxPlague| 	Rockpox infected Naedocyte Breeder|
| ED_JellyBreeder| 	Naedocyte Breeder|
| ED_Jelly_Spawn| 	Naedocyte swarmer from Breeder|
| ED_Jelly_Swarmer| 	Naedocyte swarmer|
| ED_Mactera_Shooter_Amber| 	Kursite Mactera Spawn|
| ED_Mactera_Shooter_HeavyVeteran| 	Mactera Brundle|
| ED_Mactera_Shooter_Normal| 	Mactera Spawn|
| ED_Mactera_TripleShooter| 	Mactera Tri-Jaw|
| ED_Nisse| 	Yuletide Elf|
| ED_PatrolBot_Caretaker| 	Patrol bots spawned by Caretaker (cannot be hacked)|
| ED_PatrolBot| 	Patrol Bot|
| ED_PlagueLarva| 	Rockpox Larva|
| ED_Prospector| 	Prospector|
| ED_PumpkinLootBug| 	Lootbug|
| ED_Shark| 	Nyaka Trawler|
| ED_ShootingPlant| 	Spitball Infector|
| ED_Shredder| 	Rival Shredder|
| ED_SpiderSpawner| 	Brood Nexus|
| ED_Spider_Alarm| 	Unused enemy that spawns a swarm if it is not killed before burrowing|
| ED_Spider_Amber_Shooter| 	Kursite Acid Spitter|
| ED_Spider_Boss_Heavy| 	Dreadnaught Hiveguard|
| ED_Spider_Boss_TwinA| 	Dreadnaught Arbelist|
| ED_Spider_Boss_TwinB| 	Dreadnaught Hiveguard|
| ED_Spider_Buffer| 	Glyphid Warden|
| ED_Spider_Charger| 	Melee only Glyphid Praetorian|
| ED_Spider_ExploderTankGhost| 	Ghost from haunted cave warning|
| ED_Spider_ExploderTank_King| 	Crassus Detonator|
| ED_Spider_ExploderTank| 	Bulk Detonator|
| ED_Spider_Exploder_Rockpox_Plague| 	Rockpox infected Glyphid Exploder|
| ED_Spider_Exploder_Warning| 	Glyphid Exploder|
| ED_Spider_Exploder| 	Glyphid Exploder|
| ED_Spider_GruntTutorial| 	Tutorial Difficulty Grunt|
| ED_Spider_Grunt_Attacker| 	Grunt Slasher|
| ED_Spider_Grunt_Guard| 	Grunt Guard|
| ED_Spider_Grunt_Ice| 	Glacial Grunt variant|
| ED_Spider_Grunt_Mutated| 	Radioactive Exclusion Zone override for the Glyphid Grunt|
| ED_Spider_Grunt_RockpoxPlague| 	Rockpox infected grunt|
| ED_Spider_Grunt_Rock| 	Ebonite Glyphid Grunt|
| ED_Spider_Grunt| 	Base grunt (including veteran grunts)|
| ED_Spider_Hoarder| 	Huuli Hoarder|
| ED_Spider_Lobber| 	Glyphid Septic Spreader|
| ED_Spider_RapidShooter| 	Menace|
| ED_Spider_ShieldTank| 	Oppressor|
| ED_Spider_ShooterQueen| 	Acid Spitter Queen (will more than likely crash your game)|
| ED_Spider_Shooter_Ground| 	Unused Acid Spitter that shoots acid in an arc|
| ED_Spider_Shooter_Rockpox_Plague| 	Rockpox infected Acid Spitter|
| ED_Spider_Shooter| 	Acid Spitter|
| ED_Spider_Spawn| 	Glyphid Spawns (from Brood Nexus)|
| ED_Spider_Spitter| 	Web Spitter|
| ED_Spider_Stalker| Stalker |
| ED_Spider_Stinger| 	Glyphid Stingtail|
| ED_Spider_Swarmer_Ice| 	Ice Glyphid Swarmer|
| ED_Spider_Swarmer_Mutated| 	Radioactive Exclusion Zone override for the Glyphid Swarmer|
| ED_Spider_Swarmer_Pheromone_NOFX| 	Glyphid Dreadnaught Pheromone Swarmer|
| ED_Spider_Swarmer| 	Glyphid Swarmer|
| ED_Spider_Tank_Amber| 	Kursite Glyphid Praetorian|
| ED_Spider_Tank_Boss| 	Glyphid Dreadnaught|
| ED_Spider_Tank_HeavySpawn| 	Hiveguard Sentinel|
| ED_Spider_Tank_Ice| 	Glacial Praetorian|
| ED_Spider_Tank_Mutated| 	Radioactive Exclusion Zone override for the Glyphid Praetorian|
| ED_Spider_Tank_RockpoxPlague| 	Rockpox infected Glyphid Praetorian|
| ED_Spider_Tank_Rock| 	Ebonite Glyphid Praetorian|
| ED_Spider_Tank| 	Praetorian|
| ED_TentaclePlant | Vartok Scalebramble |
| ED_Terminator| 	Rival Nemesis|
| ED_TunnelSwarmer| 	Swarmers spawned by triggering a Glyphid Tunnel|
| ED_WalkingPlagueheart| 	Rockpox Corruptor|
| ED_Woodlouse_Youngling| 	Q'ronar Youngling|
| ED_Woodlouse| 	Q'ronar Shellback|
