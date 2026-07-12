# `Direct` enemy controls 

`Direct` is a special field in enemy descriptors that allows changing properties that are not directly exposed by CD2 through other modules like the `Breeder` or the `CaveLeech` subfields. **When using `Direct`, remember that not all fields will work in-game.** The names of the `Direct` subfields can be found by looking into the enemy properties in UE4, but structs are not supported for now. A couple of examples of use:

```json
# A bulk with no meatballs, no explosion and no carve.
"Enemies": {
    "ED_Melee_Bulk":{
        "Base": "ED_Spider_ExploderTank",
        "Direct": {
            "Float:CarveDiameter": 0,
            "Int:NumClusterBombs": 0,
            "Float:DamageDeathExplosion.DamageRadius": 0,
            "Float:DamageDeathExplosion.MaxDamageRadius": 0
        }
    }
}
```

```json
# A patrol bot that deals no damage on bump
"Enemies": {
    "ED_PatrolBot": {
        "Direct": {
            "Float:BumpDamage.Damage": 0
        }
    }
}
```

The following non-exhaustive list compiled by @theBrain is provided as a reference. 

## ED_PumpkinLootBug

| Control | Default Value |
| -------- | ------- |
| Float:DamageLootDropChance | 0.2 |
| Float:DamageLootDropCoolDown | 0.5 |
| Float:EatValueMultiplier | 1.5 |
| Float:SearchChunksRadius | 2500.0 |
| Float:SearchChunksInterval | 15.0 |
| Bool:CanPlayerStandOn | True |
| Bool:UseDormancy | True |
| Float:NetUpdateFrequency | 0.25 |
| Float:MinNetUpdateFrequency | 0.1 |
| Float:NetPriority | 1.0 |
| Bool:InstantUsable.bShowUsingUI | False |
| Bool:InstantUsable.Usable | True |
| Int:InstantUsable.Priority | 5 |
| Bool:InstantUsable.IsClientPredictive | True |
| Float:Sphere.SphereRadius | 70.0 |
| Bool:Sphere.bGenerateOverlapEvents | False |
| Float:Dropshadow.CachedMaxDrawDistance | 1300.0 |
| Bool:Dropshadow.bGenerateOverlapEvents | False |
| Float:Timeline_0_Template.TimelineLength | 1.0 |

## ED_Flea

| Control | Default Value |
| -------- | ------- |
| Float:FleeFromplayerRange | 500.0 |
| Float:MinWalkTIme | 18.0 |
| Float:MaxWalkTime | 40.0 |
| Float:StaggerDurationMultiplier | 0.0 |
| Bool:FleeInsteadOfBackingOff | True |
| Float:NetUpdateFrequency | 0.1 |
| Float:MinNetUpdateFrequency | 0.1 |
| Float:NetPriority | 1.5 |
| Bool:Audio Flying.bAutoActivate | False |
| Bool:Enemy.bIsPingableByLaserpointer | True |
| Float:GroundToAir.WalkTime | 100.0 |
| Bool:GroundToAir.WalkUseTimer | False |
| Bool:GroundToAir.FlyUseTimer | False |
| Float:InDanger.DamageTimeLimit | 3.0 |
| Float:InDanger.DamageThreshold | 10.0 |
| Float:Trail.LDMaxDrawDistance | 4500.0 |
| Float:Trail.CachedMaxDrawDistance | 4500.0 |
| Bool:PointLight.bUseInverseSquaredFalloff | False |
| Float:PointLight.SourceRadius | 11.646377 |
| Float:PointLight.SoftSourceRadius | 50.0 |
| Float:PointLight.AttenuationRadius | 150.0 |
| Float:PointLight.MaxDistanceFadeRange | 5000.0 |
| Float:PointLight.Intensity | 1.5 |
| Bool:PointLight.CastShadows | False |
| Bool:Wings.bEnableUpdateRateOptimizations | True |
| Float:Wings.LDMaxDrawDistance | 4500.0 |
| Float:Wings.CachedMaxDrawDistance | 4500.0 |
| Float:Sphere.SphereRadius | 128.70302 |

## ED_Spider_Hoarder

| Control | Default Value |
| -------- | ------- |
| Float:DamageLootDropChance | 0.2 |
| Float:DamageLootDropCooldown | 0.5 |
| Bool:IsAlive | True |
| Float:AlertedSpeed | 400.0 |
| Float:DeathDuration | 20.0 |
| Float:StaggerDurationMultiplier | 0.05 |
| Bool:FrozenPauseLogic | True |
| Float:AttackerRadius | 40.0 |
| Bool:AudioScaredBegin.bAutoActivate | False |
| Bool:AudioScaredEnd.bAutoActivate | False |
| Bool:AudioScaredLoop.bAutoActivate | False |
| Bool:PointLight1.bUseInverseSquaredFalloff | False |
| Float:PointLight1.AttenuationRadius | 400.0 |
| Float:PointLight1.Intensity | 8.0 |
| Bool:PointLight1.CastShadows | False |
| Float:PointLight2.AttenuationRadius | 75.0 |
| Float:PointLight2.Intensity | 500.0 |
| Bool:PointLight2.CastShadows | False |
| Float:PointLight3.AttenuationRadius | 75.0 |
| Float:PointLight3.Intensity | 500.0 |
| Bool:PointLight3.CastShadows | False |
| Float:SK_HoarderBack_A.LDMaxDrawDistance | 12500.0 |
| Float:SK_HoarderBack_A.CachedMaxDrawDistance | 12500.0 |
| Float:SK_HoarderHead_A.LDMaxDrawDistance | 12500.0 |
| Float:SK_HoarderHead_A.CachedMaxDrawDistance | 12500.0 |
| Float:Sphere.SphereRadius | 100.0 |
| Float:Timeline_0_Template.TimelineLength | 0.6 |
| Bool:Timeline_0_Template.bLoop | True |
| Float:Timeline_2_Template.TimelineLength | 3.0 |
| Bool:Timeline_2_Template.bLoop | True |

## ED_Prospector

| Control | Default Value |
| -------- | ------- |
| Int:WeakpointsLeft | 2 |
| Float:CooldownDuration | 30.0 |
| Int:DirtSamplesTaken | 20 |
| Int:MaxDirtSamples | 40 |
| Float:ReinforcementsAllowed | 2.0 |
| Float:AlarmDuration | 10.0 |
| Float:ReinforcementDelay | 3.0 |
| Float:ReinforcementCooldown | 30.0 |
| Int:PatrolBotDifficulty | 2 |
| Bool:ShouldSpawnDataCell | True |
| Float:EnginePowerMultiplier | 2.0 |
| Float:HeadResponsiveness | 1.5 |
| Bool:UseDormancy | True |
| Float:StaggerDurationMultiplier | 0.0 |
| Bool:FrozenPauseLogic | True |
| Float:NetUpdateFrequency | 5.0 |
| Float:MinNetUpdateFrequency | 0.5 |
| Bool:ProspectingAlarmedIdle_Cue.bAutoActivate | False |
| Bool:ProspectingDroneScreamAlerted_Cue.bAutoActivate | False |
| Bool:ProspectingDroneStartSampling_Cue.bAutoActivate | False |
| Bool:ProspectingDroneStartScanning_Cue.bAutoActivate | False |
| Float:Prospector_Idle_Cue.VolumeMultiplier | 4.0 |
| Float:Capsule.CapsuleHalfHeight | 227.96706 |
| Float:Capsule.CapsuleRadius | 90.61318 |
| Float:Niagara_RadioWaves.LDMaxDrawDistance | 6000.0 |
| Float:Niagara_RadioWaves.CachedMaxDrawDistance | 6000.0 |
| Bool:Niagara_RadioWaves.bAutoActivate | False |
| Float:NS_Idle.LDMaxDrawDistance | 6000.0 |
| Float:NS_Idle.CachedMaxDrawDistance | 6000.0 |
| Float:NS_Trail.LDMaxDrawDistance | 6000.0 |
| Float:NS_Trail.CachedMaxDrawDistance | 6000.0 |
| Float:Particles_Dirt.LDMaxDrawDistance | 8000.0 |
| Float:Particles_Dirt.CachedMaxDrawDistance | 8000.0 |
| Bool:Particles_Dirt.bAutoActivate | False |
| Float:PawnSensing.HearingThreshold | 700.0 |
| Float:PawnSensing.LOSHearingThreshold | 1400.0 |
| Float:PawnSensing.SightRadius | 1500.0 |
| Bool:PawnSensing.bEnableSensingUpdates | False |
| Bool:PawnSensing.bHearNoises | False |
| Float:PawnSensing.PeripheralVisionAngle | 180.0 |
| Bool:PawnStats.UseDormancy | True |
| Float:PointLight_Eye.AttenuationRadius | 50.0 |
| Float:PointLight_Eye.MaxDrawDistance | 6000.0 |
| Float:PointLight_Eye.Intensity | 300.0 |
| Bool:PointLight_Eye.CastShadows | False |
| Float:PointLight_Weakpoint_L.SourceRadius | 50.0 |
| Float:PointLight_Weakpoint_L.SoftSourceRadius | 100.0 |
| Float:PointLight_Weakpoint_L.AttenuationRadius | 150.0 |
| Float:PointLight_Weakpoint_L.MaxDrawDistance | 10000.0 |
| Float:PointLight_Weakpoint_L.Intensity | 1250.0 |
| Bool:PointLight_Weakpoint_L.CastShadows | False |
| Float:PointLight_Weakpoint_R.SourceRadius | 50.0 |
| Float:PointLight_Weakpoint_R.SoftSourceRadius | 100.0 |
| Float:PointLight_Weakpoint_R.AttenuationRadius | 150.0 |
| Float:PointLight_Weakpoint_R.MaxDrawDistance | 10000.0 |
| Float:PointLight_Weakpoint_R.Intensity | 1250.0 |
| Bool:PointLight_Weakpoint_R.CastShadows | False |
| Float:Light_Engine.SourceWidth | 97.053986 |
| Float:Light_Engine.SourceHeight | 14.917264 |
| Float:Light_Engine.BarnDoorAngle | 14.285712 |
| Float:Light_Engine.BarnDoorLength | 75.0 |
| Float:Light_Engine.MaxDrawDistance | 15000.0 |
| Float:Light_Engine.Intensity | 300.0 |
| Bool:Light_Engine.CastShadows | False |
| Float:Light_Exhausts.SourceWidth | 147.03517 |
| Float:Light_Exhausts.SourceHeight | 11.317553 |
| Float:Light_Exhausts.BarnDoorAngle | 60.400005 |
| Float:Light_Exhausts.BarnDoorLength | 75.0 |
| Float:Light_Exhausts.AttenuationRadius | 319.03848 |
| Float:Light_Exhausts.MaxDrawDistance | 8000.0 |
| Float:Light_Exhausts.Intensity | 1200.0 |
| Bool:Light_Exhausts.CastShadows | False |
| Float:ShieldMesh.LDMaxDrawDistance | 10000.0 |
| Float:ShieldMesh.CachedMaxDrawDistance | 10000.0 |
| Bool:ShieldMesh.bVisible | False |
| Float:SM_LightCone001.LDMaxDrawDistance | 10000.0 |
| Float:SM_LightCone001.CachedMaxDrawDistance | 10000.0 |
| Bool:SM_LightCone001.bGenerateOverlapEvents | False |
| Bool:SM_LightCone001.bHiddenInGame | True |
| Float:WeakpointGlow.CurveMultiplier | 10.0 |
| Bool:WeakpointGlow.AddFirstChannelAutomatically | False |

## ED_BarrageInfector

| Control | Default Value |
| -------- | ------- |
| Float:BaseEyeHeight | 300.0 |
| Bool:bReplicateMovement | False |
| Float:NetUpdateFrequency | 15.0 |
| Float:NetPriority | 2.0 |
| Float:Capsule.CapsuleHalfHeight | 90.0 |
| Float:Capsule.CapsuleRadius | 80.0 |
| Float:EnemyLineOfSight.LoSInterval | 1.0 |
| Float:EnemyLineOfSight.LoSIntervalVariance | 0.0 |
| Float:PawnSensing.SightRadius | 2000.0 |
| Bool:PawnSensing.bHearNoises | False |
| Float:PawnSensing.PeripheralVisionAngle | 180.0 |
| Float:PointLight.AttenuationRadius | 200.0 |
| Float:PointLight.Intensity | 2500.0 |
| Bool:PointLight.CastShadows | False |
| Float:PointLight_Mouth.AttenuationRadius | 200.0 |
| Float:PointLight_Mouth.Intensity | 1500.0 |
| Bool:PointLight_Mouth.CastShadows | False |
| Bool:ProjectileAttack.ProjectilesIgnoreEachOther | True |
| Float:ProjectileAttack.MaxRange | 0.0 |
| Bool:SkeletalMesh.bEnableUpdateRateOptimizations | True |
| Float:SkeletalMesh.LDMaxDrawDistance | 15000.0 |
| Float:SkeletalMesh.CachedMaxDrawDistance | 15000.0 |
| Bool:SkeletalMesh.bReceivesDecals | False |
| Int:WeakpointGlow.ReplaceMatIndex | 1 |

