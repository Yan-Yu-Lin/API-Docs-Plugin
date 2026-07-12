# Mutators

Here follows an alphabetized list of mutators for CD2.

## Accumulate
`Accumulate` can track changes in other mutators by adding to a starting `Initial` number. In addition, it also supports clamping the accumulated value with `Min` and `Max`. If used with a constant value, it can be used to make a simple counter.

Example: the value of the following snippet starts at 0 and would cap at 10 after roughly 10 seconds.

```json
{
    "Mutate": "Accumulate",
    "Initial": 0,
    "Value": 1,
    "Min": 0,
    "Max": 10
}
```


## Add, Subtract, Multiply, Divide, Pow, Modulo, Round, Ceil, Floor
Arithmetic mutators that can be used for basic mathematical operations.

Example: enemy speed as a linear function of resupplies called during the mission.

```json
"SpeedModifier": {
      "Mutate": "Add",
      "A": 1.35,
      "B": {
        "Mutate": "Multiply",
        "A": {
          "Mutate": "ResuppliesCalled"
        },
        "B": 0.1
      }
    }
```

## And, Or, Not 
Basic boolean operators.

## ByBiome
Change the value based on the mission biome. If a value isn't set for a biome it will use the 'Default' value. A 'Default' must be set unless a value is specified for biomes. If a biome is not recognized and no default is specified, the value for CrystallineCaverns will be used.

| Official name | Alias 1 | Alias 2 |
| ------------- |-------|------------|
| BIOME_AzureWeald | AzureWeald |
| BIOME_CrystalCaves | CrystalCaves | CrystallineCaverns |
| BIOME_DenseBiozone | DenseBiozone | Biozone |
| BIOME_FungusBogs | FungusBogs |
| BIOME_HollowBough | HollowBough |
| BIOME_IceCaves | IceCaves | GlacialStrata |
| BIOME_MagmaCaves | MagmaCaves | MagmaCore |
| BIOME_RadioactiveZone | RadioactiveExclusionZone | REZ |
| BIOME_SaltCaves | SaltCaves | SaltPits |
| BIOME_SandblastedCorridors | SandblastedCorridors | Sandblasted |

## ByDDStage
Change the value based on the Deep Dive stage. If a value isn't set for a stage, it will use the 'Default' value. A 'Default' must be set.

Example: 

```json
{
    "Mutate": "ByDDStage",
    "Default": 1.2,
    "Stage1": 1.0,
    "Stage2": 1.2,
    "Stage3": 1.45
 }
```
## ByDNA
Allows setting a value based on a combination of Mission Type, Length, and Complexity:
``` json
{
  "Mutate": "ByDNA",
  "Default": 1,
  "Mining": 2,
  "Refinery": 3,
  "Refinery,x,2": 5,
  "Refinery,2": 4,
  "x,x,2": 8
}
```
The condition with the most matches will be prioritized. Mission type is prioritized over length and length over complexity. An “x” matches anything. In the above a (2,2) refinery would have the value 4.

## ByEscortPhase

Used to detect the different stages of an Escort mission:

```json
{
  "Mutate": "ByEscortPhase",
  "Default": 0,
  "InGarage": 0.1,
  "Stationary": 2,
  "Moving": 30,
  "WaitingForFuel": 400,
  "FinalEventA": 5,
  "FinalEventB": 0.6,
  "FinalEventC": 70,
  "FinalEventD": 8,
  "Finished": 900
}
```

## ByMissionType
Change the value based on mission type. If a value isn't set for a mission type it will use the 'Default' value. A 'Default' must be set unless a value is specified for all mission types.
Supported mission types:

* DeepScan
* Egg
* Elimination
* Escort
* Mining
* PE 
* Refinery
* Sabotage
* Salvage

Example: 

```json
{
    "Mutate": "ByMissionType",
    "Default": 60,
    "Egg": 70,
    "PE": 80
 }
```

## BySecondary
Can be used to detect secondary objectives both on normal missions and on deep dives. The objectives have the following names:

