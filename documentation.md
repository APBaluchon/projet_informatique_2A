## Toplane

### Variables à conserver

- kills
- assists
- deaths
- teamKills
- totalMinionsKilled
- gameDuration
- visionScore
- neutralMinionsKilled
- totalNeutralMinions

### Formules

#### taux de participations aux tueries

$(\frac{kills+assists}{teamKills})\times 100$

####  ratio de rentabilité

$\frac{kills+assists}{deaths}$

#### efficacité de farming

$\frac{totalMinionsKilled}{gameDuration}\times 60$

#### vision score par minute

$\frac{visionScore}{GameDuration}\times 60$

#### taux d'objectifs

$\frac{neutralMinionsKilled}{totalNeutralMinions}$

## Jungle

### Variables à conserver

- objectiveKills
- totalObjectiveKills
- epicMonstersKilled
- epicMonstersSpawned

### Formules

#### taux de participation aux tueries

$\frac{kills+assists}{teamKills}\times 100$

#### efficacité de farming

$\frac{neutralMinionsKilled}{gameDuration}\times 60$

#### vision score par minute

$\frac{visioScore}{gameDuration}\times 60$

#### taux de contrôle objectif

$\frac{objectiveKills}{totalObjectiveKills}$

#### ratio de sécurisation d'objectif

$\frac{epicMonstersKilled}{epicMonstersSpawned}\times 100$


## Mid

### Variables à conserver

- turretKills

### Formules

#### taux de participation aux tueries

$\frac{kills+assists}{teamKills}\times 100$

####  ratio de rentabilité

$\frac{kills+assists}{deaths}$

#### efficacité de farming

$\frac{neutralMinionsKilled}{gameDuration}\times 60$

#### vision score par minute

$\frac{visioScore}{gameDuration}\times 60$

#### taux de structures abattues

$\frac{turretKills}{gameDuration}\times 60$

## ADC

### Variables à conserver

- totalDamageDealtToChampions
- goldEarned

### Formules

#### taux de participation aux tueries

$\frac{kills+assists}{teamKills}\times 100$

####  ratio de rentabilité

$\frac{kills+assists}{deaths}$

#### efficacité de farming

$\frac{neutralMinionsKilled}{gameDuration}\times 60$

#### dégâts par minute

$\frac{totalDamageDealtToChampions}{gameDuration}\times 60$

#### gold par minute

$\frac{goldEarned}{gameDuration}\times 60$

## Support

### Variables à conserver

- wardsKilled
- wardsPlaced

### Formules

#### taux de participation aux tueries

$\frac{kills+assists}{teamKills}\times 100$

#### vision score par minute

$\frac{visioScore}{gameDuration}\times 60$

####  ratio de rentabilité

$\frac{kills+assists}{deaths}$

#### ward destruction par minute

$\frac{wardsKilled}{gameDuration}\times 60$

#### ward placed par minute

$\frac{wardsPlaced}{gameDuration}\times 60$