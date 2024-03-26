// Example CSV content
const csvContent = `Question,Answer,Points
Name A Profession Where You Might Have A Dog For A Sidekick,Police Officer,52
Name A Profession Where You Might Have A Dog For A Sidekick,Firefighter,26
Name A Profession Where You Might Have A Dog For A Sidekick,Performer,9
Another Question,Another Answer,10
Yet Another Question,Yet Another Answer,5`;

// Parse the CSV content into an array of objects
function parseCSV(csvString) {
    const lines = csvString.split('\n');
    const headers = lines[0].split(',');
    const data = lines.slice(1).map(line => {
        const values = line.split(',');
        return headers.reduce((object, header, index) => {
            object[header] = values[index];
            return object;
        }, {});
    });
    return data;
}

// Randomly select five unique questions
function selectRandomQuestions(questions, count = 5) {
    const shuffled = questions.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
}

// Display questions
function displayQuestions(questions) {
    const container = document.getElementById('quiz-container');
    container.innerHTML = ''; // Clear previous content
    questions.forEach((question, index) => {
        const questionElement = document.createElement('div');
        questionElement.innerHTML = `
            <p>${question.Question}</p>
            <input type="text" id="answer-${index}" placeholder="Your answer...">
        `;
        container.appendChild(questionElement);
    });
}

// Simple answer matching (can be improved with more sophisticated logic)
function isAnswerCorrect(userAnswer, correctAnswer) {
    return userAnswer.trim().toLowerCase() === correctAnswer.trim().toLowerCase();
}

// Submit answers and calculate score
function submitAnswers() {
    const answers = parseCSV(csvContent);
    let score = 0;
    answers.forEach((answer, index) => {
        const userAnswer = document.getElementById(`answer-${index}`).value;
        if (isAnswerCorrect(userAnswer, answer.Answer)) {
            score += parseInt(answer.Points, 10);
        }
    });
    document.getElementById('result').textContent = `Your score: ${score}`;
}

// Initial setup
const questions = parseCSV(csvContent);
const selectedQuestions = selectRandomQuestions(questions);
displayQuestions(selectedQuestions);
