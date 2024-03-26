// Example CSV content
const csvContent = `Question,Answer 1,#1,Answer 2,#2,Answer 3,#3,Answer 4,#4,Answer 5,#5,Answer 6,#6,Answer 7,#7
Name A Number Thats Associated With Being Lucky Or Unlucky,7,68.0,13,26.0,3,5,,,,,,,,
Name The Most Used Piece Of Furniture In A House.,Couch,55.0,Bed,23.0,Arm Chair,15,,,,,,,,
Name A Job In Which An Attractive Person Probably Makes Better Tips.,Server,65.0,Exotic Dancer,19.0,Bartender,13,,,,,,,,
Name A Prop used By Tap Dancers,Cane,65.0,Top Hat,28.0,Baton,5,,,,,,,,
"If You Drew Homer Simpsons Name In A Secret Santa Exchange, What Would You Buy Him?",Beer,67.0,Donuts,24.0,Bowling Ball,5,,,,,,,,
Name Something You Do To An Item Before Giving It As A Gift,Wrap It,61.0,Remove Price Tag,27.0,Buy It,4,,,,,,,,
Name A Place Where It Might Be Romantic To Get Stranded With Your Partner,Island/Beach,61.0,Park,28.0,Cabin/Lodge,6,,,,,,,,
Name A Good Gift For Someone Who Is Always Late.,Watch,58.0,Alarm Clock,34.0,Calendar,3,,,,,,,,
Why Might A Family Move Into A Bigger House?,Family Has Grown,61.0,Want More Space,33.0,Can Afford More,5,,,,,,,,`;

// Parse the CSV content into an array of objects
// Adjusted parseCSV function for new format
function parseCSV(csvString) {
    const lines = csvString.trim().split('\n');
    const questions = [];

    lines.slice(1).forEach(line => {
        const parts = line.split(',');
        const questionText = parts[0];
        const answers = [];

        for (let i = 1; i < parts.length; i += 2) {
            if (parts[i] && parts[i + 1]) {
                answers.push({ answer: parts[i], points: parseFloat(parts[i + 1]) });
            }
        }

        questions.push({ question: questionText, answers });
    });

    return questions;
}

// Function to display questions
function displayQuestions(questions) {
    const container = document.getElementById('quiz-container');
    container.innerHTML = ''; // Clear previous content
    questions.forEach((question, index) => {
        const questionElement = document.createElement('div');
        questionElement.innerHTML = `<p>${question.question}</p><input type="text" id="answer-${index}" placeholder="Your answer...">`;
        container.appendChild(questionElement);
    });
}

// Adjusted isAnswerCorrect to handle multiple answers
function isAnswerCorrect(userAnswer, answers) {
    return answers.some(answer => userAnswer.trim().toLowerCase() === answer.answer.trim().toLowerCase());
}

// Adjusted submitAnswers to handle new format
function submitAnswers() {
    const containers = document.getElementById('quiz-container').children;
    let score = 0;
    Array.from(containers).forEach((container, index) => {
        const userAnswer = document.getElementById(`answer-${index}`).value;
        const { answers } = selectedQuestions[index];
        answers.forEach(answer => {
            if (isAnswerCorrect(userAnswer, answers)) {
                score += answer.points;
            }
        });
    });
    document.getElementById('result').textContent = `Your score: ${score}`;
}