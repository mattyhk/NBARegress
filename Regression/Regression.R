carmelo = read.csv("Python/Factors2/Carmelo Anthony Factors.csv")
durant = read.csv("Python/Factors2/Kevin Durant Factors.csv")
bryant = read.csv("Python/Factors2/Kobe Bryant Factors.csv")
harden = read.csv("Python/Factors2/James Harden Factors.csv")
james = read.csv("Python/Factors2/LeBron James Factors.csv")

library(caTools)

carmeloLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=carmelo, family=binomial)
durantLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=durant, family=binomial)
bryantLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=bryant, family=binomial)
hardenLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=harden, family=binomial)
jamesLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=james, family=binomial)

carmeloLogRed = glm(made ~ takenInterval + distance, data=carmelo, family=binomial)
summary(carmeloLogRed)

durantLogRed = glm(made ~ situation + madeInterval + distance, data=durant, family=binomial)
summary(durantLogRed)

bryantLogRed = glm(made ~ location + distance, data=bryant, family=binomial)
summary(bryantLogRed)

hardenLogRed = glm(made ~ takenInterval + madeInterval + distance, data=harden, family=binomial)
summary(hardenLogRed)

jamesLogRed = glm(made ~ situation + distance, data=james, family=binomial)
summary(jamesLogRed)

westbrook = read.csv("Python/Factors2/Russell Westbrook Factors.csv")
curry = read.csv("Python/Factors2/Stephen Curry Factors.csv")
wade = read.csv("Python/Factors2/Dwyane Wade Factors.csv")
aldridge = read.csv("Python/Factors2/LaMarcus Aldridge Factors.csv")
lopez = read.csv("Python/Factors2/Brook Lopez Factors.csv")
ellis = read.csv("Python/Factors2/Monta Ellis Factors.csv")
lillard = read.csv("Python/Factors2/Damian Lillard Factors.csv")
williams = read.csv("Python/Factors2/Deron Williams Factors.csv")
pierce = read.csv("Python/Factors2/Paul Pierce Factors.csv")
lee = read.csv("Python/Factors2/David Lee Factors.csv")
gay = read.csv("Python/Factors2/Rudy Gay Factors.csv")
derozan = read.csv("Python/Factors2/DeMar DeRozan Factors.csv")
smith = read.csv("Python/Factors2/J.R. Smith Factors.csv")
griffin = read.csv("Python/Factors2/Blake Griffin Factors.csv")
jefferson = read.csv("Python/Factors2/Al Jefferson Factors.csv")

westbrookLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=westbrook, family=binomial)
curryLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=curry, family=binomial)
wadeLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=wade, family=binomial)
aldridgeLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=aldridge, family=binomial)
lopezLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=lopez, family=binomial)
ellisLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=ellis, family=binomial)
lillardLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=lillard, family=binomial)
williamsLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=williams, family=binomial)
pierceLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=pierce, family=binomial)
leeLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=lee, family=binomial)
gayLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=gay, family=binomial)
derozanLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=derozan, family=binomial)
smithLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=smith, family=binomial)
griffinLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=griffin, family=binomial)
jeffersonLog = glm(made ~ location + situation + fgPercentage + takenInterval + madeInterval + numShots + distance, data=jefferson, family=binomial)

N = 20

names = c("carmelo", "durant", "bryant", "harden", "james", "westbrook", "curry", "wade", "aldridge", "lopez", "ellis", "lillard", "williams", "pierce", "lee", "gay", "derozan", "smith", "griffin", "jefferson")
situations = numeric(N)
situations[1] = summary(carmeloLog)$coefficients[3,1]
situations[2] = summary(durantLog)$coefficients[3,1]
situations[3] = summary(bryantLog)$coefficients[3,1]
situations[4] = summary(hardenLog)$coefficients[3,1]
situations[5] = summary(jamesLog)$coefficients[3,1]
situations[6] = summary(westbrookLog)$coefficients[3,1]
situations[7] = summary(curryLog)$coefficients[3,1]
situations[8] = summary(wadeLog)$coefficients[3,1]
situations[9] = summary(aldridgeLog)$coefficients[3,1]
situations[10] = summary(lopezLog)$coefficients[3,1]
situations[11] = summary(ellisLog)$coefficients[3,1]
situations[12] = summary(lillardLog)$coefficients[3,1]
situations[13] = summary(williamsLog)$coefficients[3,1]
situations[14] = summary(pierceLog)$coefficients[3,1]
situations[15] = summary(leeLog)$coefficients[3,1]
situations[16] = summary(gayLog)$coefficients[3,1]
situations[17] = summary(derozanLog)$coefficients[3,1]
situations[18] = summary(smithLog)$coefficients[3,1]
situations[19] = summary(griffinLog)$coefficients[3,1]
situations[20] = summary(jeffersonLog)$coefficients[3,1]

order = rankings[order(situations),]
tail(order)

