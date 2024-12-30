import React, { useState } from 'react';
import axios from 'axios';

const AnswerInput = ({ row }) => {
  const [input, setInput] = useState('');
  const [feedback, setFeedback] = useState('');
  const [score, setScore] = useState(0);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5001/check_answer', {
        row,
        user_input: input,
      });
      const { match, points } = response.data;
      if (match) {
        setFeedback(`Correct! ${match} is worth ${points} points.`);
        setScore(score + points);
      } else {
        setFeedback('Incorrect! Try again.');
      }
    } catch (error) {
      setFeedback('Error checking answer. Please try again.');
    }
    setInput(''); // Clear input field
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter your answer"
        />
        <button type="submit">Submit</button>
      </form>
      <p>{feedback}</p>
      <p>Total Score: {score}</p>
    </div>
  );
};

export default AnswerInput;