## ED_CaveLeech

| Control | Default Value |
| -------- | ------- |
| Float:MaxDistanceXY | 1000.0 |
| Float:GrapDistance | 200.0 |
| Float:GrapDelay | 0.1 |
| Float:TentacleSpeed | 600.0 |
| Float:TentacleRetractSpeed | 1100.0 |
| Float:TentaclePullSpeed | 2000.0 |
| Float:TentacleDropPlayerSpeed | 1500.0 |
| Float:TentacleDropGroundDistance | 300.0 |
| Float:TentacleAttachOffset | 75.0 |
| Float:BiteDistance | 50.0 |
| Bool:bReplicateMovement | False |
| Float:NetUpdateFrequency | 60.0 |
| Bool:HeadAudio.bAutoActivate | False |
| Float:PointLight.AttenuationRadius | 400.0 |
| Float:PointLight.Intensity | 3500.0 |
| Bool:PointLight.CastShadows | False |
| Bool:TopMesh.bDeferKinematicBoneUpdate | True |
| Float:TopMesh.CachedMaxDrawDistance | 15000.0 |
| Bool:TopMesh.bVisibleInReflectionCaptures | False |
| Bool:TopMesh.bVisible | False |
| Bool:HeadCollision.bGenerateOverlapEvents | False |
| Float:HitCollider.SphereRadius | 120.0 |
| Bool:StaticMesh.bVisible | False |
| Bool:StaticMesh.bHiddenInGame | True |

## ED_Crawler

| Control | Default Value |
| -------- | ------- |
| Float:StaggerDurationMultiplier | 0.6 |
| Float:StaggerImunityWindow | 2.0 |
| Bool:FrozenPauseLogic | True |
| Float:AttackerRadius | 100.0 |
| Float:BallisticMovement.MinMoveDistance | 800.0 |
| Float:BallisticMovement.RotateDelay | 0.333 |
| Float:BallisticMovement.LaunchDelay | 0.67 |
| Float:BallisticMovement.LandingDelay | 0.75 |
| Bool:BallisticMovement.bReplicates | True |
| Bool:Niagara.bAutoActivate | False |
| Float:PlayerProximity.Cooldown | 2.0 |
| Float:PlayerProximity.Distance | 600.0 |
| Float:Mouth_Light.AttenuationRadius | 30.0 |
| Float:Mouth_Light.Intensity | 100.0 |
| Bool:Mouth_Light.CastShadows | False |
| Bool:PoseCorrection.Enabled | True |
| Float:PoseCorrection.FrontX | 80.0 |
| Float:PoseCorrection.BackX | -80.0 |
| Float:HeadshotSphere.SphereRadius | 12.0 |
| Float:Sphere.SphereRadius | 50.0 |
| Float:DropShadow.CachedMaxDrawDistance | 2300.0 |
| Bool:DropShadow.bGenerateOverlapEvents | False |
| Bool:DropShadow.bUseAttachParentBound | True |

## ED_SpiderSpawner

| Control | Default Value |
| -------- | ------- |
| Int:DeathSpawnCount | 15 |
| Float:Spawn Interval | 10.0 |
| Int:MaxConcurrentEnemies | 20 |
| Bool:bReplicateMovement | False |
| Float:NetUpdateFrequency | 1.0 |
| Float:MinNetUpdateFrequency | 1.0 |
| Float:Eye1.Health | 700.0 |
| Float:Eye2.Health | 700.0 |
| Float:Eye3.Health | 700.0 |
| Float:Eye4.Health | 700.0 |
| Float:PlayerCollision.CapsuleHalfHeight | 340.0 |
| Float:PlayerCollision.CapsuleRadius | 165.0 |
| Bool:PathfinderCollision.ActivatePFCollisionAtInit | True |
| Float:PawnSensing.SightRadius | 3000.0 |
| Bool:PawnSensing.bHearNoises | False |
| Float:PawnSensing.PeripheralVisionAngle | 360.0 |
| Bool:SK_Spawner.bEnableUpdateRateOptimizations | True |
| Float:SK_Spawner.CachedMaxDrawDistance | 15000.0 |
| Float:Spawner_Eye1_Rig.CachedMaxDrawDistance | 15000.0 |
| Float:Spawner_Eye2_Rig.CachedMaxDrawDistance | 15000.0 |
| Float:Spawner_Eye3_Rig.CachedMaxDrawDistance | 15000.0 |
| Float:Spawner_Eye4_Rig.CachedMaxDrawDistance | 15000.0 |
| Float:Sphere_Eye1.SphereRadius | 25.0 |
| Bool:Sphere_Eye1.bGenerateOverlapEvents | False |
| Float:Sphere_Eye2.SphereRadius | 25.0 |
| Bool:Sphere_Eye2.bGenerateOverlapEvents | False |
| Float:Sphere_Eye3.SphereRadius | 25.0 |
| Bool:Sphere_Eye3.bGenerateOverlapEvents | False |
| Float:Sphere_Eye4.SphereRadius | 25.0 |
| Bool:Sphere_Eye4.bGenerateOverlapEvents | False |

## ED_Bomber

| Control | Default Value |
| -------- | ------- |

## ED_Bomber_Explosive

| Control | Default Value |
| -------- | ------- |
| Float:AttackModeRotationSpeed | 6.0 |
| Float:DashPoints.DashSpeed | 1100.0 |
| Bool:ProjectileAttack.ProjectilesIgnoreEachOther | True |

## ED_Bomber_Ice

| Control | Default Value |
| -------- | ------- |

## ED_Grabber

| Control | Default Value |
| -------- | ------- |
| Float:WanderingSpeed | 250.0 |
| Float:WanderingAcceleration | 1000.0 |
| Float:ChaseSpeed | 750.0 |
| Float:ChaseAcceleration | 4000.0 |
| Float:CarrySpeed | 500.0 |
| Float:CarryAcceleration | 3000.0 |
| Float:FleeSpeed | 800.0 |
| Float:FleeAcceleration | 1000.0 |
| Float:ExtraUpForce | 15.0 |
| Bool:UsesAttackStance | False |
| Bool:LookStraight | True |
| Float:StaggerDurationMultiplier | 0.0 |
| Bool:bAlwaysRelevant | True |
| Float:NetUpdateFrequency | 20.0 |

## ED_Mactera_Shooter_Amber

| Control | Default Value |
| -------- | ------- |
| Float:PointLight1.AttenuationRadius | 500.0 |
| Bool:PointLight1.CastShadows | False |
| Float:PointLight2.AttenuationRadius | 50.0 |
| Float:PointLight2.Intensity | 500.0 |
| Bool:PointLight2.CastShadows | False |
| Bool:Mesh_Infestation01.bGenerateOverlapEvents | False |
| Bool:Mesh_Infestation02.bGenerateOverlapEvents | False |

## ED_Mactera_Shooter_HeavyVeteran

| Control | Default Value |
| -------- | ------- |
| Float:DistanceForAttackMode | 800.0 |
| Float:DashPoints.MaxRangeFromPlayer | 800.0 |
| Float:DashPoints.MinRangeFromPlayer | 450.0 |
| Float:DashPoints.MaxHeightAboveTarget | 300.0 |
| Float:DashPoints.DashSpeed | 400.0 |

## ED_Mactera_Shooter_Normal

| Control | Default Value |
| -------- | ------- |
| Float:DashPoints.MaxHeightAboveTarget | 400.0 |

## ED_Mactera_TripleShooter

| Control | Default Value |
| -------- | ------- |
| Float:DistanceForAttackMode | 1400.0 |
| Float:DashPoints.MaxRangeFromPlayer | 1500.0 |
| Float:DashPoints.MinRangeFromPlayer | 1050.0 |
| Float:DashPoints.MinHeightAboveTarget | 150.0 |
| Float:DashPoints.DashSpeed | 600.0 |
| Float:ProjectileAttack.MaxRange | 0.0 |
| Int:WeakpointGlowComponent.ReplaceMatIndex | 2 |

## ED_HydraWeed

| Control | Default Value |
| -------- | ------- |
| Float:SpawnRadius | 1400.0 |
| Int:NumShootersKilledToOpen | 4 |
| Bool:IsOpen | True |
| Bool:IsDormant | True |
| Int:MaxAllowedShooters | 5 |
| Float:MaxLightIntensity | 20.0 |
| Int:MaxNumHealers | 1 |
| Float:StayOpenTimerTick | 0.2 |
| Float:TimeToDamageConversion | 150.0 |
| Float:StayOpenWhenBellowThisHealthPercentage | 0.05 |
| Float:HealCapPercentage | 1.0 |
| Float:HealthCheckPointValue1 | 0.666 |
| Float:HealthCheckPointValue2 | 0.33 |
| Float:MinHealthPercentageToSpawnHealingPods | 0.8 |
| Int:NumSpawnAttempts | 10 |
| Float:ShooterDormantRange | 1000.0 |
| Float:ShooterActiveRange | 5000.0 |
| Float:StopFightingDistance | 4500.0 |
| Float:ResumeFightingDistance | 2500.0 |
| Bool:CanFlee | False |
| Float:BaseEyeHeight | 128.0 |
| Bool:bReplicateMovement | False |
| Bool:bCollideWhenPlacing | False |
| Float:NetUpdateFrequency | 15.0 |
| Bool:P_GodRays.bVisible | False |
| Bool:PathfinderCollision.ActivatePFCollisionAtInit | True |
| Bool:PointLight.bUseInverseSquaredFalloff | False |
| Float:PointLight.AttenuationRadius | 1300.0 |
| Float:PointLight.Intensity | 100.0 |
| Bool:PointLight.CastShadows | False |
| Bool:SkeletalMesh.bReceivesDecals | False |
| Float:SpawnActorWithDebrisPos.MinDistanceBetweenSpwans | 500.0 |
| Bool:SpawnActorWithDebrisPos.AvoidImportantLocations | True |
| Float:Sphere.SphereRadius | 110.0 |
| Float:WakeUpTrigger.SphereRadius | 800.0 |
| Bool:Carving Mesh.bHiddenInGame | True |
| Bool:SM_HydraWeed_Extra_Roots_SM_HydraWeed_Root_01.bGenerateOverlapEvents | False |
| Bool:SM_HydraWeed_Extra_Roots_SM_HydraWeed_Root_02.bGenerateOverlapEvents | False |
| Bool:SM_HydraWeed_Extra_Roots_SM_HydraWeed_Root_03.bGenerateOverlapEvents | False |
| Bool:SM_HydraWeed_Extra_Roots_SM_HydraWeed_Root_04.bGenerateOverlapEvents | False |
| Bool:SM_HydraWeed_Extra_Roots_SM_HydraWeed_Root_05.bGenerateOverlapEvents | False |
| Bool:SM_HydraWeed_Extra_Roots_SM_HydraWeed_Root_06.bGenerateOverlapEvents | False |
| Float:GlowIntensity_Template.TimelineLength | 1.5 |

## ED_InfestationLarva

| Control | Default Value |
| -------- | ------- |
| Float:NetUpdateFrequency | 20.0 |
| Float:MeleeAttack.MaxRange | 250.0 |
| Float:DropShadow.CachedMaxDrawDistance | 2300.0 |
| Bool:DropShadow.bGenerateOverlapEvents | False |
| Bool:DropShadow.bUseAttachParentBound | True |

## ED_Jelly_Spawn

| Control | Default Value |
| -------- | ------- |
| Float:Trail.LDMaxDrawDistance | 5000.0 |
| Float:Trail.CachedMaxDrawDistance | 5000.0 |

## ED_Jelly_Swarmer

| Control | Default Value |
| -------- | ------- |

## ED_JellyBreeder

| Control | Default Value |
| -------- | ------- |

## ED_InfectedMule