| Name |
| ----- |
| OBJ_2nd_Mine_Dystrum|
|OBJ_2nd_Mine_Hollomite|
|OBJ_2nd_KillFleas|
|OBJ_2nd_Find_Gunkseed|
|OBJ_2nd_Find_Fossil|
|OBJ_2nd_Find_Ebonut|
|OBJ_2nd_Find_BooloCap|
|OBJ_2nd_Find_ApocaBloom|
|OBJ_2nd_DestroyEggs|
|OBJ_2nd_DestroyBhaBarnacles|
|OBJ_DD_RepairMinimules|
|OBJ_DD_Defense|
|OBJ_DD_DeepScan|
|OBJ_DD_Morkite|
|OBJ_DD_Elimination_Eggs|
|OBJ_DD_AlienEggs|
|OBJ_DD_MorkiteWell|

Example: change the Nitra multiplier depending on the secondary objective in deep dives (20 % more nitra on dreadnought and black box objectives).

```json 
{
    "NitraMultiplier": {
        "Mutate": "BySecondary",
        "OBJ_DD_Elimination_Eggs": 1.2,
        "OBJ_DD_Defense": 1.2 
    }
}
```

## ByTime 
Change a value over time. Time matches the mission clock in the escape menu in-game, including starting before players receive control of their dwarves.
The value is determined by `InitialValue + RateOfChange * Max(0, Time - StartDelay)`.

Parameters:

* `InitialValue` - Value at time 0 and up until StartDelay
* `StartDelay` - Time in seconds to stay at the InitialValue before changing.
* `RateOfChange` - Rate per second to change the value.

Example: 

```json
{
    "Mutate": "ByTime",
    "InitialValue": 3.1,
    "RateOfChange": 0.0033,
    "StartDelay": 400
}
```

## ByPlayerCount
Change the value based on the number of players in-game. A solo game gets the first position in the list; two players get the second spot and so on. The last value in the list is used if there are more players than there are values in the list.

Example:

```json
{
    "Mutate": "ByPlayerCount",
    "Values": [
        80,
        120,
        180,
        180
    ]
}
```


## ByRefineryPhase

Used to detect the different stages of a Refinery mission.

```json
 {
  "Mutate": "ByRefineryPhase",
  "Default": 0,
  "Landing": 1,
  "ConnectingPipes": 2,
  "PipesConnected": 3,
  "Refining": 4,
  "RefiningStalled": 5,
  "RefiningComplete": 6,
  "RocketLaunched": 7
}
```

## ByResuppliesCalled

Allows specifying an array with indexes 0, 1, 2, etc, where the values at each index become valid when the number of resupplies corresponding to said index have been called.
The most typical use is specifying a varying number of resupply costs. For example:

```json 
{
    "Resupply": {
        "Cost": {
            "Mutate": "ByResuppliesCalled",
            "Values": [40, 50, 60]
        }
    }
}
```

will set up the first resupply to be 40 nitra, the second to be 50 nitra and 60 for all subsequent supplies.

## BySaboPhase

Used to detect the different stages of a Sabotage mission.

```json 
{
  "Mutate": "BySaboPhase",
  "Default": "Default Value",
  "Hacking": "Hacking Value",
  "BetweenHacks": "BetweenHacks Value",
  "HackingFinished": "HackingFinished Value",
  "Phase1Vent": "Phase1VentValue",
  "Phase1Eye": "Value for Phase1Eye",
  "Phase2Vent": "Value for Phase2Vent",
  "Phase2Eye": "Value for Phase2Eye",
  "Phase3Vent": "Phase3Vent Value",
  "Phase3Eye": "Value to use during Phase3Eye",
  "Finished": "Value for Finished"
}
```

## BySalvagePhase

Used to detect the different stages of a Salvage mission. The mutator uses the `Default` value for any mission that is not Salvage. 

