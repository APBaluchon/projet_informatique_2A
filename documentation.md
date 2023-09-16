## stats_for_support_one_game

### indicateur de vision (IV)
$IV = 0.4\times \frac{wardPlaced}{gameDuration}+0.3\times \frac{wardKilled}{gameDuration}+0.2\times \frac{visionWardsBoughtInGame}{gameDuration}+0.1\times visionScore$

Echelle allant de 0 à 4.5

### indicateur d'engagement et de sauvetage (IES)

$IES=0.3​\times assists+0.1​ \times (kills−0.2\times deaths)+0.2\times timeCCingOthers+0.1\times \frac{totalHealsOnTeammates}{gameDuration}+0.05\times \frac{totalDamageTaken}{gameDuration}+0.05\times\frac{wardsKilled}{gameDuration}$

Echelle allant de 0 à 225

### indicateur des dégâts subis (IDS)

$IDS = 0.4\times totalDamageTaken+0.3\times damageSelfMitigated-0.2\times totalHeal-0.1\times timeCCingOthers$

Echelle allant de 0 à 21000