distances = numeric(N)
distances[1] = summary(carmeloLog)$coefficients[8,1]
distances[2] = summary(durantLog)$coefficients[8,1]
distances[3] = summary(bryantLog)$coefficients[8,1]
distances[4] = summary(hardenLog)$coefficients[8,1]
distances[5] = summary(jamesLog)$coefficients[8,1]
distances[6] = summary(westbrookLog)$coefficients[8,1]
distances[7] = summary(curryLog)$coefficients[8,1]
distances[8] = summary(wadeLog)$coefficients[8,1]
distances[9] = summary(aldridgeLog)$coefficients[8,1]
distances[10] = summary(lopezLog)$coefficients[8,1]
distances[11] = summary(ellisLog)$coefficients[8,1]
distances[12] = summary(lillardLog)$coefficients[8,1]
distances[13] = summary(williamsLog)$coefficients[8,1]
distances[14] = summary(pierceLog)$coefficients[8,1]
distances[15] = summary(leeLog)$coefficients[8,1]
distances[16] = summary(gayLog)$coefficients[8,1]
distances[17] = summary(derozanLog)$coefficients[8,1]
distances[18] = summary(smithLog)$coefficients[8,1]
distances[19] = summary(griffinLog)$coefficients[8,1]
distances[20] = summary(jeffersonLog)$coefficients[8,1]

rankings = data.frame(names, situations, distances)
distanceOrder = rankings[order(distances),]
tail(distanceOrder)

percentages = numeric(N)
percentages[1] = summary(carmeloLog)$coefficients[4,1]
percentages[2] = summary(durantLog)$coefficients[4,1]
percentages[3] = summary(bryantLog)$coefficients[4,1]
percentages[4] = summary(hardenLog)$coefficients[4,1]
percentages[5] = summary(jamesLog)$coefficients[4,1]
percentages[6] = summary(westbrookLog)$coefficients[4,1]
percentages[7] = summary(curryLog)$coefficients[4,1]
percentages[8] = summary(wadeLog)$coefficients[4,1]
percentages[9] = summary(aldridgeLog)$coefficients[4,1]
percentages[10] = summary(lopezLog)$coefficients[4,1]
percentages[11] = summary(ellisLog)$coefficients[4,1]
percentages[12] = summary(lillardLog)$coefficients[4,1]
percentages[13] = summary(williamsLog)$coefficients[4,1]
percentages[14] = summary(pierceLog)$coefficients[4,1]
percentages[15] = summary(leeLog)$coefficients[4,1]
percentages[16] = summary(gayLog)$coefficients[4,1]
percentages[17] = summary(derozanLog)$coefficients[4,1]
percentages[18] = summary(smithLog)$coefficients[4,1]
percentages[19] = summary(griffinLog)$coefficients[4,1]
percentages[20] = summary(jeffersonLog)$coefficients[4,1]

rankings = data.frame(names, percentages)
percentagesOrder = rankings[order(percentages),]


locations = numeric(N)
locations[1] = summary(carmeloLog)$coefficients[2,1]
locations[2] = summary(durantLog)$coefficients[2,1]
locations[3] = summary(bryantLog)$coefficients[2,1]
locations[4] = summary(hardenLog)$coefficients[2,1]
locations[5] = summary(jamesLog)$coefficients[2,1]
locations[6] = summary(westbrookLog)$coefficients[2,1]
locations[7] = summary(curryLog)$coefficients[2,1]
locations[8] = summary(wadeLog)$coefficients[2,1]
locations[9] = summary(aldridgeLog)$coefficients[2,1]
locations[10] = summary(lopezLog)$coefficients[2,1]
locations[11] = summary(ellisLog)$coefficients[2,1]
locations[12] = summary(lillardLog)$coefficients[2,1]
locations[13] = summary(williamsLog)$coefficients[2,1]
locations[14] = summary(pierceLog)$coefficients[2,1]
locations[15] = summary(leeLog)$coefficients[2,1]
locations[16] = summary(gayLog)$coefficients[2,1]
locations[17] = summary(derozanLog)$coefficients[2,1]
locations[18] = summary(smithLog)$coefficients[2,1]
locations[19] = summary(griffinLog)$coefficients[2,1]
locations[20] = summary(jeffersonLog)$coefficients[2,1]

rankings = data.frame(names, locations)
locationsOrder = rankings[order(locations),]
tail(locationsOrder)
head(locationsOrder)

covariates = data.frame(names, locations, percentages, situations, distances)

library(ggplot2)

lastNames = c("Anthony", "Durant", "Bryant", "Harden", "James", "Westbrook", "Curry", "Wade", "Aldridge", "Lopez", "Ellis", "Lillard", "Williams", "Pierce", "Lee", "Gay", "DeRozan", "Smith", "Griffin", "Jefferson")

covariates$lastNames = lastNames

png("Plots/LocationVsSituation.png")
ggplot(covariates, aes(x = locations, y = situations)) + geom_point(color = 'blue', size = 2) + ggtitle("Location Variable vs. Situation Variable") + xlab("Location Variable") + ylab("Situation Variable") + geom_text(aes(label=lastNames), hjust=-0.2, vjust=1, size = 3) + xlim(c(-0.32, 0.22))
dev.off()

png("Plots/DistanceVsSituation.png")
ggplot(covariates, aes(x = distances, y = situations)) + geom_point(color = 'blue', size = 2) + ggtitle("Distance Variable vs. Situation Variable") + xlab("Distance Variable") + ylab("Situation Variable") + geom_text(aes(label=lastNames), hjust=-0.2, vjust=2, size = 2)
dev.off()

png("Plots/DistanceVsPercentage.png")
ggplot(covariates, aes(x = distances, y = percentages)) + geom_point(color = 'blue', size = 2) + ggtitle("Distance Variable vs. Momentum Variable") + xlab("Distance Variable") + ylab("Momentum") + geom_text(aes(label=lastNames), hjust=-0.2, vjust=1, size = 2)
dev.off()