```json 
{
      "Mutate":    "BySalvagePhase",
      "Default":   "Default Value",
      "Mules":     "Value until all mules repaired",
      "PreUplink": "Value while mules finished but uplink not started",
      "Uplink":    "Value during the uplink event",
      "PreRefuel": "Value between defense events",
      "Refuel":    "Value during the refuel event",
      "Finished":  "Value for the remainder of the mission"
}
```

## Clamp
Constrain a float (number) to fall within a range. This range is inclusive. If only a min or only a max is specified, the value will only be clamped in that direction.
 
Example:

```json
{
    "Mutate": "Clamp",
    "Value": 90,
    "Min": 0,
    "Max": 100
}
```

## Countdown 

A mutator that will count down from `Start` to `Stop`. It is usually used together with the `Int2String` mutator and the messages module to print messages on chat. It also has a `Default` value which is used when the countdown is not enabled. A boolean, mutable `Enable` field starts the countdown:

```json
"Messages": [
    {
      "SendOnChange": true,
      "Type": "Developer",
      "Sender": "My Difficulty",
      "Message": {
        "Mutate": "Join",
        "Values": [
          "Something in...",
          {
            "Mutate": "Int2String",
            "Value": {
              "Mutate": "Countdown",
              "Start": 16,
              "Enable": true
            }
          }
        ]
      }
    }
]
```

<figure markdown="span">
  ![CountdownMutator](pictures/countdown-mutator.png)
  <figcaption>Chat output resulting from the snippet above.</figcaption>
</figure>

If you want to trigger an event after a certain amount of time after something happens consider using the `TriggerDelay` and the trigger mutators instead of `Countdown`, at the bottom of the page. 

## DefenseProgress

This mutator tracks the progress of a defense event such as a black box, refuel or uplink. It returns a float between [0, 1] starting at 0.3.


## Delta
`Delta` can be used to detect a change in some other variable or mutator, and it is often used with `Accumulate`.

Example:
The following snippet will become momentarily true when a player receives health or shield damage.

```json
{
    "Mutate": "IfFloat",
    "Value": {
      "Mutate": "Delta",
      "Value": {
        "Mutate": "Add",
        "A": {
          "Mutate": "DwarvesHealth"
        },
        "B": {
          "Mutate": "DwarvesShield"
        }
      }
    },
    "<": 0,
    "Then": true,
    "Else": false
}
```

## DepositedResource
Count of a resource that has been deposited into the team depository. Any resource can be referenced by the name as it appears in the in-game UI.
 
Example:

```json
{
    "Mutate": "DepositedResource",
    "Resource": "Nitra"
}
```
## DescriptorExists
This is a boolean value which reflects whether an enemy descriptor is available. This is intended to allow a difficulty to fall back to a different descriptor if the desired descriptor isn't available, e.g. if MEV is not available.
Example:

```json
{
  "Mutate": "If",
  "Condition": {
    "Mutate": "DescriptorExists",
    "ED": "ED_MEV_Enemy"
  },
  "Then": ["ED_MEV_Enemy"],
  "Else": ["ED_Backup"]
}
```
## DrillerCount
Number of drillers in the lobby.

## DroppodDistance
Returns an average of the distance in cm between players and drop pod during mission extraction. It accepts the following fields:

+ `Default`: the default value to return when there is no drop pod.
+ `IncludeDowned`: a boolean which indicates whether to include dead dwarves in the average.

See also: `MuleDroppodDistance` mutator.

## DuringDefend
Becomes true when a black box, uplink or cell refuel is active.
## DuringDread
Becomes true whenever there is one of the following descriptors active on the map: `ED_Spider_Boss_Heavy` (Hiveguard), `ED_Spider_Boss_TwinA` (Arbalest), `ED_Spider_Boss_TwinB` (Lacerator) and `ED_Spider_Tank_Boss` (classic Dreadnought). 
## DuringDrillevator
Becomes true during the elevator phase in a Deep Scan mission. 
## DuringEggAmbush
Returns True during a non-announced wave after pulling an egg in Egg Hunts. As an example of use, the following snippet increases the `EnemyCountModifier` only during Egg waves, to make them more challenging. The `StartingAt` and `StoppingAfter` tries to make the increase affect only the current egg wave. 