| Control | Default Value |
| -------- | ------- |
| Float:IntroductionTime | 3.0 |
| Float:BigShieldScale | 8.0 |
| Float:ShieldGrowthRate | 6.0 |
| Float:LerpExp | 0.25 |
| Float:MinimumShieldSize | 0.25 |
| Float:IdleRotationSpeed | 190.0 |
| Float:LaserScaleRate | 53.0 |
| Float:MaxSearchAngle | 60.0 |
| Bool:DoSpecialWhenFriendly | False |
| Bool:PerfectTrackingWhenEnemy | False |
| Float:TurretSpinSpeed | 200.0 |
| Float:ChanceToSpawnParasite | 0.5 |
| Float:LockonTime | 0.25 |
| Float:GunRange | 2500.0 |
| Float:FireRate | 12.0 |
| Float:GrenadeFireRate | 0.5 |
| Float:BurstCooldown | 0.8 |
| Int:MinBurst | 6 |
| Int:MaxBurst | 8 |
| Float:TurretLerpSpeed | 7.0 |
| Float:DamageWhenFriendly | 15.0 |
| Float:FriendlyFriendlyFireMultiplier | 0.08 |
| Bool:Box.bGenerateOverlapEvents | False |
| Bool:ActivationParticle.bAutoActivate | False |
| Float:PawnSensing.HearingThreshold | 0.0 |
| Float:PawnSensing.LOSHearingThreshold | 0.0 |
| Float:PawnSensing.SightRadius | 1000.0 |
| Bool:PawnSensing.bHearNoises | False |
| Float:PawnSensing.PeripheralVisionAngle | 180.0 |
| Float:Light_Leg1.AttenuationRadius | 0.0 |
| Float:Light_Leg1.Intensity | 0.0 |
| Bool:Light_Leg1.CastShadows | False |
| Bool:Light_Leg1.bVisible | False |
| Bool:Light_Leg1.bHiddenInGame | True |
| Float:Light_Leg2.AttenuationRadius | 0.0 |
| Float:Light_Leg2.Intensity | 0.0 |
| Bool:Light_Leg2.CastShadows | False |
| Bool:Light_Leg2.bVisible | False |
| Bool:Light_Leg2.bHiddenInGame | True |
| Float:Light_Leg3.AttenuationRadius | 0.0 |
| Float:Light_Leg3.Intensity | 0.0 |
| Bool:Light_Leg3.CastShadows | False |
| Bool:Light_Leg3.bVisible | False |
| Bool:Light_Leg3.bHiddenInGame | True |
| Float:Light_Leg4.AttenuationRadius | 0.0 |
| Float:Light_Leg4.Intensity | 0.0 |
| Bool:Light_Leg4.CastShadows | False |
| Bool:Light_Leg4.bVisible | False |
| Bool:Light_Leg4.bHiddenInGame | True |
| Float:Light_TurretGlow.AttenuationRadius | 200.0 |
| Float:Light_TurretGlow.MaxDrawDistance | 12500.0 |
| Bool:Light_TurretGlow.CastShadows | False |
| Float:WakeUp_PointLight.AttenuationRadius | 4500.0 |
| Float:WakeUp_PointLight.Intensity | 0.0 |
| Bool:WakeUp_PointLight.CastShadows | False |
| Float:UseSphere.SphereRadius | 120.0 |
| Bool:UseSphere.bGenerateOverlapEvents | False |
| Float:SpotLight1.InnerConeAngle | 5.0 |
| Float:SpotLight1.OuterConeAngle | 30.0 |
| Float:SpotLight1.AttenuationRadius | 500.0 |
| Float:SpotLight1.Intensity | 3000.0 |
| Bool:SpotLight1.CastShadows | False |
| Bool:Widget.bWindowFocusable | False |
| Bool:Widget.bGenerateOverlapEvents | False |

## ED_Bomber_Rockpox_Plague

| Control | Default Value |
| -------- | ------- |
| Float:ArmorHealthDamage.RadialSocketDamageMultiplier | 0.1 |
| Float:InfectionMaster.SpikeScale | 0.55 |
| Float:InfectionMaster.InfectionScale | 0.65 |
| Bool:InfectionMaster.KillWhenAllPointsDestroyed | True |
| Float:InfectionPoint10.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint10.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint10.bGenerateOverlapEvents | False |
| Float:InfectionPoint2.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint2.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint2.bGenerateOverlapEvents | False |
| Float:InfectionPoint6.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint6.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint6.bGenerateOverlapEvents | False |
| Float:InfectionPoint7.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint7.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint7.bGenerateOverlapEvents | False |
| Float:InfectionPoint8.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint8.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint8.bGenerateOverlapEvents | False |
| Float:InfectionPoint9.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint9.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint9.bGenerateOverlapEvents | False |

## ED_Spider_Grunt_RockpoxPlague

| Control | Default Value |
| -------- | ------- |
| Float:ArmorHealthDamage.RadialSocketDamageMultiplier | 0.1 |
| Bool:ArmorHealthDamage.AffectedByAmorBreak | False |
| Float:InfectionMaster.SpikeScale | 0.8 |
| Float:InfectionMaster.InfectionScale | 0.8 |
| Bool:InfectionMaster.KillWhenAllPointsDestroyed | True |
| Bool:ProjectileThrowerAttack.RotateToTarget | True |
| Float:DropShadow.LDMaxDrawDistance | 2300.0 |
| Float:InfectionPoint1.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint1.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint1.bGenerateOverlapEvents | False |
| Float:InfectionPoint2.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint2.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint2.bGenerateOverlapEvents | False |
| Float:InfectionPoint3.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint3.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint3.bGenerateOverlapEvents | False |
| Float:InfectionPoint5.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint5.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint5.bGenerateOverlapEvents | False |
| Float:InfectionPoint6.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint6.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint6.bGenerateOverlapEvents | False |
| Float:InfectionPoint7.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint7.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint7.bGenerateOverlapEvents | False |
| Float:InfectionPoint8.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint8.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint8.bGenerateOverlapEvents | False |
| Float:InfectionPoint9.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint9.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint9.bGenerateOverlapEvents | False |

## ED_Spider_Tank_RockpoxPlague

| Control | Default Value |
| -------- | ------- |
| Int:InfectionMaster.InfectionPoints | 5 |
| Bool:InfectionMaster.ExtraInfectionPointsWithMorePlayers | True |
| Float:InfectionMaster.SpikeScale | 0.8 |
| Float:InfectionMaster.InfectionScale | 0.8 |
| Bool:InfectionMaster.KillWhenAllPointsDestroyed | True |
| Float:PawnSensing.SightRadius | 1000.0 |
| Float:InfectionPoint10.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint10.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint10.bGenerateOverlapEvents | False |
| Float:InfectionPoint1.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint1.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint1.bGenerateOverlapEvents | False |
| Float:InfectionPoint2.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint2.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint2.bGenerateOverlapEvents | False |
| Float:InfectionPoint3.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint3.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint3.bGenerateOverlapEvents | False |
| Float:InfectionPoint4.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint4.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint4.bGenerateOverlapEvents | False |
| Float:InfectionPoint5.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint5.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint5.bGenerateOverlapEvents | False |
| Float:InfectionPoint6.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint6.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint6.bGenerateOverlapEvents | False |
| Float:InfectionPoint7.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint7.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint7.bGenerateOverlapEvents | False |
| Float:InfectionPoint8.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint8.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint8.bGenerateOverlapEvents | False |
| Float:InfectionPoint9.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint9.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint9.bGenerateOverlapEvents | False |

## ED_JellyBreeder_RockpoxPlague

| Control | Default Value |
| -------- | ------- |
| Float:TimeBetweenBursts | 10.0 |
| Float:TimeBetweenEggs | 5.0 |
| Float:ArmorHealthDamage.RadialSocketDamageMultiplier | 0.1 |
| Bool:ArmorHealthDamage.AffectedByAmorBreak | False |
| Int:InfectionMaster.InfectionPoints | 7 |
| Bool:InfectionMaster.ExtraInfectionPointsWithMorePlayers | True |
| Float:InfectionMaster.SpikeScale | 0.9 |
| Float:InfectionMaster.InfectionScale | 0.8 |
| Bool:InfectionMaster.KillWhenAllPointsDestroyed | True |
| Bool:ProjectileThrowerAttack.RotateToTarget | True |
| Float:InfectionPoint10.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint10.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint10.bGenerateOverlapEvents | False |
| Float:InfectionPoint11.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint11.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint11.bGenerateOverlapEvents | False |
| Float:InfectionPoint1.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint1.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint1.bGenerateOverlapEvents | False |
| Float:InfectionPoint2.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint2.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint2.bGenerateOverlapEvents | False |
| Float:InfectionPoint3.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint3.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint3.bGenerateOverlapEvents | False |
| Float:InfectionPoint4.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint4.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint4.bGenerateOverlapEvents | False |
| Float:InfectionPoint5.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint5.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint5.bGenerateOverlapEvents | False |
| Float:InfectionPoint6.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint6.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint6.bGenerateOverlapEvents | False |
| Float:InfectionPoint7.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint7.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint7.bGenerateOverlapEvents | False |
| Float:InfectionPoint8.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint8.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint8.bGenerateOverlapEvents | False |
| Float:InfectionPoint9.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint9.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint9.bGenerateOverlapEvents | False |
| Float:Wobble_Template.TimelineLength | 1.0 |

## ED_Spider_Exploder_Rockpox_Plague

| Control | Default Value |
| -------- | ------- |
| Float:ArmorHealthDamage.RadialSocketDamageMultiplier | 0.1 |
| Bool:ArmorHealthDamage.AffectedByAmorBreak | False |
| Float:Damage.RadialDamage | 20.0 |
| Float:Damage.DamageRadius | 300.0 |
| Int:InfectionMaster.InfectionPoints | 2 |
| Float:InfectionMaster.SpikeScale | 0.8 |
| Float:InfectionMaster.InfectionScale | 1.1 |
| Bool:InfectionMaster.KillWhenAllPointsDestroyed | True |
| Float:InfectionPoint1.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint1.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint1.bGenerateOverlapEvents | False |
| Float:InfectionPoint2.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint2.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint2.bGenerateOverlapEvents | False |
| Float:InfectionPoint3.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint3.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint3.bGenerateOverlapEvents | False |
| Float:InfectionPoint4.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint4.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint4.bGenerateOverlapEvents | False |
| Float:InfectionPoint5.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint5.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint5.bGenerateOverlapEvents | False |
| Float:InfectionPoint6.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint6.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint6.bGenerateOverlapEvents | False |
| Float:InfectionPoint7.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint7.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint7.bGenerateOverlapEvents | False |
| Float:InfectionPoint8.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint8.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint8.bGenerateOverlapEvents | False |
| Float:InfectionPoint9.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint9.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint9.bGenerateOverlapEvents | False |

## ED_PlagueLarva

| Control | Default Value |
| -------- | ------- |
| Float:AllowedInFormationChance | 0.0 |
| Float:NetUpdateFrequency | 20.0 |
| Float:MeleeAttack.MaxRange | 250.0 |
| Float:P_Larva_Move_Spray.LDMaxDrawDistance | 5000.0 |
| Float:P_Larva_Move_Spray.CachedMaxDrawDistance | 5000.0 |
| Float:DropShadow.CachedMaxDrawDistance | 2300.0 |
| Bool:DropShadow.bGenerateOverlapEvents | False |
| Bool:DropShadow.bUseAttachParentBound | True |

## ED_PlagueShark

| Control | Default Value |
| -------- | ------- |
| Float:LaunchPower | 1000.0 |
| Float:UpsideDownTime | 4.0 |
| Float:TiltOutSpeed | 300.0 |
| Float:SafeTimeAfterVounerable | 2.0 |
| Float:RaiseHeight | 40.0 |
| Float:AttackDuration | 3.0 |
| Float:ChanceToGrab | 0.0 |
| Float:ChanceForJump | 0.5 |
| Float:MinJumpCooldown | 1.0 |
| Float:MaxJumpCooldown | 3.0 |
| Float:JumpForce | 750.0 |
| Float:MinCirclingTime | 4.0 |
| Float:MaxCirclingTime | 8.0 |
| Float:StaggerDurationMultiplier | 0.0 |
| Bool:CanFlee | False |
| Bool:AttackSound.bAutoActivate | False |
| Bool:DiveSound.bEnableLowPassFilter | True |
| Float:DiveSound.LowPassFilterFrequency | 1000.0 |
| Bool:DiveSound.bAutoActivate | False |
| Bool:VulnerableSound.bAutoActivate | False |
| Float:ProjectileCollision.CapsuleHalfHeight | 227.3429 |
| Float:ProjectileCollision.CapsuleRadius | 75.422165 |
| Float:Outline.CustomLaserPointDuration | 2.0 |
| Float:VulnerableParticles.LDMaxDrawDistance | 10000.0 |
| Float:VulnerableParticles.CachedMaxDrawDistance | 10000.0 |
| Bool:VulnerableParticles.bAutoActivate | False |

## ED_Spider_Shooter_Rockpox_Plague

| Control | Default Value |
| -------- | ------- |
| Float:DeathDuration | 20.0 |
| Float:MeshScale | 0.75 |
| Bool:LimitRagdollSpeed | True |
| Bool:FrozenPauseLogic | True |
| Float:AttackerRadius | 50.0 |
| Float:NetUpdateFrequency | 45.0 |
| Float:ArmorHealthDamage.RadialSocketDamageMultiplier | 0.1 |
| Bool:ArmorHealthDamage.AffectedByAmorBreak | False |
| Bool:GlyphidPraetorianIdle_Cue.bAutoActivate | False |
| Float:InfectionMaster.SpikeScale | 0.8 |
| Float:InfectionMaster.InfectionScale | 0.65 |
| Bool:InfectionMaster.KillWhenAllPointsDestroyed | True |
| Float:PawnSensing.SightRadius | 2000.0 |
| Float:Sphere.SphereRadius | 100.0 |
| Float:InfectionPoint1.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint1.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint1.bGenerateOverlapEvents | False |
| Float:InfectionPoint2.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint2.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint2.bGenerateOverlapEvents | False |
| Float:InfectionPoint3.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint3.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint3.bGenerateOverlapEvents | False |
| Float:InfectionPoint5.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint5.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint5.bGenerateOverlapEvents | False |
| Float:InfectionPoint6.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint6.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint6.bGenerateOverlapEvents | False |
| Float:InfectionPoint7.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint7.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint7.bGenerateOverlapEvents | False |
| Float:InfectionPoint8.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint8.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint8.bGenerateOverlapEvents | False |
| Float:InfectionPoint9.LDMaxDrawDistance | 4000.0 |
| Float:InfectionPoint9.CachedMaxDrawDistance | 4000.0 |
| Bool:InfectionPoint9.bGenerateOverlapEvents | False |

