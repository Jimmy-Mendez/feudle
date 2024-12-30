import React, { useState } from 'react';
import QuestionDisplay from './components/QuestionDisplay';
import AnswerInput from './components/AnswerInput';

const App = () => {
  const [row, setRow] = useState(null);

  return (
    <div>
      <QuestionDisplay setRow={setRow} />
      {row && <AnswerInput row={row} />}
    </div>
  );
};

export default App;