```json 
{
"DifficultySetting":
    {
    "EnemyCountModifier": {
          "Mutate": "Multiply",
          "A": {
            "Mutate": "ByPlayerCount",
            "Values": [
              1.84,
              2,
              2.32,
              2.8
            ]
          },
          "B": {
              "Mutate": "If",
              "Condition": {
                "Mutate": "DuringEggAmbush",
                "StartingAt": 5,
                "StoppingAfter": 10
              },
              "Then": 4,
              "Else": 1
            }
        }
    }
} 

```


## DuringEncounters
Becomes true when Encounters are being placed in the map, that is, during mission generation. One of its uses it to change descriptor properties depending on whether they are part of an encounter or not:

```json 
{
    "Enemies": {
        "ED_Spider_Exploder": {
             "Base": "ED_Spider_Exploder",
             "CanBeUsedForConstantPressure": true,
             "CanBeUsedInEncounters": true,
             "DifficultyRating": 10,
             "Rarity": {
               "Mutate": "If",
               "Condition": {
                 "Mutate": "DuringEncounters"
               },
               "Then": 0.1,
               "Else": 5.5
             }
        }
    }
}
```

The snippet will force exploders in almost all encounters by giving them a very low rarity during those.
Clearing the `EnemyPool` when `DuringEncounters` is true will remove encounters from the mission.

## DuringExtraction
Becomes true during the extraction phase of the mission, ie, when going back to the drop pod.
## DuringGenericSwarm
Becomes true during a swarm announced by Mission Control. 
## DuringMission
This is true during a mission, or true during a specific window of time during a mission if times are specified. If specified, StartingAt determines the elapsed mission time in seconds when this becomes true. If specified, StoppingAfter determines the elapsed mission time in seconds after which this is false.
 
Example:
Only add stalkers and elite guards to the pool after 240 seconds have elapsed in the mission.

```json
"EnemyPool"{
    "add" {
        "Mutate": "If", 
        "Condition": {"Mutate": "DuringMission", "StartingAt": 240},
        "Then": ["ED_Spider_Stalker", "ED_Spider_Grunt_Guard_Elite"],
        "Else": []
    }
}
```

## DuringPECountdown
Returns True during the extraction phase of a PE mission. 

## DwarfCount 
Returns the number of players in the mission. 

## DwarvesAmmo
Average percent ammo left for the team, 1 when all teammates have 100% of their ammo and 0 when all teammates are at 0% ammo. This works the same way as the 4 bars under the dwarves names in the UI.

## DwarvesDown
Float count of the dwarves that are currently down, 0 if no dwarves are currently downed, 4 if all 4 dwarves are down.

## DwarvesDownTime
Time in seconds that has elapsed while a dwarf has been down. If multiple dwarves are down, it's the longest time down among the downed dwarves.

## DwarvesDowns
Total number of downs for the team during the mission. This might not match the end screen because it will still count downs from disconnected players, and will not over-count downs.

## DwarvesHealth
Average health, 1 when all teammates are at 100% health and 0 when all teammates are down.

## DwarvesRevives
Total number of revives for the team during the mission. This includes IW self-revives.

## DwarvesShield
Average shields, 1 when all teammates are at full shield 0 when all teammates are at 0 shield. Untested on shield disruption.
## ElapsedExtraction
Returns the elapsed time in the extraction phase of a mission.

## EnemiesKilled
Count number of Enemies that have died this mission. Optionally, this can get the deaths of a specific enemy descriptor.
Despawned enemies because of caps are likely counted. If your difficulty despawns significant amounts of enemies, this number might not match expectations.

Examples:

Count of all enemy kills:

```json
{
    "Mutate": "EnemiesKilled"
}
```

Count of enemies that have died with a specific descriptor:

```json
{
    "Mutate": "EnemiesKilled",
    "ED": "ED_Spider_Grunt"
}
```

Since CD2 v15, it is possible to specify a list of ED's and avoid having to nest addition mutators:

```json
{
    {
      "Mutate": "EnemiesKilled",
      "EDs": [ "A", "B", "C" ]
    }
},
```

## EnemiesRecentlySpawned

This mutator tracks enemies that spawned in the last `Seconds` seconds. You can track a single enemy descriptor with `ED` or multiple descriptors with `EDs`: in the last case, the mutator will return the sum of all spawned enemies that match the descriptors. If empty, the mutator will track all enemies. 

Example: returns how many enemies spawned in the last 60 seconds.

```json 
{  
    "Mutate": "EnemiesRecentlySpawned",  
    "Seconds": 60  
}
```

Example: return how many exploders spawned in the last 60 seconds.

```json 
{  
    "Mutate": "EnemiesRecentlySpawned",  
    "Seconds": 60,
    "ED": "ED_Spider_Exploder"
}
```

Example: return how many exploders, grunts and slashers spawned in the last 60 seconds.

```json 
{  
    "Mutate": "EnemiesRecentlySpawned",  
    "Seconds": 60,
    "EDs": ["ED_Spider_Grunt", "ED_Spider_Grunt_Guard", "ED_Spider_Grunt_Attacker"]
}
```

## EnemyCooldown

This mutator tracks a timer that is true after an enemy descriptor has spawned.

```json
{
    "ED_Example": {
        "Rarity": {
            "Mutate": "EnemyCooldown",
            "ED": "ED_Opp1",
            "CooldownTime": 60,
            "ValueDuringCooldown": 1000,
            "DefaultValue": 1
          }
    }
}
```

In the example, the mutator will be true for 60 seconds (the value of `CooldownTime`) after `ED_Example` has spawned. During this time, the value for the `Rarity` will be the value specified in `ValueDuringCooldown` and `DefaultValue` otherwise. The `ED` field can accept an array of enemies:

```json
{
    "ED_Example": {
        "Rarity": {
            "Mutate": "EnemyCooldown",
            "ED": ["ED_Opp1", "ED_Opp2", "ED_Opp3"],
            "CooldownTime": 60,
            "ValueDuringCooldown": 1000,
            "DefaultValue": 1
          }
    }
}
```

which will start the timer whenever one of the enemies inside the array spawns. 


## EnemyCount
Count the number of enemies currently alive on the map. Optionally, this can get the count of a specific enemy descriptor.
It's possible for this monitor to drift slightly from the actual count if base game events don't fire, but it should always be correct.

Examples:
Count all enemies on the map:

```json
{
    "Mutate": "EnemyCount"
}
```

Count of enemies with a specific descriptor:

```json
{
    "Mutate": "EnemyCount",
    "ED": "ED_Spider_Grunt"
}
```
Since CD2 v15, it is possible to specify a list of ED's and avoid having to nest addition mutators:

```json
{
    {
      "Mutate": "EnemyCount",
      "EDs": [ "A", "B", "C" ]
    }
},
```

## EnemyHealth
This mutator returns the health of a descriptor or group of descriptors. The mutator can be configured to return the maximum, minimum, or average health among enemies with a descriptor. This value is a percentage between 0 and 1. A Default can (and should) be specified. It accepts the following fields:

+ `ED` or `EDs`: the descriptor or descriptors of the enemy or group of enemies you want to track. 
+ `Default`: the value returned when there are no `ED` or `EDs` alive. Returns 0 by default.
+ `Type`: a string value which is either `Min`, `Max` or `Average`. Defaults to `Average`.

## EnemyDistance 
This mutator returns the distance of enemies of a descriptor or descriptors. The mutator can be configured to return the maximum, minimum, or average distance to the closest living player among enemies. Distance is in cm. A Default can (and should) be specified based on desired behavior. It accepts the following fields:

+ `ED` or `EDs`: the descriptor or descriptors of the enemy or group of enemies you want to track. 
+ `Default`: the value returned when there are no `ED` or `EDs` alive. Returns 0 by default.
+ `Type`: a string value which is either `Min`, `Max` or `Average`. Defaults to `Min`.

## EngineerCount
Number of engineers in the lobby. 