## ED_WalkingPlagueheart

| Control | Default Value |
| -------- | ------- |
| Float:SlimeTrailBarfCooldown | 4.0 |
| Float:StopFightingDistance | 4500.0 |
| Float:ResumeFightingDistance | 2500.0 |
| Int:WeakspotCount | 3 |
| Float:RagdollImpulseSpeed | 0.0 |
| Bool:RagdolEnabled | False |
| Float:DeathDuration | 20.0 |
| Float:StaggerDurationMultiplier | 0.0 |
| Bool:FrozenPauseLogic | True |
| Float:AttackerRadius | 40.0 |
| Bool:bNetLoadOnClient | False |
| Bool:ArmorHealthDamage.AffectedByAmorBreak | False |
| Bool:KnockBackRotation1.bVisible | False |
| Bool:KnockBackRotation2.bVisible | False |
| Bool:KnockBackRotation3.bVisible | False |
| Float:BodyRotationManager.LerpSpeed | 0.3 |
| Float:Capsule1.CapsuleHalfHeight | 300.0 |
| Float:Capsule1.CapsuleRadius | 160.0 |
| Bool:Capsule1.bGenerateOverlapEvents | False |
| Float:Capsule.CapsuleHalfHeight | 180.0 |
| Float:Capsule.CapsuleRadius | 87.0 |
| Bool:Capsule.bGenerateOverlapEvents | False |
| Bool:TentacleMove.bAutoActivate | False |
| Bool:SpawnCleaningPodUsable.Usable | True |
| Int:LineSpikeAttack.SequenceLoops | 3 |
| Float:LineSpikeAttack.firstSpikeDelay | 0.45 |
| Float:LineSpikeAttack.firstSpikeExtraDistance | 400.0 |
| Float:LineSpikeAttack.MaxDistanceToGround | 2000.0 |
| Float:LineSpikeAttack.DistanceBetweenSpikes | 300.0 |
| Float:LineSpikeAttack.TimeBetweenSpikes | 0.2 |
| Int:LineSpikeAttack.MinSpikeCount | 14 |
| Bool:MeleeAttack.CenterOnTarget | False |
| Float:NiagTrailParticle.LDMaxDrawDistance | 12000.0 |
| Float:NiagTrailParticle.CachedMaxDrawDistance | 12000.0 |
| Float:NS_MobilePlague_GroundEffect.LDMaxDrawDistance | 10000.0 |
| Float:NS_MobilePlague_GroundEffect.CachedMaxDrawDistance | 10000.0 |
| Float:NS_MobilePlague_Tendrils.LDMaxDrawDistance | 12000.0 |
| Float:NS_MobilePlague_Tendrils.CachedMaxDrawDistance | 12000.0 |
| Bool:NS_MobilePlague_Tendrils.CastShadow | True |
| Float:PawnSensing.SightRadius | 0.0 |
| Bool:PawnSensing.bEnableSensingUpdates | False |
| Bool:PawnSensing.bSeePawns | False |
| Float:PawnSensing.PeripheralVisionAngle | 0.0 |
| Bool:PointLight10.bUseInverseSquaredFalloff | False |
| Float:PointLight10.AttenuationRadius | 80.0 |
| Float:PointLight10.MaxDrawDistance | 7000.0 |
| Float:PointLight10.Intensity | 150.0 |
| Bool:PointLight10.CastShadows | False |
| Bool:PointLight10.bVisible | False |
| Bool:PointLight10.bUseAttachParentBound | True |
| Bool:PointLight11.bUseInverseSquaredFalloff | False |
| Float:PointLight11.AttenuationRadius | 80.0 |
| Float:PointLight11.MaxDrawDistance | 7000.0 |
| Float:PointLight11.Intensity | 150.0 |
| Bool:PointLight11.CastShadows | False |
| Bool:PointLight11.bVisible | False |
| Bool:PointLight11.bUseAttachParentBound | True |
| Bool:PointLight6.bUseInverseSquaredFalloff | False |
| Float:PointLight6.AttenuationRadius | 80.0 |
| Float:PointLight6.MaxDrawDistance | 7000.0 |
| Float:PointLight6.Intensity | 150.0 |
| Bool:PointLight6.CastShadows | False |
| Bool:PointLight6.bVisible | False |
| Bool:PointLight6.bUseAttachParentBound | True |
| Bool:PointLight7.bUseInverseSquaredFalloff | False |
| Float:PointLight7.AttenuationRadius | 80.0 |
| Float:PointLight7.MaxDrawDistance | 7000.0 |
| Float:PointLight7.Intensity | 150.0 |
| Bool:PointLight7.CastShadows | False |
| Bool:PointLight7.bVisible | False |
| Bool:PointLight7.bUseAttachParentBound | True |
| Bool:PointLight8.bUseInverseSquaredFalloff | False |
| Float:PointLight8.AttenuationRadius | 80.0 |
| Float:PointLight8.MaxDrawDistance | 7000.0 |
| Float:PointLight8.Intensity | 150.0 |
| Bool:PointLight8.CastShadows | False |
| Bool:PointLight8.bVisible | False |
| Bool:PointLight8.bUseAttachParentBound | True |
| Bool:PointLight9.bUseInverseSquaredFalloff | False |
| Float:PointLight9.AttenuationRadius | 80.0 |
| Float:PointLight9.MaxDrawDistance | 7000.0 |
| Float:PointLight9.Intensity | 150.0 |
| Bool:PointLight9.CastShadows | False |
| Bool:PointLight9.bVisible | False |
| Bool:PointLight9.bUseAttachParentBound | True |
| Float:PointLight.AttenuationRadius | 800.0 |
| Float:PointLight.MaxDrawDistance | 15000.0 |
| Float:PointLight.Intensity | 2.0 |
| Bool:PointLight.CastShadows | False |
| Float:Head_A.LDMaxDrawDistance | 10000.0 |
| Float:Head_A.CachedMaxDrawDistance | 10000.0 |
| Float:Head_B.LDMaxDrawDistance | 10000.0 |
| Float:Head_B.CachedMaxDrawDistance | 10000.0 |
| Float:Head_C.LDMaxDrawDistance | 10000.0 |
| Float:Head_C.CachedMaxDrawDistance | 10000.0 |
| Bool:plagueheart1.bRenderStatic | True |
| Float:plagueheart1.LDMaxDrawDistance | 7000.0 |
| Float:plagueheart1.CachedMaxDrawDistance | 7000.0 |
| Bool:plagueheart2.bRenderStatic | True |
| Float:plagueheart2.LDMaxDrawDistance | 7000.0 |
| Float:plagueheart2.CachedMaxDrawDistance | 7000.0 |
| Bool:plagueheart3.bRenderStatic | True |
| Float:plagueheart3.LDMaxDrawDistance | 7000.0 |
| Float:plagueheart3.CachedMaxDrawDistance | 7000.0 |
| Float:SpawnActorWithDebrisPos.MinDistanceBetweenSpwans | 200.0 |
| Bool:SpawnActorWithDebrisPos.AddTerrainPlacementBlockers | False |
| Float:ProximityInfectionSphereTrigger.SphereRadius | 260.0 |
| Float:Sphere.SphereRadius | 100.0 |
| Bool:Sphere.bGenerateOverlapEvents | False |
| Float:UsableSphere.SphereRadius | 320.0 |
| Float:InnerPoint_A1.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_A1.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_A1.bGenerateOverlapEvents | False |
| Bool:InnerPoint_A1.bVisible | False |
| Bool:InnerPoint_A1.bUseAttachParentBound | True |
| Float:InnerPoint_A2.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_A2.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_A2.bGenerateOverlapEvents | False |
| Bool:InnerPoint_A2.bVisible | False |
| Bool:InnerPoint_A2.bUseAttachParentBound | True |
| Float:InnerPoint_A3.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_A3.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_A3.bGenerateOverlapEvents | False |
| Bool:InnerPoint_A3.bVisible | False |
| Bool:InnerPoint_A3.bUseAttachParentBound | True |
| Float:InnerPoint_A4.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_A4.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_A4.bGenerateOverlapEvents | False |
| Bool:InnerPoint_A4.bVisible | False |
| Bool:InnerPoint_A4.bUseAttachParentBound | True |
| Float:InnerPoint_A5.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_A5.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_A5.bGenerateOverlapEvents | False |
| Bool:InnerPoint_A5.bVisible | False |
| Bool:InnerPoint_A5.bUseAttachParentBound | True |
| Float:InnerPoint_B1.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_B1.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_B1.bGenerateOverlapEvents | False |
| Bool:InnerPoint_B1.bVisible | False |
| Bool:InnerPoint_B1.bUseAttachParentBound | True |
| Float:InnerPoint_B2.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_B2.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_B2.bGenerateOverlapEvents | False |
| Bool:InnerPoint_B2.bVisible | False |
| Bool:InnerPoint_B2.bUseAttachParentBound | True |
| Float:InnerPoint_B3.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_B3.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_B3.bGenerateOverlapEvents | False |
| Bool:InnerPoint_B3.bVisible | False |
| Bool:InnerPoint_B3.bUseAttachParentBound | True |
| Float:InnerPoint_B4.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_B4.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_B4.bGenerateOverlapEvents | False |
| Bool:InnerPoint_B4.bVisible | False |
| Bool:InnerPoint_B4.bUseAttachParentBound | True |
| Float:InnerPoint_B5.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_B5.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_B5.bGenerateOverlapEvents | False |
| Bool:InnerPoint_B5.bVisible | False |
| Bool:InnerPoint_B5.bUseAttachParentBound | True |
| Float:InnerPoint_C1.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_C1.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_C1.bGenerateOverlapEvents | False |
| Bool:InnerPoint_C1.bVisible | False |
| Bool:InnerPoint_C1.bUseAttachParentBound | True |
| Float:InnerPoint_C2.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_C2.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_C2.bGenerateOverlapEvents | False |
| Bool:InnerPoint_C2.bVisible | False |
| Bool:InnerPoint_C2.bUseAttachParentBound | True |
| Float:InnerPoint_C3.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_C3.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_C3.bGenerateOverlapEvents | False |
| Bool:InnerPoint_C3.bVisible | False |
| Bool:InnerPoint_C3.bUseAttachParentBound | True |
| Float:InnerPoint_C4.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_C4.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_C4.bGenerateOverlapEvents | False |
| Bool:InnerPoint_C4.bVisible | False |
| Bool:InnerPoint_C4.bUseAttachParentBound | True |
| Float:InnerPoint_C5.LDMaxDrawDistance | 5000.0 |
| Float:InnerPoint_C5.CachedMaxDrawDistance | 5000.0 |
| Bool:InnerPoint_C5.bGenerateOverlapEvents | False |
| Bool:InnerPoint_C5.bVisible | False |
| Bool:InnerPoint_C5.bUseAttachParentBound | True |
| Float:IdleAudioManager.FadeInTime | 0.3 |
| Float:IdleAudioManager.FadeOutTime | 0.3 |
| Float:TerrainScannerStaticMesh.MinDrawDistance | 1000.0 |
| Float:TerrainScannerStaticMesh.CachedMaxDrawDistance | 1.0 |
| Bool:TerrainScannerStaticMesh.bApplyImpulseOnDamage | False |
| Bool:TerrainScannerStaticMesh.bHiddenInGame | True |
| Bool:TerrainScannerStaticMesh.bUseAttachParentBound | True |
| Bool:WeakpointGlow.AddFirstChannelAutomatically | False |

## ED_PatrolBot

