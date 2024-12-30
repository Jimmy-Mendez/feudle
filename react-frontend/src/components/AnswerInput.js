import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AnswerInput.css'; // Add styles for the blue boxes and the X image

const AnswerInput = ({ row }) => {
  const [input, setInput] = useState('');
  const [feedback, setFeedback] = useState('');
  const [score, setScore] = useState(0);
  const [revealedAnswers, setRevealedAnswers] = useState(new Array(row.answers.length).fill(false));
  const [strikes, setStrikes] = useState(0);
  const [gameOver, setGameOver] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (gameOver) return;

    try {
      const response = await axios.post('http://localhost:5001/check_answer', {
        row,
        user_input: input,
      });

      const { match, points } = response.data;
      if (match) {
        // Update revealed answers
        const index = row.answers.indexOf(match);
        const updatedRevealedAnswers = [...revealedAnswers];
        updatedRevealedAnswers[index] = true;
        setRevealedAnswers(updatedRevealedAnswers);

        setFeedback(`Correct! ${match} is worth ${points} points.`);
        setScore(score + parseFloat(points)); // Convert points to a number

        // Check if all answers are revealed
        if (updatedRevealedAnswers.every((revealed) => revealed)) {
          setGameOver(true);
          setFeedback(`You guessed all the answers! Total score: ${score + parseFloat(points)}`);
        }
      } else {
        // Increment strikes
        setStrikes((prevStrikes) => prevStrikes + 1);
        setFeedback('Incorrect! Try again.');

        // End the game if 3 strikes
        if (strikes + 1 === 3) {
          setGameOver(true);
          setFeedback(`Game over! Total score: ${score}`);
        }
      }
    } catch (error) {
      setFeedback('Error checking answer. Please try again.');
    }
    setInput(''); // Clear input field
  };

  const revealAllAnswers = () => {
    setRevealedAnswers(new Array(row.answers.length).fill(true));
  };

  useEffect(() => {
    if (gameOver) {
      revealAllAnswers();
    }
  }, [gameOver]);

  return (
    <div>
      {/* Display the large "X" for strikes */}
      <div className="strike-container">
        {[...Array(strikes)].map((_, index) => (
          <img key={index} src="/x.jpg" alt="Strike" className="x-image" />
        ))}
      </div>

      {/* Display the answer boxes */}
      <div className="answer-boxes">
        {row.answers.map((answer, index) => (
          <div
            key={index}
            className={`answer-box ${revealedAnswers[index] ? 'revealed' : ''}`}
          >
            {revealedAnswers[index] ? answer : ''}
          </div>
        ))}
      </div>

      {/* Input for user answers */}
      {!gameOver && (
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter your answer"
          />
          <button type="submit">Submit</button>
        </form>
      )}

      <p>{feedback}</p>
      {gameOver && <p>Game Over! Total Score: {score}</p>}
    </div>
  );
};

export default AnswerInput;
