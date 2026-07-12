# Wave Spawners

Wave spawners are a feature of CD2 that allow the creation of unnanounced enemy waves with various degrees of flexibility. The following basic example spawns a wave of difficulty 100 composed of only grunts every 90 seconds in 3 locations around the player:

```json
{
    "WaveSpawners": 
        {
          "Enabled": true,
          "Interval": 90,
          "Enemies": ["ED_Spider_Grunt"],
          "Difficulty": 100,
          "Distance": 10,
          "Locations": 3
        }
}
```

The following table shows the valid fields inside a `WaveSpawner`:

| Field | Type | Description |
| -- |-- |--|
| Enabled| Bool | Whether the wave spawner is active (true) or not (false). |
| Name | String | A description. Doesn't have any effect. |
| Interval | Float | After the wave is enabled, a time of `Interval` seconds will pass until the first spawns appear unless `SpawnOnEnable` (see below) is true. After that the wave will repeat every `Interval` seconds unless disabled. |
| Enemies | [List] | A list of the enemy descriptors that will spawn. To spawn all available enemies in the pool, leave the field out. A blank field ("Enemies: []") will spawn zero enemies. |
| Difficulty | Float | Number of points assigned to the wave event, which will be distributed among the enemies in `Enemies` depending on their `DifficultyRating` to decide how many will spawn. |
| Distance | Float | Distance where the enemies will spawn relative to the player. |
| Diversity | Int | If the `Enemies` field is left empty, the spawner will use all enemies in the pool and the difficulty's diversity. This field allows to specify an independent diversity only for the wavespawner. |
| Locations | Int | Number of spawn points. |
| SpawnOnEnable | Bool | If true, the wave will start spawning enemies as soon as it is enabled, skipping the initial `Interval`. Defaults to False.|
| UnlockInterval | Bool | If true, changing the interval will modify the current timer. If false, the time to next spawn is selected once and locked to that time until rerolled (e.g. when enemies spawn). Defaults to False. |
| PauseOnDisable | Bool | If true, the timer for the next spawn is paused while the wavespawner is disabled and resumes when it is enabled. If false, the timer is reset when the spawner is re-enabled. Defaults to False. |
| Alert | Bool | If true, the enemies will spawn aggroed to the player. Defaults to True. |

All `WaveSpawner` fields can be mutated. The following snippet shows a popular spawner useful in Elimination missions, which spawns a bulk detonator with descriptor `ED_WeakBulk`, defined in the `Enemies` module, whenever there is a dreadnought on the map:

```json
{
    "WaveSpawners": [
        {
          "Name": "Bulk helper wave during dreads",
          "Enabled": {
            "Mutate": "IfFloat",
            "Value": {
              "Mutate": "EnemyCount",
              "ED": "XED_WeakBulk"
            },
            "<": 1,
            "Then": {
              "Mutate": "DuringDread"
            },
            "Else": false
          },
          "Interval": 10,
          "Enemies": ["XED_WeakBulk"],
          "Difficulty": 250,
          "Distance": 1750,
          "Locations": 1
        }
}
```

There are a special group of `Trigger` mutators that can be used to gain a lot of control on enabling and disabling the wavespawners based on game conditions: please see their docs at the bottom of the [mutator section](mutators.md/#trigger-mutators).