| Control | Default Value |
| -------- | ------- |
| Float:HackedRegainModifier | 0.33 |
| Float:HackChance | 25.0 |
| Float:MaxMotionSoundVelThresholdFlying | 600.0 |
| Float:MaxMotionSoundVelThreshold | 500.0 |
| Float:MaxTurningMotionSoundVelThreshold | 30.0 |
| Float:DelayAfterLockOn | 1.25 |
| Float:LaunchPower | 200.0 |
| Float:SpawnRocketsTime | 3.0 |
| Float:MinTurretAngle | -40.0 |
| Float:MaxTurretAngle | 90.0 |
| Float:SpawnRocketsChance | 0.3 |
| Float:GunRange | 2500.0 |
| Float:RollingAttackCooldown | 1.5 |
| Float:FlyingAttackCooldown | 3.5 |
| Float:TurretLerpSpeed | 8.0 |
| Float:AimDownwardsOffset | 5.0 |
| Float:AccelerationThreshold | 1.0 |
| Float:LowSpeedThreshold | 10.0 |
| Bool:CanJump | True |
| Float:JumpForce | 1000.0 |
| Float:MinRollingTime | 4.0 |
| Float:MaxRollingTime | 6.0 |
| Float:MinFlyingTime | 4.0 |
| Float:MaxFlyingTime | 10.0 |
| Float:StaggerDurationMultiplier | 0.0 |
| Float:AllowedInFormationChance | -1.0 |
| Bool:CanFlee | False |
| Float:ProjectileCollision.CapsuleHalfHeight | 70.0 |
| Float:ProjectileCollision.CapsuleRadius | 45.0 |
| Float:JetParticles1.LDMaxDrawDistance | 5000.0 |
| Float:JetParticles1.CachedMaxDrawDistance | 5000.0 |
| Float:JetParticles2.LDMaxDrawDistance | 5000.0 |
| Float:JetParticles2.CachedMaxDrawDistance | 5000.0 |
| Float:JetParticles3.LDMaxDrawDistance | 5000.0 |
| Float:JetParticles3.CachedMaxDrawDistance | 5000.0 |
| Float:JetParticles.LDMaxDrawDistance | 5000.0 |
| Float:JetParticles.CachedMaxDrawDistance | 5000.0 |
| Float:SpawnParticles.LDMaxDrawDistance | 5000.0 |
| Float:SpawnParticles.CachedMaxDrawDistance | 5000.0 |
| Float:Trail1.LDMaxDrawDistance | 4500.0 |
| Float:Trail1.CachedMaxDrawDistance | 4500.0 |
| Float:PointLight.AttenuationRadius | 500.0 |
| Float:PointLight.Intensity | 0.0 |
| Bool:PointLight.CastShadows | False |
| Float:PointLight_HeadGlow.AttenuationRadius | 250.0 |
| Float:PointLight_HeadGlow.Intensity | 10000.0 |
| Bool:PointLight_HeadGlow.CastShadows | False |
| Bool:HackUsable.CoopUse | False |
| Bool:HackUsable.TurnOffAfterUse | True |
| Float:HackUsable.UseDuration | 1.0 |
| Bool:HackUsable.ResetOnFail | True |
| Float:HackUse.SphereRadius | 70.0 |
| Bool:HackUse.bGenerateOverlapEvents | False |
| Int:WeakpointGlow.ReplaceMatIndex | 4 |

## ED_PatrolBot_Caretaker

| Control | Default Value |
| -------- | ------- |
| Float:HackChance | 0.05 |

## ED_Shredder

| Control | Default Value |
| -------- | ------- |
| Bool:Enemy.bIsPingableByLaserpointer | True |

## ED_Terminator

| Control | Default Value |
| -------- | ------- |
| Float:ArmorHP | 150.0 |
| Int:NumPhaseBombs | 30 |
| Float:MaxEyeIntensity | 9492.1875 |
| Float:MaxEyeRadius | 75.0 |
| Float:ShieldBarrierSpawnDelay | 1.2 |
| Float:ShieldBarrierCooldown | 5.0 |
| Float:MinFlairAnimCooldown | 10.0 |
| Float:MaxFlairAnimationCooldown | 20.0 |
| Float:StaggerDurationMultiplier | 0.0 |
| Bool:CanFlee | False |
| Bool:bCollideWhenPlacing | False |
| Bool:bGenerateOverlapEventsDuringLevelStreaming | False |
| Float:NetUpdateFrequency | 30.0 |
| Float:NetPriority | 1.0 |
| Bool:AlignEnemy.IncludePitch | True |
| Bool:TerminatorDeath_Cue.bAutoActivate | False |
| Float:Capsule.CapsuleHalfHeight | 120.0 |
| Float:Capsule.CapsuleRadius | 120.0 |
| Bool:AoEDamage.UseAreaOfEffect | True |
| Float:AoEDamage.RadialDamage | 100.0 |
| Float:AoEDamage.DamageRadius | 600.0 |
| Float:AoEDamage.MaxDamageRadius | 600.0 |
| Bool:CarveAttack.CenterOnTarget | False |
| Float:PawnSensing.SightRadius | 4000.0 |
| Bool:PawnSensing.bHearNoises | False |
| Float:PointLight.AttenuationRadius | 100.0 |
| Float:PointLight.Intensity | 0.0 |
| Bool:PointLight.CastShadows | False |
| Float:AoERange.SphereRadius | 600.0 |
| Float:TerminatorShout.MaxRadius | 200.0 |
| Float:TerminatorShout.MaxIntensity | 15000.0 |
| Bool:TerminatorShout.bReplicates | True |
| Float:TerrainScannerStaticMesh_TEMP_ForTEsting.CachedMaxDrawDistance | 1.0 |
| Bool:TerrainScannerStaticMesh_TEMP_ForTEsting.bVisible | False |
| Bool:TerrainScannerStaticMesh_TEMP_ForTEsting.bHiddenInGame | True |
| Float:Fade_Template.TimelineLength | 0.2 |
| Float:Flutter_Template.TimelineLength | 0.12 |
| Bool:Flutter_Template.bLoop | True |
| Bool:WeakpointGlow.AddFirstChannelAutomatically | False |

## ED_Shark

| Control | Default Value |
| -------- | ------- |
| Float:LaunchPower | 1000.0 |
| Float:UpsideDownTime | 4.0 |
| Float:TiltOutSpeed | 300.0 |
| Float:SafeTimeAfterVounerable | 2.0 |
| Float:RaiseHeight | 40.0 |
| Float:AttackDuration | 6.0 |
| Float:ChanceForJump | 0.4 |
| Float:MinJumpCooldown | 4.0 |
| Float:MaxJumpCooldown | 5.0 |
| Float:JumpForce | 1500.0 |
| Float:MinCirclingTime | 8.0 |
| Float:MaxCirclingTime | 12.0 |
| Float:MaxInGroundTime | 10.0 |
| Float:MinInGroundTime | 12.0 |
| Float:StartParticleTime | 3.0 |
| Float:EndParticleTime | 1.5 |
| Float:StaggerDurationMultiplier | 0.0 |
| Bool:CanFlee | False |
| Bool:AttackSound.bAutoActivate | False |
| Bool:DiveSound.bEnableLowPassFilter | True |
| Float:DiveSound.LowPassFilterFrequency | 1000.0 |
| Bool:DiveSound.bAutoActivate | False |
| Bool:VulnerableSound.bAutoActivate | False |
| Float:ProjectileCollision.CapsuleHalfHeight | 227.3429 |
| Float:ProjectileCollision.CapsuleRadius | 75.422165 |
| Float:Outline.CustomLaserPointDuration | 2.0 |
| Float:VulnerableParticles.LDMaxDrawDistance | 10000.0 |
| Float:VulnerableParticles.CachedMaxDrawDistance | 10000.0 |

## ED_ShootingPlant

| Control | Default Value |
| -------- | ------- |
| Float:BaseEyeHeight | 300.0 |
| Bool:bReplicateMovement | False |
| Float:NetUpdateFrequency | 15.0 |
| Float:NetPriority | 2.0 |
| Float:EnemyLineOfSight.LoSInterval | 1.0 |
| Float:EnemyLineOfSight.LoSIntervalVariance | 0.0 |
| Float:PawnSensing.SightRadius | 2000.0 |
| Bool:PawnSensing.bHearNoises | False |
| Float:PawnSensing.PeripheralVisionAngle | 180.0 |
| Float:PointLight.AttenuationRadius | 200.0 |
| Float:PointLight.Intensity | 300.0 |
| Bool:PointLight.CastShadows | False |
| Float:ProjectileAttack.MaxRange | 0.0 |
| Bool:SkeletalMesh.bDeferKinematicBoneUpdate | True |
| Bool:SkeletalMesh.bEnableUpdateRateOptimizations | True |
| Float:SkeletalMesh.LDMaxDrawDistance | 15000.0 |
| Float:SkeletalMesh.CachedMaxDrawDistance | 15000.0 |
| Bool:SkeletalMesh.bReceivesDecals | False |
| Int:WeakpointGlow.ReplaceMatIndex | 1 |

## ED_Spider_Buffer

| Control | Default Value |
| -------- | ------- |
| Float:DeathDuration | 20.0 |
| Bool:LimitRagdollSpeed | True |
| Float:MaxRagdollSpeed | 500.0 |
| Float:AttackerRadius | 40.0 |
| Bool:BuffingLoop.bAutoActivate | False |
| Float:Capsule1.CapsuleHalfHeight | 40.0 |
| Float:Capsule1.CapsuleRadius | 40.0 |
| Float:Capsule.CapsuleHalfHeight | 80.0 |
| Float:Capsule.CapsuleRadius | 80.0 |
| Float:EnemyBuffer.ParticleTangentSize | 40.0 |
| Float:EnemyBuffer.BuffRadius | 900.0 |
| Float:PawnSensing.SightRadius | 1500.0 |
| Bool:PointLight.bUseInverseSquaredFalloff | False |
| Float:PointLight.AttenuationRadius | 400.0 |
| Float:PointLight.MaxDrawDistance | 15000.0 |
| Float:PointLight.Intensity | 20.0 |
| Bool:PointLight.CastShadows | False |
| Float:SimpleArmorDamage.ArmorStrength | 15.0 |
| Int:WeakpointGlow.ReplaceMatIndex | 3 |

## ED_Spider_Charger

| Control | Default Value |
| -------- | ------- |
| Float:RagdollImpulseSpeed | 1000.0 |
| Float:DeathDuration | 20.0 |
| Float:MeshScale | 1.2 |
| Float:AttackerRadius | 100.0 |
| Float:NetUpdateFrequency | 45.0 |
| Float:Capsule1.CapsuleHalfHeight | 623.11 |
| Float:Capsule1.CapsuleRadius | 160.0 |
| Float:Capsule.CapsuleHalfHeight | 120.0 |
| Float:Capsule.CapsuleRadius | 120.0 |
| Float:Light_BackBody.Intensity | 6000.0 |
| Bool:Light_BackBody.CastShadows | False |
| Bool:Light_BackBody.CastStaticShadows | False |
| Bool:Light_BackBody.CastDynamicShadows | False |

## ED_Spider_Exploder

| Control | Default Value |
| -------- | ------- |
| Bool:ExplodeOnDeath | True |
| Bool:NearbyExplodersFlee | True |
| Float:DeathDuration | 20.0 |
| Float:MeshScale | 0.8 |
| Bool:GlyphidPraetorianIdle_Cue.bAutoActivate | False |
| Bool:Damage.UseAreaOfEffect | True |
| Float:Damage.RadialDamage | 50.0 |
| Float:Damage.DamageRadius | 350.0 |
| Float:Damage.MaxDamageRadius | 150.0 |
| Float:PawnSensing.SightRadius | 2000.0 |
| Bool:Light_BackBody.bUseInverseSquaredFalloff | False |
| Float:Light_BackBody.AttenuationRadius | 500.0 |
| Float:Light_BackBody.MaxDrawDistance | 15000.0 |
| Float:Light_BackBody.MaxDistanceFadeRange | 1000.0 |
| Float:Light_BackBody.Intensity | 3.0 |
| Bool:Light_BackBody.CastShadows | False |
| Bool:Light_BackBody.CastStaticShadows | False |
| Bool:Light_BackBody.CastDynamicShadows | False |

## ED_Spider_Exploder_Warning

| Control | Default Value |
| -------- | ------- |

## ED_Spider_ExploderTank

| Control | Default Value |
| -------- | ------- |
| Float:WeakspotDamageMult | 5.0 |
| Int:NumClusterBombs | 8 |
| Float:PushForce | 1000.0 |
| Float:BurnThickness | 20.0 |
| Float:CarveDiameter | 1600.0 |
| Float:DeathDuration | 20.0 |
| Float:MeshScale | 1.2 |
| Bool:ApplyDifficultySpeedModifier | False |
| Float:StaggerDurationMultiplier | 0.0 |
| Float:NetUpdateFrequency | 45.0 |
| Bool:ArmorHealthDamage.AffectedByAmorBreak | False |
| Bool:GlyphidPraetorianIdle_Cue.bAutoActivate | False |
| Float:Capsule.CapsuleHalfHeight | 120.0 |
| Float:Capsule.CapsuleRadius | 120.0 |
| Float:Damage.Damage | 0.0 |
| Float:Damage.FriendlyFireModifier | 2.0 |
| Bool:Damage.UseAreaOfEffect | True |
| Float:Damage.RadialDamage | 80.0 |
| Float:Damage.MinDamagePct | 0.1 |
| Float:Damage.DamageRadius | 800.0 |
| Float:Damage.MaxDamageRadius | 250.0 |
| Bool:DamageDeathExplosion.UseAreaOfEffect | True |
| Float:DamageDeathExplosion.RadialDamage | 20000.0 |
| Float:DamageDeathExplosion.MinDamagePct | 0.001 |
| Float:DamageDeathExplosion.DamageRadius | 800.0 |
| Float:DamageDeathExplosion.MaxDamageRadius | 400.0 |
| Bool:Growl.bAutoActivate | False |
| Bool:CarveAttack.CenterOnTarget | False |
| Bool:P_ExploderTank_CollectingEmbers.bAutoActivate | False |
| Float:PawnSensing.SightRadius | 1500.0 |
| Bool:Light_BackBody.bUseInverseSquaredFalloff | False |
| Float:Light_BackBody.AttenuationRadius | 500.0 |
| Float:Light_BackBody.MaxDrawDistance | 15000.0 |
| Float:Light_BackBody.MaxDistanceFadeRange | 1000.0 |
| Float:Light_BackBody.Intensity | 3.0 |
| Bool:Light_BackBody.CastShadows | False |
| Bool:Light_BackBody.CastStaticShadows | False |
| Bool:Light_BackBody.CastDynamicShadows | False |
| Int:WeakpointGlow.ReplaceMatIndex | 3 |

