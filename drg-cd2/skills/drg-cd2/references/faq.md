# CD2 FAQ

* **Q: Where can I get the mod?**
* A: The mod right now is in open beta and the .pak file can be found in the Practical DRG discord server. The mod integration loader is recommended.
<br/>
* **Q: Can I use this at the same time as CD1?**
* A: No. Only enable one CD version at a time. If you want to join CD1 lobbies while having CD2 enabled yourself and not suffer a desync in the nitra cost of resupplies,
there is a cd1-client.pak available in PDRG that allows to do that.
<br/>
* **Q: How can I use the cd2 pak?**
* A: Drag and drop the zip file into MINT and press install mods. You do not need to extract the pak from the zip to install.
<br/>
* **Q: Do clients need CD2 to play in my CD2 lobby?**
* A: Clients only need CD2 if you use certain features. For instance, difficulties that use the Enemies module will require that all clients have CD2. If the EnemiesNoSync module is used instead, clients will no longer need CD2. 
[On Pubbing With CD2](https://docs.google.com/document/d/1ShytNpPJF56XojjrTofA9DCkBXCzqBH2W-aFaLgbk30/edit?tab=t.0#heading=h.ithv7n4jcboa) is a guide by @Spy detailing which CD2 features are incompatible with pubbing and is a recommended read.
<br/>
* **Q: Why aren't my original CD1 difficulties compatible with CD2?**
* A: Custom Difficulty v2 is a complete redesign and it uses top level names to denote independent modules.
If you need to port something from CD1 to CD2, there is [a script](https://github.com/vonacht/cd2ifier/tree/main/src) that automatically does the translation. Alternatively, you can
post the file in the PDRG forums asking for help in running the script or making the port yourself. 
<br/>
* **Q: Does CD2 support more than 4 players?**
* A: Yes CD2 has complete support for more than 4 player lobbies. Any player-count depedent field can be extended to any number of players. Additionally, you can specify `MaxPlayers: 8` in your difficulty to set the max players count.
<br/>
* **Q: Will changing the difficulty mid mission break the game like in CD1?**
* A: No. That has not been observed in any of the testing so far.
<br/>
* **Q: Is this compatible with MEV/DEA and other similar expansion mods?**
* A: Yes, this is fully compatible with the most common enemy expansion mods!
<br/>
* **Q: Is CD2 compatible with Deep Dives?**
* A: Yes, and it doesn't need any extra mods. Just select your chosen difficulty and go into the dive. There is also the possibility of choosing a different difficulty for each stage similar to the vanilla dive, please see the `NextDifficulty` section in [Modules](modules.md) to see how to do it. 
<br/>
