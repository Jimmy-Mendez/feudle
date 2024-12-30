import React, { useEffect, useState } from 'react';
import axios from 'axios';

const QuestionDisplay = ({ setRow }) => {
  const [questionData, setQuestionData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:5001/get_question')
      .then((response) => {
        setQuestionData(response.data);
        setRow(response.data); // Pass the data to the parent component
      })
      .catch((error) => setError(error.message));
  }, [setRow]);

  if (error) return <p>Error fetching question: {error}</p>;
  if (!questionData) return <p>Loading...</p>;

  return (
    <div>
      <h1>{questionData.question}</h1>
      <p>Top {questionData.num_answers} answers are on the board!</p>
    </div>
  );
};

export default QuestionDisplay;