## ED_Spider_ExploderTankGhost

| Control | Default Value |
| -------- | ------- |
| Float:Damage.FriendlyFireModifier | 0.25 |
| Float:Damage.RadialDamage | 200.0 |
| Float:TerrainScannerMesh.MinDrawDistance | 1000.0 |
| Float:TerrainScannerMesh.CachedMaxDrawDistance | 500.0 |
| Bool:TerrainScannerMesh.bGenerateOverlapEvents | False |
| Bool:TerrainScannerMesh.bAllowCullDistanceVolume | False |
| Bool:TerrainScannerMesh.bVisibleInReflectionCaptures | False |
| Bool:TerrainScannerMesh.bReceivesDecals | False |
| Bool:TerrainScannerMesh.bUseAsOccluder | False |
| Bool:TerrainScannerMesh.CastShadow | False |
| Bool:TerrainScannerMesh.bUseAttachParentBound | True |

## ED_Spider_ExploderTank_King

| Control | Default Value |
| -------- | ------- |
| Float:BurnThickness | 25.0 |
| Float:CarveDiameter | 1300.0 |
| Bool:Light_BackBody1.bUseInverseSquaredFalloff | False |
| Float:Light_BackBody1.LightFalloffExponent | 10.0 |
| Float:Light_BackBody1.AttenuationRadius | 350.0 |
| Float:Light_BackBody1.MaxDrawDistance | 15000.0 |
| Float:Light_BackBody1.MaxDistanceFadeRange | 1000.0 |
| Float:Light_BackBody1.Intensity | 70.0 |
| Bool:Light_BackBody1.CastShadows | False |
| Bool:Light_BackBody1.CastStaticShadows | False |
| Bool:Light_BackBody1.CastDynamicShadows | False |
| Bool:Light_BackBody2.bUseInverseSquaredFalloff | False |
| Float:Light_BackBody2.AttenuationRadius | 350.0 |
| Float:Light_BackBody2.MaxDrawDistance | 15000.0 |
| Float:Light_BackBody2.MaxDistanceFadeRange | 1000.0 |
| Float:Light_BackBody2.Intensity | 70.0 |
| Bool:Light_BackBody2.CastShadows | False |
| Bool:Light_BackBody2.CastStaticShadows | False |
| Bool:Light_BackBody2.CastDynamicShadows | False |
| Float:Light_BackBody.AttenuationRadius | 1000.0 |

## ED_Spider_Drone

| Control | Default Value |
| -------- | ------- |
| Float:GroundToAir.WalkTime | 10.0 |
| Float:GroundToAir.WalkTimeMaxRandomOffset | -5.0 |
| Float:GroundToAir.WalkTimeMinRandomOffset | 5.0 |
| Float:GroundToAir.FlyTime | 10.0 |
| Float:GroundToAir.FlyTimeMaxRandomOffset | -5.0 |
| Float:GroundToAir.FlyTimeMinRandomOffset | 5.0 |
| Bool:GroundToAir.FlyUseTimer | False |
| Float:PawnSensing.SightRadius | 3000.0 |

## ED_Spider_Grunt

| Control | Default Value |
| -------- | ------- |
| Float:SimpleArmorDamage.ArmorStrength | 15.0 |

## ED_Spider_GruntTutorial

| Control | Default Value |
| -------- | ------- |
| Float:SimpleArmorDamage.ArmorStrength | 15.0 |

## ED_Spider_Grunt_Ice

| Control | Default Value |
| -------- | ------- |

## ED_Spider_Grunt_Mutated

| Control | Default Value |
| -------- | ------- |

## ED_Spider_Grunt_Attacker

| Control | Default Value |
| -------- | ------- |
| Float:MeshScale | 1.2 |
| Float:SimpleArmorDamage.ArmorStrength | 15.0 |

## ED_Spider_Grunt_Guard

| Control | Default Value |
| -------- | ------- |
| Float:MeshScale | 1.0 |
| Float:StaggerImunityWindow | 2.0 |
| Float:InDanger.DamageTimeLimit | 3.0 |
| Float:InDanger.DamageThreshold | 30.0 |
| Bool:InDanger.RunsOnClients | True |

## ED_Spider_Grunt_Rock

| Control | Default Value |
| -------- | ------- |
| Float:StaggerDurationMultiplier | 0.0 |

## ED_Spider_Lobber

| Control | Default Value |
| -------- | ------- |
| Bool:GlyphidPraetorianIdle_Cue.bAutoActivate | True |

## ED_Spider_RapidShooter

| Control | Default Value |
| -------- | ------- |
| Float:DeathDuration | 20.0 |
| Float:MeshScale | 1.2 |
| Bool:LimitRagdollSpeed | True |
| Float:MaxRagdollSpeed | 500.0 |
| Bool:StaggerPauseLogic | True |
| Bool:FrozenPauseLogic | True |
| Float:AttackerRadius | 50.0 |
| Float:NetUpdateFrequency | 45.0 |
| Bool:ArmorHealthDamage.AffectedByAmorBreak | False |
| Float:Capsule.CapsuleHalfHeight | 120.0 |
| Float:Capsule.CapsuleRadius | 90.0 |
| Float:PawnSensing.SightRadius | 2000.0 |
| Bool:PointLight.bUseInverseSquaredFalloff | False |
| Float:PointLight.LightFalloffExponent | 6.0 |
| Float:PointLight.AttenuationRadius | 250.0 |
| Float:PointLight.Intensity | 3.0 |
| Bool:PointLight.CastShadows | False |
| Bool:WeakpointGlow.AddFirstChannelAutomatically | False |

## ED_Spider_Amber_Shooter

| Control | Default Value |
| -------- | ------- |
| Float:PointLight1.AttenuationRadius | 500.0 |
| Bool:PointLight1.CastShadows | False |
| Float:PointLight2.AttenuationRadius | 50.0 |
| Float:PointLight2.Intensity | 500.0 |
| Bool:PointLight2.CastShadows | False |
| Float:PointLight3.AttenuationRadius | 50.0 |
| Float:PointLight3.Intensity | 500.0 |
| Bool:PointLight3.CastShadows | False |
| Bool:Mesh_Infestation01.bGenerateOverlapEvents | False |
| Bool:Mesh_Infestation02.bGenerateOverlapEvents | False |
| Bool:Mesh_Infestation03.bGenerateOverlapEvents | False |

## ED_Spider_Shooter

| Control | Default Value |
| -------- | ------- |

## ED_Spider_Shooter_Ground

| Control | Default Value |
| -------- | ------- |

## ED_Spider_ShooterQueen

| Control | Default Value |
| -------- | ------- |
| Float:DeathDuration | 20.0 |
| Float:MeshScale | 1.2 |
| Bool:FrozenPauseLogic | True |
| Float:AttackerRadius | 50.0 |
| Float:NetUpdateFrequency | 45.0 |
| Float:PawnSensing.SightRadius | 1500.0 |
| Float:SimpleArmorDamage.ArmorStrength | 100.0 |
| Float:Sphere.SphereRadius | 100.0 |

## ED_Spider_Spitter

| Control | Default Value |
| -------- | ------- |
| Float:DeathDuration | 20.0 |
| Bool:LimitRagdollSpeed | True |
| Float:AttackerRadius | 50.0 |
| Float:NetUpdateFrequency | 45.0 |
| Bool:GlyphidPraetorianIdle_Cue.bAutoActivate | False |
| Float:PawnSensing.SightRadius | 2000.0 |
| Float:Sphere.SphereRadius | 100.0 |

## ED_Spider_Stalker

| Control | Default Value |
| -------- | ------- |
| Float:StaggerDurationMultiplier | 0.0 |
| Float:GlyphidPraetorianIdle_Cue.VolumeMultiplier | 1.0 |

## ED_Spider_Stinger

| Control | Default Value |
| -------- | ------- |
| Float:DeathDuration | 20.0 |
| Float:MeshScale | 0.8 |
| Float:StaggerImunityWindow | 2.0 |
| Bool:FrozenPauseLogic | True |
| Bool:GlyphidPraetorianIdle_Cue.bAutoActivate | False |
| Float:Capsule.CapsuleHalfHeight | 159.782 |
| Float:Capsule.CapsuleRadius | 61.56915 |
| Float:PawnSensing.SightRadius | 2500.0 |
| Float:PointLight_Tail.AttenuationRadius | 400.0 |
| Float:PointLight_Tail.MaxDrawDistance | 9000.0 |
| Float:PointLight_Tail.Intensity | 0.0 |
| Bool:PointLight_Tail.CastShadows | False |
| Bool:PointLight_Tail.bVisible | False |
| Bool:PointLight_Weakpoint.bUseInverseSquaredFalloff | False |
| Float:PointLight_Weakpoint.AttenuationRadius | 40.0 |
| Float:PointLight_Weakpoint.MaxDrawDistance | 9000.0 |
| Float:PointLight_Weakpoint.Intensity | 10.0 |
| Bool:PointLight_Weakpoint.CastShadows | False |
| Float:TailEnd.LDMaxDrawDistance | 9000.0 |
| Float:TailEnd.CachedMaxDrawDistance | 9000.0 |
| Float:SplineHookAttack.MaxAngledForce | 1800.0 |
| Float:SplineHookAttack.AdjustmentStartDistance | 100.0 |
| Float:SplineHookAttack.AttackDuration | 0.625 |
| Float:SplineHookAttack.AttackDelay | 1.2 |
| Float:SplineHookAttack.LeadMultiplier | 0.75 |
| Float:SplineHookAttack.AquireLocationTime | 0.9 |
| Float:SplineHookAttack.OnSuccessCooldown | 15.0 |
| Bool:SplineHookAttack.Lead | True |
| Float:Extender.LDMaxDrawDistance | 10000.0 |
| Float:Extender.CachedMaxDrawDistance | 10000.0 |
| Bool:Extender.bGenerateOverlapEvents | False |

## ED_Spider_Swarmer

| Control | Default Value |
| -------- | ------- |
| Float:DeathDuration | 3.0 |
| Float:MeshScale | 0.6 |
| Float:StaggerDurationMultiplier | 0.0 |
| Float:AttackerRadius | 40.0 |
| Float:JumpAttack.MaxSurfaceAngle | 35.0 |
| Float:JumpAttack.MaxRange | 230.0 |
| Float:MeleeAttack.MaxRange | 230.0 |
| Float:PawnSensing.SightRadius | 1500.0 |
| Float:Sphere.SphereRadius | 130.0 |
| Float:DropShadow.CachedMaxDrawDistance | 1300.0 |
| Bool:DropShadow.bGenerateOverlapEvents | False |
| Bool:DropShadow.bUseAttachParentBound | True |

## ED_Spider_Swarmer_Ice

| Control | Default Value |
| -------- | ------- |

## ED_Spider_Swarmer_Mutated

| Control | Default Value |
| -------- | ------- |
| Float:RadiationDistance | 250.0 |
| Float:RadiationCheckDelay | 1.0 |
| Bool:IsRadioactive | True |
| Float:ParticleSystem.CachedMaxDrawDistance | 5000.0 |
| Bool:ParticleSystem.bAutoActivate | False |
| Bool:PointLight.bUseInverseSquaredFalloff | False |
| Float:PointLight.LightFalloffExponent | 2.0 |
| Float:PointLight.AttenuationRadius | 100.0 |
| Float:PointLight.MaxDrawDistance | 15000.0 |
| Float:PointLight.MaxDistanceFadeRange | 1000.0 |
| Float:PointLight.Intensity | 3.0 |
| Bool:PointLight.CastShadows | False |
| Bool:PointLight.CastStaticShadows | False |
| Bool:PointLight.CastDynamicShadows | False |

## ED_Spider_Swarmer_Pheromone_NOFX

| Control | Default Value |
| -------- | ------- |

## ED_Spider_Spawn

| Control | Default Value |
| -------- | ------- |
| Float:PawnSensing.SightRadius | 1000.0 |
| Float:Sphere.SphereRadius | 120.0 |
| Float:Spawn_Template.TimelineLength | 1.0 |

## ED_Spider_Tank

| Control | Default Value |
| -------- | ------- |
| Float:ConeAttack.MaxRange | 500.0 |
| Float:ConeCapsule.CapsuleHalfHeight | 625.0 |
| Float:ConeCapsule.CapsuleRadius | 160.0 |
| Float:Light_BackBody.MaxDrawDistance | 12000.0 |

## ED_Spider_Tank_Ice

| Control | Default Value |
| -------- | ------- |
| Float:RagdollImpulseSpeed | 2000.0 |
| Float:ConeAttack.MaxRange | 500.0 |
| Float:ConeCapsule.CapsuleHalfHeight | 625.0 |
| Float:ConeCapsule.CapsuleRadius | 160.0 |

