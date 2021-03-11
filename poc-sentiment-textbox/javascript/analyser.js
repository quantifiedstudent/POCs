const vader = require("vader-sentiment")
const Detect = require('detectlanguage')

const deteclanguage = new Detect("0d6f6dee800003f00f2562dac364c070")
let sentencesSentimentScore = []
const analyser = async (event) => {
    if(event.key == "."){
        let input = event.target.value

        let endOfSentencePositions = getAllIndexes(input, ".")
        let size = endOfSentencePositions.length
        let sentence;
        if (size == 1){
            sentence = input.slice(0, endOfSentencePositions[0])
        } else{
            sentence = input.slice(endOfSentencePositions[size-2] + 1, endOfSentencePositions[size-1])
        }
        
        let originalSentence = sentence
        let languageCode
        await deteclanguage.detect(input).then(result => {languageCode = result[0].language})
        if (languageCode != "en"){
            sentence = await translateSentence(sentence, languageCode)
        }

        const score = vader.SentimentIntensityAnalyzer.polarity_scores(sentence);
        sentencesSentimentScore.push(score)
        console.log(sentencesSentimentScore)
        const totalScore = meanScore(sentencesSentimentScore)

        addScoreToList(originalSentence, score.compound)
        addMeanScoreToHeader("Negative: " + totalScore.neg + " Neutral: " + totalScore.neu + " Positive: " + totalScore.pos + "<br> Compound: " + totalScore.compound)
    }   
}

const addScoreToList = (sentence, score) => {
    let liNode = document.createElement("LI")
    liNode.innerHTML = "<strong>" + score + "</strong> --- " + sentence
    document.getElementById("scores").appendChild(liNode)
}

const addMeanScoreToHeader = (score) => {
    document.getElementById("total-score").innerHTML = score
}

const meanScore = (scores) => {
    let length = scores.length
    console.log(length)
    let sumNeg = 0
    let sumPos = 0
    let sumNeu = 0
    let sumComp = 0

    let averageNeg = 0
    let averagePos = 0
    let averageNeu = 0
    let averageComp = 0

    scores.forEach(element => {
        sumNeg += element.neg
        sumNeu += element.neu
        sumPos += element.pos
        sumComp += element.compound
    })

    console.log(sumNeg)
    averageNeg = sumNeg / length
    averagePos = sumPos / length
    averageNeu = sumNeu / length
    averageComp = sumComp / length

    averageComp = Math.round(averageComp * 100) / 100
    averagePos = Math.round(averagePos * 100) / 100
    averageNeu = Math.round(averageNeu * 100) / 100
    averageNeg = Math.round(averageNeg * 100) / 100
    return {neg: averageNeg, neu: averageNeu, pos: averagePos, compound: averageComp}
}

const translateSentence = async (sentence, language) => {
    let translatedSentence
    await fetch("https://api.mymemory.translated.net/get?q=" + sentence + "!&langpair=" + language + "|en")
    .then(result => {
        return result.json()
    })
    .then(data => {
        console.log(data)
        translatedSentence = data.responseData.translatedText
    })
    return translatedSentence
}


const getAllIndexes = (arr, val) => {
    var indexes = [], i;
    for(i = 0; i < arr.length; i++)
        if (arr[i] === val)
            indexes.push(i);
    return indexes;
}


document.getElementById("input").addEventListener("keyup", analyser) 
