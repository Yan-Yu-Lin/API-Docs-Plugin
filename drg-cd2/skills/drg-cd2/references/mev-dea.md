# MEV, DEA and EEE

MEV, DEA and EEE are three common mods that add enemies to the game. They are used in a few commonly played difficulties and although they are not directly related to CD2, it is handy to have a list of the new enemy descriptors they add. Some of the enemies they add can be replicated with CD2 without needing an external mod with the use of custom materials and [projectiles](projectiles.md); some enemies in these mods, however, have changes in their behaviour tree which are impossible to replicate with CD2 for now. 

+ MEV is not in mod.io and can be found as a .pak in the Pracical DRG discord. There is no official documentation for the MEV enemies, so this page contains the list below.
+ DEA is available in [mod.io](https://mod.io/g/drg/m/donnies-enemy-addon-cd2-version#description) together with a [document](https://docs.google.com/document/d/12pFMGVzQYR2vQzEhvCqaLcBBsOfjhkpxvEaIOJB8HHw/edit?tab=t.0) with the list of enemies it adds. 
+ A more recent mod is EEE, available in [mod.io](https://mod.io/g/drg/m/elytrasenemiesexpansion). You can see the list of EEE enemies [here](https://github.com/Elytras/ElytrasEnemiesExpansion/blob/main/EEE%20ReadMe.txt).

These enemy expansion mods don't do anything by themselves: in order to spawn the new enemies their descriptors have to be explicitly included in a CD2 file, so you can leave them enabled at all times while you are playing.

## MEV enemies

Descriptions provided by mod author @yinny. Updated for MEV 5.4.

### Grunt variants

These grunts are recolors of the normal grunt and its veterans (Guards and Slashers) to be used for special purposes (eg. to give grunts spawning from nexus a different color from normal grunts).

| ED name | Comments |
| -------- | -------- |
| ED_Spider_Grunt_cyan | Blue grunt. | 
| ED_Spider_Grunt_red | Red grunt. |  
| ED_Spider_Grunt_white | White grunt. | 
| ED_Spider_Grunt_yellow | Yellow grunt. |
| ED_Spider_Grunt_Guard_cyan | Blue guard. |
| ED_Spider_Grunt_Guard_red | Red guard. |
| ED_Spider_Grunt_Guard_white | White guard. |
| ED_Spider_Grunt_Guard_yellow | Yellow guard. |
| ED_Spider_Grunt_Attacker_cyan | Blue slasher. |
| ED_Spider_Grunt_Attacker_red | Red slasher. |
| ED_Spider_Grunt_Attacker_white | White slasher. | 
| ED_Spider_Grunt_Attacker_yellow | Yellow slasher. |

### Breeders 

These breeders are recolors of the normal breeder. Their main use is to be able to have multiple breeders spawning different enemies in the same mission, which before CD2 was only partially possible by using the rockpox breeder as a second variant. As an alternative way, CD2 now allows to have multiple breeder descriptors with different settings (see the `Breeder` module in [Enemies](enemies.md).)

| ED name | Comments |
| --------- | ------- |
| ED_JellyBreeder_green | Green breeder, spawns ED_Jelly_Spawn_dummy_green. |
| ED_JellyBreeder_red | Red breeder, spawns ED_Jelly_Spawn_dummy_red. |
| ED_JellyBreeder_purple | Purple breeder, spawns ED_Jelly_Spawn_dummy_purple. |
| ED_JellyBreeder_yellow | Yellow breeder, spawns ED_Jelly_Spawn_dummy_yellow. |

To use these, override the specified dummy jelly descriptor with the ED you want to spawn:

```json
"ED_Jelly_Spawn_dummy_purple": {
    "Base": "ED_Spider_Exploder"
}
```

will make the purple breeder spawn exploders.

### Bulks


| ED name | Comments |
| --------- | ------- |
| ED_Spider_ExploderTank_black | A bulk recolor in black. |
| ED_Spider_ExploderTank_white | A bulk recolor in white. |
| ED_Spider_ExploderTank_small | A small bulk, commonly called mini-bulk, with a smaller radius explosion. |
| ED_Spider_ExploderTank_big | A bigger bulk which also has a huge explosion with magma lining. |
| ED_Spider_ExploderTank_frozen | An ice bulk, does no damage but freezes everything around it. |
| ED_Spider_Plantonator | A special bulk. When exploding, each bomblet will spawn ED_sprout_spawn in turn, which is a korlok sprout by default but can be changed by specifying a different base. |

### Exploders

| ED name | Comments |
| --------- | ------- |
| ED_Spider_Exploder_frost | An ice exploder, leaves snow when it explodes. |
| ED_Spider_Exploder_fungus | A fungus bogs themed exploder, leaves goo behind when it dies. |
| ED_Spider_Exploder_white | A recolor in white. |

### Mactera

| ED name | Comments |
| --------- | ------- |
| ED_Mactera_Shooter_HeavyVeteran_cyan | Elemental electric brundle. |
| ED_Mactera_Shooter_HeavyVeteran_green | Elemental poison brundle. |
| ED_Mactera_Shooter_HeavyVeteran_red | Elemental fire brundle. |
| ED_Mactera_Shooter_HeavyVeteran_white | Elemental ice brundle. |
| ED_Mactera_Shooter_cyan | Elemental electric mactera spawn. |
| ED_Mactera_Shooter_green | Elemental green mactera spawn. |
| ED_Mactera_Shooter_red | Elemental fire mactera spawn. |
| ED_Mactera_Shooter_white | Elemental ice mactera spawn. |
| ED_Mactera_TripleShooter_cyan | Elemental electric trijaw. |
| ED_Mactera_TripleShooter_green | Elemental poison trijaw. |
| ED_Mactera_TripleShooter_red | Elemental fire trijaw. |
| ED_Mactera_TripleShooter_white | Elemental ice trijaw. |
| ED_Bomber_buffer | A goo bomber warden, gives the protection effect to nearby enemies. |

### Menaces

| ED name | Comments |
| --------- | ------- |
| ED_Spider_RapidShooter_cyan | Elemental electric menace. |
| ED_Spider_RapidShooter_green | Elemental poison menace. |
| ED_Spider_RapidShooter_red | Elemental fire menace. |
| ED_Spider_RapidShooter_white | Elemental ice menace. |
| ED_Spider_RapidShooter_Turbo | A rapid-fire shooting menace. |

### Nexus

These are recolors of the normal nexus, following the same logic for breeders: they allow to have more than one type of nexus in the same mission. CD2 currently doesn't have a `Nexus` module to specify the EDs of different nexii (although the effect can be simulated by using `Spawner`, see in [enemies](enemies.md)), so this method is still the simplest. 

| ED name | Comments |
| ----- | --------- |
| ED_SpiderSpawner_green | Green nexus spawning ED_Spider_Spawn_dummy_green. |
| ED_SpiderSpawner_red | Red nexus spawning ED_Spider_Spawn_dummy_red. |
| ED_SpiderSpawner_yellow | Yellow nexus spawning ED_Spider_Spawn_dummy_yellow. |
| ED_SpiderSpawner_white | White nexus spawning ED_Spider_Spawn_dummy_white. |

### Nukeballers

Spitballers shooting nukes. Since they provide a different number of shot projectiles, they are an interesting match for custom [projectiles](projectiles.md).

| ED name | Comments |
| ----- | --------- |
| ED_ShootingPlant_NukeSingle | Shoots a single projectile. |
| ED_ShootingPlant_Nuke | Shoots three projectiles in a row. |
| ED_ShootingPlant_NukeEX | Shoots five projectiles in a row. |
| ED_ShootingPlant_NukeU | Shoots ten projectiles in a row. |

### Oppressors

Recolors (not elemental) of the oppressor.

| ED name | Comments |
| ----- | --------- |
| ED_Spider_ShieldTank_cyan | Blue oppressor. |
| ED_Spider_ShieldTank_red |  Red oppressor. |
| ED_Spider_ShieldTank_yellow |  Yellow oppressor. |
| ED_Spider_ShieldTank_white |  White oppressor. |

### Praetorians 

| ED name | Comments |
| ----- | --------- |
| ED_Spider_Tank_buffer | Praetorian warden, gives the protection buff and a healing buff to nearby enemies. |
| ED_Spider_Tank_cyan | Elemental electric praetorian variant. |
| ED_Spider_Tank_red | Elemental fire praetorian variant. |

### Shellbacks 

| ED name | Comments |
| ----- | --------- |
| ED_Woodlouse_cyan | Elemental electric shellback. |
| ED_Woodlouse_red | Elemental fire shellback. |
| ED_Woodlouse_purple | Purple shellback recolor. |
| ED_Woodlouse_white | Elemental ice shellback. |

### Sprouts
Can be used as new stationary enemies. 

| ED name | Comments |
| ----- | --------- |
| ED_Sprout_Normal | Vanilla korlok sprout. |
| ED_Sprout_purple | A korlok sprout that shoots the web spitter projectile. |
| ED_Sprout_upside | Vanilla korlok sprout that spawns on ceilings. |

### Swarmers

| ED name | Comments |
| ----- | --------- |
| ED_Spider_Tank_HeavySpawn_swarmer | Swarmer-scale sentinel. |
| ED_Spider_Stalker_swarmer | Swarmer-scale stalker. |

### Younglings

| ED name | Comments |
| ----- | --------- |
| ED_Woodlouse_Youngling_cyan | Blue youngling recolor. |
| ED_Woodlouse_Youngling_red | Red youngling recolor. |

### Miscellaneous enemies

| ED name | Comments |
| ----- | --------- |
| ED_Lootbug_bulk | Mimic lootbug. Can't be pet and when killed it explodes like a bulk detonator. |
| ED_CaveLeech_cloak | A leech with the stalker material. |
| ED_CaveLeech_silent | A silent leech. |
| ED_PatrolBot_missile | A special patrol bot with a different attack pattern. |
| ED_PatrolBot_rocketbeam | A special patrol bot with a different attack pattern. |