## ED_Spider_Tank_Mutated

| Control | Default Value |
| -------- | ------- |
| Float:BaseLightIntensity | 10.0 |
| Float:BaseEmissive | 0.5 |
| Float:BaseLightRadius | 650.0 |
| Bool:RadiationSound.bAutoActivate | False |
| Float:RadiationAttack.MaxRange | 500.0 |
| Float:ParticleSystem.LDMaxDrawDistance | 8000.0 |
| Float:ParticleSystem.CachedMaxDrawDistance | 8000.0 |
| Float:Light_BackBody.LightFalloffExponent | 4.0 |
| Float:Light_BackBody.AttenuationRadius | 300.0 |
| Float:Light_BackBody.Intensity | 10.0 |
| Float:Sphere.SphereRadius | 500.0 |
| Float:RadiationSphere.LDMaxDrawDistance | 12000.0 |
| Float:RadiationSphere.CachedMaxDrawDistance | 12000.0 |
| Bool:RadiationSphere.bHiddenInGame | True |
| Float:Radiation_Template.TimelineLength | 2.2 |

## ED_Spider_Tank_Amber

| Control | Default Value |
| -------- | ------- |
| Float:PointLight1.AttenuationRadius | 500.0 |
| Bool:PointLight1.CastShadows | False |
| Float:PointLight2.AttenuationRadius | 50.0 |
| Float:PointLight2.Intensity | 500.0 |
| Bool:PointLight2.CastShadows | False |
| Float:PointLight4.AttenuationRadius | 50.0 |
| Float:PointLight4.Intensity | 500.0 |
| Bool:PointLight4.CastShadows | False |
| Bool:Mesh_Infestation01.bGenerateOverlapEvents | False |
| Bool:Mesh_Infestation02.bGenerateOverlapEvents | False |
| Bool:Mesh_Infestation03.bGenerateOverlapEvents | False |

## ED_Spider_Tank_Rock

| Control | Default Value |
| -------- | ------- |
| Float:StaggerDurationMultiplier | 0.0 |
| Float:StaggerImunityWindow | 0.0 |

## ED_Spider_ShieldTank

| Control | Default Value |
| -------- | ------- |
| Float:MovementSpeedPenaltyReduction | 0.75 |
| Float:StaggerDurationMultiplier | 0.0 |
| Bool:CarveAttack.CenterOnTarget | False |
| Float:GroundSlam.MaxRange | 500.0 |
| Float:MeleeAttack.MaxRange | 300.0 |
| Bool:TremorParticles.bAutoActivate | False |
| Float:TremorAttack.InitialParticlesDelay | 0.3 |
| Float:TremorAttack.TargetMaxDistanceFromGround | 200.0 |
| Float:TremorAttack.LaunchForce | 300.0 |
| Float:TremorAttack.Duration | 4.5 |

## ED_Spider_Boss_Heavy

| Control | Default Value |
| -------- | ------- |
| Float:MeshScale | 1.8 |
| Bool:ApplyDifficultySpeedModifier | False |
| Bool:FrozenPauseLogic | True |
| Float:AttackerRadius | 200.0 |
| Float:Capsule.CapsuleHalfHeight | 170.0 |
| Float:Capsule.CapsuleRadius | 110.0 |
| Float:Weakspot_C.CapsuleHalfHeight | 60.0 |
| Float:Weakspot_C.CapsuleRadius | 30.0 |
| Bool:Weakspot_C.bGenerateOverlapEvents | False |
| Bool:Weakspot_L.bGenerateOverlapEvents | False |
| Bool:Weakspot_R.bGenerateOverlapEvents | False |
| Float:SpecialAttackAoE.Damage | 0.0 |
| Bool:SpecialAttackAoE.UseAreaOfEffect | True |
| Float:SpecialAttackAoE.RadialDamage | 50.0 |
| Float:SpecialAttackAoE.DamageRadius | 500.0 |
| Float:SpecialAttackAoE.MaxDamageRadius | 200.0 |
| Float:WeakspotHealth_C.MaxHealth | 200.0 |
| Float:WeakspotHealth_C.RadialDamageResistance | 0.5 |
| Float:WeakspotHealth_L.MaxHealth | 200.0 |
| Float:WeakspotHealth_L.RadialDamageResistance | 0.5 |
| Float:WeakspotHealth_R.MaxHealth | 200.0 |
| Float:WeakspotHealth_R.RadialDamageResistance | 0.5 |
| Float:HealthDamageTracker.TiggerOnPercentage | 0.4 |
| Bool:IK.Enabled | True |
| Bool:CarveAttack.CenterOnTarget | False |
| Float:MeleeAttack1.MaxRange | 350.0 |
| Float:PawnSensing.SightRadius | 1500.0 |
| Float:ProjectileFireball.MinRange | 400.0 |
| Float:ProjectileFireball.MaxRange | 3500.0 |
| Float:SpecialAttackSpawn.MinDistanceBetweenSpwans | 250.0 |
| Bool:SpecialAttackSpawn.AddTerrainPlacementBlockers | False |
| Bool:WeakpointGlow.AddFirstChannelAutomatically | False |

## ED_Spider_Tank_HeavySpawn

| Control | Default Value |
| -------- | ------- |
| Float:RagdollImpulseSpeed | 1000.0 |
| Float:DissolveDelay | 0.0 |
| Float:DeathDuration | 20.0 |
| Float:MeshScale | 0.95 |
| Bool:ApplyDifficultySpeedModifier | False |
| Bool:LimitRagdollSpeed | True |
| Float:MaxRagdollSpeed | 350.0 |
| Float:StaggerDurationMultiplier | 0.5 |
| Float:StaggerImunityWindow | 2.0 |
| Bool:StaggerPauseLogic | True |
| Bool:FrozenPauseLogic | True |
| Float:AttackerRadius | 100.0 |
| Float:NetUpdateFrequency | 45.0 |
| Float:Capsule.CapsuleHalfHeight | 90.0 |
| Float:Capsule.CapsuleRadius | 90.0 |
| Bool:CarveAttack.CenterOnTarget | False |
| Float:PawnSensing.SightRadius | 1500.0 |

## ED_Spider_Tank_Boss

| Control | Default Value |
| -------- | ------- |
| Bool:TankArmorIntact | True |
| Float:HitGlow | 20.0 |
| Float:BaseGlowFrequency | 1.0 |
| Float:BaseGlowStrength | 200.0 |
| Float:RagdollImpulseSpeed | 1000.0 |
| Float:DeathDuration | 20.0 |
| Float:MeshScale | 1.6 |
| Float:DecalSize | 300.0 |
| Bool:ApplyDifficultySpeedModifier | False |
| Bool:LimitRagdollSpeed | True |
| Float:MaxRagdollSpeed | 350.0 |
| Float:AttackerRadius | 150.0 |
| Float:NetUpdateFrequency | 45.0 |
| Float:NetPriority | 5.0 |
| Float:SlamAttackk.MaxRange | 500.0 |
| Float:Capsule.CapsuleHalfHeight | 150.0 |
| Float:Capsule.CapsuleRadius | 85.0 |
| Float:DestructibleSubHealth.MaxHealth | 1700.0 |
| Bool:DestructibleSubHealth.AllowInderectDamage | True |
| Float:HealthDamageTracker.TiggerOnPercentage | 0.3 |
| Bool:IK.Enabled | True |
| Bool:CarveAttack.CenterOnTarget | False |
| Float:MeleeAttack.MaxRange | 350.0 |
| Float:PawnSensing.SightRadius | 1500.0 |
| Bool:Light_BackBody.CastShadows | False |
| Bool:Light_BackBody.CastStaticShadows | False |
| Bool:Light_BackBody.CastDynamicShadows | False |
| Float:EggProjectile.MinRange | 300.0 |
| Float:EggProjectile.MaxRange | 3500.0 |
| Float:Fireball.MinRange | 300.0 |
| Float:Fireball.MaxRange | 3500.0 |
| Bool:Armor_Back_TankBoss.bGenerateOverlapEvents | False |
| Float:Butt FadeOut_Template.TimelineLength | 1.0 |
| Float:Timeline_0_Template.TimelineLength | 3.5 |

## ED_Spider_Boss_TwinA

| Control | Default Value |
| -------- | ------- |
| Float:BP_Meet_Attack.MaxRange | -1.0 |
| Bool:Projectile_Fireball.ProjectilesIgnoreEachOther | True |
| Bool:Projectile_Mines.ProjectilesIgnoreEachOther | True |
| Float:Projectile_Mines.MaxRange | 0.0 |
| Bool:Projectile_MinesBarrage.ProjectilesIgnoreEachOther | True |
| Float:Projectile_MinesBarrage.MaxRange | 0.0 |

## ED_Spider_Boss_TwinB

| Control | Default Value |
| -------- | ------- |
| Float:BurrowAttack.BurrowDuration | 5.0 |
| Float:BurrowAttack.TargetingDelay | 3.5 |
| Float:BurrowAttack.MaxSurfaceAngle | 45.0 |
| Float:BurrowAttack.MaxRange | 0.0 |
| Float:ConeAttack.MinRange | 100.0 |
| Float:ConeAttack.MaxRange | 700.0 |
| Float:BP_Meet_Attack.MaxRange | -1.0 |
| Float:SpecialAttackCollider.CapsuleHalfHeight | 331.35992 |
| Float:SpecialAttackCollider.CapsuleRadius | 35.11046 |
| Float:EnemyBuffer.BuffRadius | 2000.0 |
| Int:EnemyBuffer.MaxBuffedTargets | 1 |
| Bool:CarveAttack.CenterOnTarget | False |
| Float:ThreeWayAttack.MaxSurfaceAngle | 30.0 |
| Float:ThreeWayAttack.MaxRange | 1000.0 |

## ED_TentaclePlant

| Control | Default Value |
| -------- | ------- |
| Float:MinimumDistance | 2000.0 |
| Float:MinDistanceBetweenNodes | 500.0 |
| Float:BaseEyeHeight | 400.0 |
| Bool:bReplicateMovement | False |
| Float:Capsule.CapsuleHalfHeight | 150.0 |
| Float:Capsule.CapsuleRadius | 150.0 |
| Float:EnemyLineOfSight.LoSInterval | 0.3 |
| Float:EnemyLineOfSight.LoSIntervalVariance | 0.0 |
| Bool:PathfinderCollision.ActivatePFCollisionAtInit | True |
| Float:PawnSensing.SightRadius | 4000.0 |
| Float:PawnSensing.SensingInterval | 0.3 |
| Bool:PawnSensing.bHearNoises | False |
| Float:PawnSensing.PeripheralVisionAngle | 180.0 |
| Bool:PointLight.bUseInverseSquaredFalloff | False |
| Float:PointLight.AttenuationRadius | 750.0 |
| Float:PointLight.MaxDrawDistance | 15000.0 |
| Float:PointLight.Intensity | 0.0 |
| Bool:PointLight.CastShadows | False |
| Float:ProjectileAttack.MaxRange | 0.0 |
| Bool:SkeletalMesh.bDeferKinematicBoneUpdate | True |
| Bool:SkeletalMesh.bEnableUpdateRateOptimizations | True |
| Float:SkeletalMesh.LDMaxDrawDistance | 15000.0 |
| Float:SkeletalMesh.CachedMaxDrawDistance | 15000.0 |
| Bool:SkeletalMesh.bReceivesDecals | False |

## ED_Woodlouse

| Control | Default Value |
| -------- | ------- |
| Float:DecalSize | 150.0 |
| Float:RollingCenterOffsetOnStanding | 55.0 |
| Float:RollingCenterOffsetOnFold | 85.0 |
| Float:BurstTime | 0.45 |
| Float:BurstXOffset | 300.0 |
| Float:BurstYOffset | 300.0 |
| Float:BurstZOffset | 300.0 |
| Bool:InvounerableOnRoll | False |
| Float:ForgetRange | 500.0 |
| Float:ForgetTime | 1.2 |
| Float:RefreshTimeMax | 3.0 |
| Float:RefreshTimeMin | 3.0 |
| Float:BumpPower | 500.0 |
| Float:DirectionalBumpPower | 400.0 |
| Float:FoldedStateMaxTime | 15.0 |
| Float:FoldedStateMinTime | 10.0 |
| Float:UnfoldedStateMaxTime | 10000.0 |
| Float:UnflodedStateMinTime | 10000.0 |
| Float:TimeBetweenBumpingSamePlayer | 1.0 |
| Float:MinBumpDamage | 5.0 |
| Float:MaxBumpDamage | 12.0 |
| Float:BumpDamage | 5.0 |
| Float:MaxBumpPower | 900.0 |
| Float:BumpRange | 200.0 |
| Float:RollSpeedModifier | 0.9 |
| Float:SeeTargetSafetyTime | 12.0 |
| Float:StaggerDurationMultiplier | 0.0 |
| Float:NetUpdateFrequency | 25.0 |
| Float:ParticleSystem.LDMaxDrawDistance | 7500.0 |
| Float:ParticleSystem.CachedMaxDrawDistance | 7500.0 |
| Float:ProjectileHit.SphereRadius | 125.0 |