## Float2String

Converts an float to a string value so it can be used in the `Messages` [module](modules.md). For conversion from integers to strings, consider `Int2String` above.

## GunnerCount
Number of gunners in the lobby.

## HeldResource
For a resource, the sum of that resource in players' inventories, not deposited.
 
Example:
```json
{
    "Mutate": "HeldResource",
    "Resource": "Apoca Bloom"
}
```
## IWsLeft
Float count of the number of IWs the team still has in reserve, 0 when no IWs remain. This will be 0 until dwarves are spawned which happens after the level is setup including encounters and terrain.

## If
Check a boolean condition, "Condition", and select either "Then" or "Else". The condition is usually another mutator that returns a boolean value.
 
Example:
Remove a fast bulk from the pool during a defense objective.

```json
{
  "Mutate": "If",
  "Condition": {"Mutate": "DuringDefend"},
  "Then": [],
  "Else": ["ED_Fast_Bulk"]
}
```
## IfFloat
Choose one value or another based on a comparison of two float values.
The two floats are specified by 'Value' and the operator to be used e.g. '>=' if the comparison was to be greater than or equal. If the condition is true the 'Then' value is used, else the 'Else' condition is used.
Valid operators are: ==, >=, >, <=, <

Example: as long as the team has called less than 2 resupplies the value is 40. After the team has called their second resupply, the value is 80.

```json
{
    "Mutate": "IfFloat",
    "Value": {"Mutate": "ResuppliesCalled"},
    "<": 2,
    "Then": 40,
    "Else": 80
}
```
## IfOnSpaceRig
Returns True on the Space Rig. 

## Int2String

Converts an integer to a string value so it can be used in the `Messages` [module](modules.md). For conversion from floats to strings, consider `Float2String` above.

## Join 

Joins two strings. Can be used together with `Int2String` and `Float2String` to pass integer and float outputs from mutators into the `Messages` module. It accepts a `Values` array and a separator `Sep`. The following example shows a randomized welcome message 15 seconds into the mission:
```json 
...,
"Messages": [
    {
        "Send": {
            "Mutate": "DuringMission",
            "StartingAt": 15
        },
        "Message": {
            "Mutate": "Join",
            "Values": [
                        "Welcome to my difficulty! ",
                        {
                            "Mutate": "RandomChoice",
                            "Choices": ["Enjoy your stay.", "Thanks for playing"]
                        }
                    ]
        },
        "Sender": "CD2",
        "Type": "Developer"
    }
],
```

To see a more complex, check the `Countdown` mutator above.

## LockFloat, LockBoolean, LockString

This mutator will selectively update its value based on a condition. You may use `Lock` condition or the "Update" condition based on desired semantics:

+ `Lock`: When true, this mutator's value will not change.
+ `Update`: When false, this mutator's value will not change.
+ `Value`: This will be what the mutator will update to when it is unlocked.

The following snippet shows a mutator that will increase each time a dwarf downs until the secondary objective is finished, after which it will no longer increase and will remain the same for the rest of the mission:

```json 
{
  "Mutate": "LockFloat",
  "Lock": {"Mutate": "SecondaryFinished"},
  "Value": {"Mutate": "DwarvesDowns"}
}
```

Another example: we create a mutator that will hold the value of a string until a dwarf is revived, and at that point we randomly select another one. This mutator could be followed by a `Select` mutator to react to the new string:

```json 
{
  "Mutate": "LockString",
  "Update": {
    "Mutate": "TriggerOnChange",
    "FallOnly": true,
    "Value": { "Mutate": "DwarvesDown" }
  },
  "Value": {
    "Mutate": "RandomChoice", 
    "Choices": ["ChallengeA", "ChallengeB", "ChallengeC"]
  }
}
```

## Max 
Returns the maximum of a value.

## Min 
Returns the minimum of a value.

## MuleDroppodDistance 

Returns an average of the distance in cm between the mule and the drop pod during mission extraction. It accepts the following fields:

+ `Default`: the default value to return when there is no drop pod or there is no mule.

