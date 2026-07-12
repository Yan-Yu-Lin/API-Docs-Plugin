### Increase or decrease the number of enemies
If you enjoy a certain difficulty file but you think the number of enemies is either too small or too big, you can modify it to your taste with a very simple edit: look for the `EnemyCountModifier` (ECM) field inside `DifficultySettings`. The ECM works as a **global multiplier** for all spawn events in the difficulty, so you just need to increase it or decrease it however you like. As an example, the following snippet is from Hazard 6x2:

```json 
...,
"DifficultySetting": {
        "EnemyCountModifier": [
            2,
            2.1,
            2.7,
            3.3
        ]
}
...,
```
so if we wanted to create Hazard 6x4 we would double these values:
```json 
...,
"DifficultySetting": {
        "EnemyCountModifier": [
            4,
            4.2,
            5.4,
            6.6
        ]
}
...,
```
Depending on how many enemies you want to get you might have to edit also the `MaxActiveEnemies` cap in `Caps`:
```json 
...,
"Caps": {
        "MaxActiveCritters": 40,
        "MaxActiveSwarmers": [
            60,
            120,
            180,
            180
        ],
        "MaxActiveEnemies": [
            100,
            120,
            180,
            180
        ]
    }
...,
```
When the number of enemies in a mission goes above `MaxActiveEnemies` the game will despawn some of them, although this behaviour is not completely understood. Take into account that increasing the enemy cap will negatively affect the frame rate and going above 300 is not recommended.

### Removing vanilla enemies from a difficulty
Are you a solo player that hates stingtails or stalkers? Or maybe you want to remove younglings from Salt Pits? This is one of the most common edits and it's really easy to do. You will need two things:

1. Know the in-game name of the enemy you want to remove (the descriptor's name)
2. Know the vanilla pool the enemy is in by default

For the first, check the table in [Resources](resources.md). As an example, if you wanted to remove stalkers the name you'd need is `ED_Spider_Stalker`. For the second, locate your enemy in the following (slightly incomplete) table:

| Pool | Pools module field | Enemies |
| ---- | ------  | ------ |
| Common Pool | CommonEnemies | Grunts, Praetorians |
| Disruptor Pool | DisruptiveEnemies | Menaces, Wardens, Bulk Detonators, Stingtails, Shellbacks, Grabbers, Goo Bombers, Stalkers |
| Special Pool | SpecialEnemies | Swarmers, Exploders, Web Spitters, Acid Spitters, Septic Spreaders, Mactera Spawns and Trijaws |
| Stationary Pool | StationaryPool | Breeders, Swarmer Nexii, Spitballers, Cave Leech, Barragers, Vartok Scalebramble |

Once you know the original pool where your enemy is, just remove it. For example, removing stalkers and septics from a difficulty:

```json
...,
"Pools": {
    "DisruptiveEnemies": {
        "Remove": ["ED_Spider_Stalker"]
    },
    "SpecialEnemies": {
        "Remove": ["ED_Spider_Lobber"]
    }
}
...,
```