## ED_Woodlouse_Youngling

| Control | Default Value |
| -------- | ------- |
| Float:RollingCenterOffsetOnStanding | 20.0 |
| Float:RollingCenterOffsetOnFold | 50.0 |
| Float:ChanceToWalk | 0.0 |
| Float:BurstTime | 0.2 |
| Int:BurstCount | 0 |
| Float:BumpPower | 350.0 |
| Float:DirectionalBumpPower | 250.0 |
| Float:MinBumpDamage | 3.5 |
| Float:MaxBumpDamage | 7.0 |
| Float:BumpDamage | 3.5 |

## ED_GreatEggHunt_SpringBunny

| Control | Default Value |
| -------- | ------- |
| Float:RunSpeedMod | 4.0 |
| Float:StaggerDurationMultiplier | 0.0 |
| Bool:BunnyScaredStart.bAutoActivate | False |
| Float:Capsule.CapsuleHalfHeight | 65.0 |
| Float:Capsule.CapsuleRadius | 55.0 |
| Bool:BunnyIdle.bAutoActivate | False |
| Bool:Trail.bVisible | False |
| Bool:Trail.bHiddenInGame | True |
| Float:PawnSensing.SightRadius | 1000.0 |
| Bool:PawnSensing.bHearNoises | False |
| Float:PointLight1.AttenuationRadius | 150.0 |
| Float:PointLight1.Intensity | 300.0 |
| Bool:PointLight1.CastShadows | False |
| Float:DropShadow.CachedMaxDrawDistance | 2300.0 |
| Bool:DropShadow.bGenerateOverlapEvents | False |
| Bool:DropShadow.bUseAttachParentBound | True |

## ED_Halloween_Skull

| Control | Default Value |
| -------- | ------- |
| Float:RunSpeedMod | 7.0 |
| Float:AudioUpdateTime | 0.1 |
| Float:AlertedMovementScale | 140.0 |
| Float:AlertedMovementTimeScale | 0.4 |
| Float:StaggerDurationMultiplier | 0.0 |
| Bool:AudioLoop.bAutoActivate | False |
| Float:PawnSensing.SightRadius | 1000.0 |
| Bool:PawnSensing.bHearNoises | False |
| Bool:PointLight_Far.bUseInverseSquaredFalloff | False |
| Float:PointLight_Far.AttenuationRadius | 600.0 |
| Float:PointLight_Far.Intensity | 10.0 |
| Bool:PointLight_Far.CastShadows | False |
| Bool:PointLight.bUseInverseSquaredFalloff | False |
| Float:PointLight.LightFalloffExponent | 4.0 |
| Float:PointLight.AttenuationRadius | 50.0 |
| Float:PointLight.Intensity | 1000.0 |
| Bool:PointLight.CastShadows | False |
| Float:ColdSphere_Close.SphereRadius | 400.0 |
| Float:ColdSphere_Far.SphereRadius | 800.0 |
| Float:Sphere.SphereRadius | 45.0 |
| Bool:Sphere.bGenerateOverlapEvents | False |
| Bool:Mesh_Flame01.bUseDefaultCollision | True |
| Bool:Mesh_Flame01.bGenerateOverlapEvents | False |
| Bool:Mesh_Flame01.bReceivesDecals | False |

## ED_Nisse

| Control | Default Value |
| -------- | ------- |
| Float:RunSpeedMod | 4.0 |
| Float:StaggerDurationMultiplier | 0.0 |
| Bool:AudioScaredLoop.bAutoActivate | False |
| Float:Capsule.CapsuleHalfHeight | 65.0 |
| Float:Capsule.CapsuleRadius | 55.0 |
| Bool:Trail.bVisible | False |
| Bool:Trail.bHiddenInGame | True |
| Float:PawnSensing.SightRadius | 1000.0 |
| Bool:PawnSensing.bHearNoises | False |
| Float:PointLight.AttenuationRadius | 150.0 |
| Float:PointLight.Intensity | 100.0 |
| Bool:PointLight.CastShadows | False |
| Bool:SK_Moustache_Rig_A_003.bVisible | False |
| Bool:SK_Moustache_Rig_A_003.bHiddenInGame | True |
| Float:DropShadow.CachedMaxDrawDistance | 2300.0 |
| Bool:DropShadow.bGenerateOverlapEvents | False |
| Bool:DropShadow.bUseAttachParentBound | True |

## ED_Spider_Grunt_Rock_Warning

| Control | Default Value |
| -------- | ------- |
| Float:StaggerDurationMultiplier | 0.0 |

## ED_Spider_Tank_Rock_Warning

| Control | Default Value |
| -------- | ------- |
| Float:StaggerDurationMultiplier | 0.0 |
| Float:StaggerImunityWindow | 0.0 |

## ED_FlyingSmartRock

| Control | Default Value |
| -------- | ------- |
| Float:AttackDistance | 300.0 |
| Float:LightRadiusBoost | 500.0 |
| Float:LightIntensityBoost | 100.0 |
| Float:EmissiveBoost | 50000.0 |
| Float:StaggerDurationMultiplier | 0.0 |
| Float:AttackerRadius | 85.0 |
| Float:AllowedInFormationChance | 0.0 |
| Bool:CanFlee | False |
| Float:NetUpdateFrequency | 10.0 |
| Float:NetPriority | 2.0 |
| Bool:PrepareToAttack_Cue.bAutoActivate | False |
| Float:Damage.Damage | 20.0 |
| Float:Trail.LDMaxDrawDistance | 4500.0 |
| Float:Trail.CachedMaxDrawDistance | 4500.0 |
| Bool:PointLight.bUseInverseSquaredFalloff | False |
| Float:PointLight.AttenuationRadius | 500.0 |
| Float:PointLight.Intensity | 100.0 |
| Bool:PointLight.CastShadows | False |
| Float:Sphere.SphereRadius | 160.0 |
| Bool:Core.bGenerateOverlapEvents | False |
| Bool:Core.bVisible | False |
| Bool:Core.bHiddenInGame | True |
| Float:AttackTell_Template.TimelineLength | 2.25 |
| Float:Timeline_1_Template.TimelineLength | 1.5 |

## ED_FacilityTurret_Barrier

| Control | Default Value |
| -------- | ------- |
| Int:Attacks | 1 |
| Float:TurnCooldown | 0.5 |
| Bool:BarrierTurretFire_Cue.bAutoActivate | False |
| Float:BlockPlayers.CapsuleHalfHeight | 84.8539 |
| Float:BlockPlayers.CapsuleRadius | 38.060886 |
| Bool:BlockPlayers.bGenerateOverlapEvents | False |
| Float:Base.LDMaxDrawDistance | 15000.0 |
| Float:Base.CachedMaxDrawDistance | 15000.0 |
| Bool:Base.bGenerateOverlapEvents | False |

## ED_FacilityTurret_Burst

| Control | Default Value |
| -------- | ------- |
| Float:FireInterval | 0.2 |
| Float:TurretRotationSpeed | 4.0 |
| Float:InitialLockonDelay | 0.0 |
| Float:FoldOutTime | 2.47 |
| Bool:bNetLoadOnClient | False |
| Bool:PointLight1.bUseInverseSquaredFalloff | False |
| Float:PointLight1.LightFalloffExponent | 6.0 |
| Float:PointLight1.AttenuationRadius | 200.0 |
| Float:PointLight1.Intensity | 15.0 |
| Bool:PointLight1.CastShadows | False |
| Bool:PointLight1.CastStaticShadows | False |
| Bool:PointLight1.CastDynamicShadows | False |
| Bool:PointLight.bUseInverseSquaredFalloff | False |
| Float:PointLight.LightFalloffExponent | 6.0 |
| Float:PointLight.AttenuationRadius | 200.0 |
| Float:PointLight.Intensity | 15.0 |
| Bool:PointLight.CastShadows | False |
| Bool:PointLight.CastStaticShadows | False |
| Bool:PointLight.CastDynamicShadows | False |
| Bool:ProjectileAttack1.ProjectilesIgnoreEachOther | True |
| Float:Shield.LDMaxDrawDistance | 15000.0 |
| Float:Shield.CachedMaxDrawDistance | 15000.0 |
| Bool:Shield.bGenerateOverlapEvents | False |
| Float:Timeline_0_Template.TimelineLength | 0.4 |
| Bool:FireWeaponGlow.AddFirstChannelAutomatically | False |

## ED_FacilityTurret_Sniper

| Control | Default Value |
| -------- | ------- |
| Float:LockOnTime | 0.5 |
| Float:BurstInterval | 1.5 |
| Float:FireInterval | 0.0 |
| Float:TurretRotationSpeed | 3.5 |
| Float:InitialLockonDelay | 0.0 |
| Float:AimZOffset | -15.0 |
| Float:TargetLeadingStrength | 0.5 |
| Float:TargetLeadingResponsiveness | 1000.0 |
| Float:RaimainAfterShotTime | 1.0 |
| Float:TargetLeadingAfterLockonMultiplier | 0.5 |
| Float:TurningSpeedAfterLockOnMultipier | 50.0 |
| Float:PreLockonTargetChangeChance | 0.11 |
| Float:PreLockongTargetChangeRate | 1.0 |
| Float:IndicatorFlashTime | 0.5 |
| Bool:TrackTargetAfterLockon | True |
| Bool:UseTraceForLockOn | True |
| Float:IndicatorActivationDelay | 2.1 |
| Bool:InvulnerableOnInactive | False |
| Float:FoldOutTime | 2.3 |
| Float:AimAcceleration | 40.0 |
| Bool:LockonParticles.bAutoActivate | False |
| Bool:Beam.bVisible | False |
| Bool:BeamLockOn.bVisible | False |
| Bool:PointLight1.bUseInverseSquaredFalloff | False |
| Float:PointLight1.LightFalloffExponent | 6.0 |
| Float:PointLight1.AttenuationRadius | 300.0 |
| Float:PointLight1.Intensity | 15.0 |
| Bool:PointLight1.CastShadows | False |
| Bool:PointLight1.bVisible | False |
| Bool:PointLight2.bUseInverseSquaredFalloff | False |
| Float:PointLight2.LightFalloffExponent | 6.0 |
| Float:PointLight2.AttenuationRadius | 250.0 |
| Float:PointLight2.Intensity | 20.0 |
| Bool:PointLight2.CastShadows | False |
| Bool:PointLight.bUseInverseSquaredFalloff | False |
| Float:PointLight.LightFalloffExponent | 6.0 |
| Float:PointLight.AttenuationRadius | 250.0 |
| Float:PointLight.Intensity | 10.0 |
| Bool:PointLight.CastShadows | False |
| Float:StaticMesh.LDMaxDrawDistance | 12000.0 |
| Float:StaticMesh.CachedMaxDrawDistance | 12000.0 |

## ED_InsectSwarm_Spawner

| Control | Default Value |
| -------- | ------- |
| Float:SpawnHeightOffset | 150.0 |
| Float:AlertDistance | 0.0 |
| Bool:CanFlee | False |
| Float:NetUpdateFrequency | 5.0 |
| Bool:PathfinderCollision.ActivatePFCollisionAtInit | True |
| Float:PointLight.AttenuationRadius | 800.0 |
| Float:PointLight.Intensity | 2000.0 |
| Bool:PointLight.CastShadows | False |
| Float:Timeline_0_Template.TimelineLength | 1.0 |
| Bool:Timeline_0_Template.bLoop | True |

## ED_EggSpider

| Control | Default Value |
| -------- | ------- |
| Float:DeathDuration | 3.0 |
| Float:MeshScale | 0.6 |
| Float:StaggerDurationMultiplier | 0.0 |
| Float:AttackerRadius | 40.0 |
| Float:JumpAttack.MaxSurfaceAngle | 35.0 |
| Float:JumpAttack.MaxRange | 230.0 |
| Float:MeleeAttack.MaxRange | 230.0 |
| Float:PawnSensing.SightRadius | 1500.0 |
| Float:Sphere.SphereRadius | 130.0 |
| Float:DropShadow.CachedMaxDrawDistance | 1300.0 |
| Bool:DropShadow.bGenerateOverlapEvents | False |
| Bool:DropShadow.bUseAttachParentBound | True |

## ED_TunnelSwarmer

| Control | Default Value |
| -------- | ------- |
| Float:DeathDuration | 3.0 |
| Float:MeshScale | 0.6 |
| Float:StaggerDurationMultiplier | 0.0 |
| Float:AttackerRadius | 40.0 |
| Float:JumpAttack.MaxSurfaceAngle | 35.0 |
| Float:JumpAttack.MaxRange | 230.0 |
| Float:MeleeAttack.MaxRange | 230.0 |
| Float:PawnSensing.SightRadius | 1500.0 |
| Float:Sphere.SphereRadius | 130.0 |
| Float:DropShadow.CachedMaxDrawDistance | 1300.0 |
| Bool:DropShadow.bGenerateOverlapEvents | False |
| Bool:DropShadow.bUseAttachParentBound | True |