See also: `DroppodDistance` mutator.

## Nonzero

Accepts an integer or float `Value` and returns the boolean false if zero, true otherwise.

## Random 
Continuously samples a float number between `Min` and `Max`, uniformly.

```json
{
    "Resupply": {
        "Cost": {
            "Mutate": "Random",
            "Min": 40, 
            "Max": 60
        }
    }
}
```

## RandomChoice
Given an array of choices, choose one at random. It accepts an optional second list with weights for a weighted sampling of the choices.

Example: add either arbalests or lacerators to the enemy pool with a higher chance for arbalests.

```json
{
    "EnemyPool"{
        "add" {
            "Mutate": "RandomChoice", 
            "Choices": ["ED_Spider_Boss_TwinA", "ED_Spider_Boss_TwinB"],
            "Weights": [0.6, 0.4]
        }
    }
}
```

## RandomChoicePerMission
Choose one of a set of values for each mission. The choice is fixed to the seed of the mission. Subsequent plays of the same seed will use the same value. This mutator can be used with just `Choices`. In that case it will uniformly sample from the choices.
Optionally, a second list `Weights` provides weights for weighted sampling of the choices.

Example:

```json
{
  "Mutate": "RandomChoicePerMission",
  "Choices": [
    "bedrock",
    "hotrock",
    "dirt"
  ]
}
```

The following will be false 95 % of the time:

```json
{
  "Mutate": "RandomChoicePerMission",
  "Choices": [
    false,
    true
  ],
  "Weights": [
    95,
    5
  ]
}
```
## ResupplyUsesLeft
The count among all supply pods of uses left on a resupply. By default, resupplies start with 4 uses.

Caveat: the counts goes up immediately when a resupply is called, before it lands.

## ResuppliesCalled
Number of resupplies the team has called during the mission. This should increment almost immediately after a resupply is initiated, before another resupply can be called.
## ResupplyUsesConsumed
The number of uses that have been consumed from resupplies this mission.

## SecondaryFinished 
Returns a boolean which is true when all secondary objectives have been completed, or when there are no secondary objectives (like in Sandbox). 


## ScoutCount
Number of scouts in the lobby. 

## Select
Similar to a switch statement in programming languages, this mutator allows to select different options based on a string value. It is very useful when used together with global variables from the `Var` module:

```json
...,
"Vars": {
    "Pressure": {
        "Type": "String",
        "Value": "Easy"
    }
},
"DifficultySetting": {
    "EnemyCountModifier": {
        "Mutate": "Multiply",
        "BaseValues": {
            "Mutate": "ByPlayerCount",
            "Values": [1.9, 2.1, 2.7, 3.3]
        },
        "Multiplier": {
            "Mutate": "Select",
            "Select": {"Var": "Pressure"}
            "Default": 1,
            "Easy": 1, 
            "Hard": 1.3 
        }
    }
},
...
```

## SquareWave
Alternates between two values with a given period.

Example:
Add and remove stalkers on alternating periods of 250 seconds. 

```json
{
    "EnemyPool": {
        "clear": false,
        "add": [
            {
              "Mutate": "IfFloat",
              "Value": {
                "Mutate": "SquareWave",
                "Period": 250,
                "High": 1,
                "Low": 0
              },
              ">": 0.5,
              "Then": ["ED_Spider_Stalker"],
              "Else": []
            }
        ],
        "remove": [
            {
              "Mutate": "IfFloat",
              "Value": {
                "Mutate": "SquareWave",
                "Period": 250,
                "High": 1,
                "Low": 0
              },
              ">": 0.5,
              "Then": [],
              "Else": ["ED_Spider_Stalker"]
            }
        ],
    }
}
```
## TimeDelta
Change a value over time. Time matches the mission clock in the escape menu in-game, including starting before players receive control of their dwarves.
The value is determined by `InitialValue + RateOfChange * Max(0, Time - StartDelay)`.

Parameters:

* `InitialValue`: Value at time 0 and up until `StartDelay`
* `StartDelay`: Time in seconds to stay at the `InitialValue` before changing. 
* `RateOfChange`: Rate per second to change the value.

Example:

```json
{
    "Mutate": "TimeDelta",
    "InitialValue": 3.1,
    "RateOfChange": 0.0033,
    "StartDelay": 400
 }
```
## TotalResource
Sum of a resource held in players inventories and the group depot. Any resource can be referenced by the name as it appears in the in-game UI.
 
Example:
```json
{
    "Mutate": "TotalResource",
    "Resource": "Morkite"
}
```

## Trigger mutators
These are a special group of mutators that can be used on boolean values, typically (but not limited to) on the `Enabled` field of a wavespawner. Please see some examples below. The fields of each trigger are specified `like this`. There are currently the following triggers:

### TriggerOnce
Triggers only on the first False -> True `In` transition, then never again. Used if something has to happen exactly once per mission. It can optionally have a `Reset` field which resets its ability to trigger.

### TriggerNTimes
Allows up to `N` False -> True `In` transitions, then blocks any further attempts. Same idea as `TriggerOnce` but for multiple events. 

### TriggerSometimes
Triggers only a percentage of times `P` when `In` goes from False -> True. As a simple example, this could be used to spawn a wave when a player goes down but only with a probability `P` of that happening. 

### TriggerCooldown
After the boolean `In` goes from True -> False, it can't go True again for `N` seconds.

### TriggerFixedDuration
Stays True for `N` seconds before switching back to False, regardless of what happens to its boolean input. It can be configured to `Reset: true` if the input transitions from False -> True during the fixed window. 

### TriggerSustain 
Extends a current True `In` state by `N` additional seconds.

### TriggerDelay
Delays the transition of the `In` boolean by `N` seconds.

### TriggerOnChange
It accepts a float input `In`. The trigger becomes momentarily true if the input float value changes. It accepts the special values `RiseOnly` and `FallOnly` to fire only on an increase or a decrease of the input value, respectively. 

### Trigger examples

The following is an example on how to use triggers. It spawns a small wave of exploders 15 seconds after calling a resupply, but only 30 % of the time: 

```json 
  "WaveSpawners": [
    {
      "Enabled": {
        "Mutate": "TriggerSometimes",
        "P": 0.3,
        "In": {
          "Mutate": "TriggerDelay",
          "N": 15,
          "In": {
            "Mutate": "TriggerOnChange",
            "In": {
              "Mutate": "ResuppliesCalled"
            }
          }
        }
      },
      "Enemies": [
        "ED_Spider_Exploder"
      ],
      "Difficulty": 300,
      "Interval": 20,
      "Distance": 50,
      "Locations": 3,
      "SpawnOnEnable": true
    }
  ]
```

Following the order of the mutators:

+ `TriggerOnChange` detects a change in `ResuppliesCalled` and becomes momentarily True.
+ `TriggerDelay` adds a delay of 15 seconds to the `TriggerOnChange` transition.
+ Finally, `TriggerSometimes` lets the True transition pass but only 30 % of the time.

 A similar example, but now the waves of exploders is sustained for 20 seconds:

```json
  "WaveSpawners": [
    {
      "Enabled": {
          "Mutate": "TriggerFixedDuration",
          "N": 20,
          "In": {
            "Mutate": "TriggerSometimes",
            "P": 0.3,
            "In": {
              "Mutate": "TriggerDelay",
              "N": 15,
              "In": {
                "Mutate": "TriggerOnChange",
                "In": {
                  "Mutate": "ResuppliesCalled"
                }
              }
            }
          }
      },
      "Enemies": [
        "ED_Spider_Exploder"
      ],
      "Difficulty": 20,
      "Interval": 1,
      "Distance": 50,
      "Locations": 3,
      "SpawnOnEnable": true
    }
  ]
```

The chain of mutators is the same, but now a `TriggerFixedDuration` has been added on top which will grant a 20 second window for the wavespawner to be active. Since its `Interval` is set to 1, this will generate 20 spawn events in total. 
