import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { Container, Box, Typography, Button, Paper } from '@mui/material';
import axios from 'axios';

function App() {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [code, setCode] = useState('');
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    try {
      const response = await axios.get('http://localhost:8000/questions');
      setQuestions(response.data.questions);
      if (response.data.questions.length > 0) {
        setCurrentQuestion(response.data.questions[0]);
      }
    } catch (error) {
      console.error('Error fetching questions:', error);
    }
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:8000/submit', {
        code,
        question_id: currentQuestion.id,
        test_cases: currentQuestion.test_cases,
        user_id: 1 // Hardcoded for now, should come from auth
      });
      setResult(response.data.result);
    } catch (error) {
      console.error('Error submitting code:', error);
      setResult({ error: 'Failed to submit code' });
    }
  };

  return (
    <Container>
      <Typography variant="h4" sx={{ my: 4 }}>
        Interview Coder
      </Typography>
      
      {currentQuestion && (
        <Box sx={{ mb: 4 }}>
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6">{currentQuestion.title}</Typography>
            <Typography>{currentQuestion.description}</Typography>
          </Paper>
          
          <Editor
            height="400px"
            defaultLanguage="python"
            value={code}
            onChange={setCode}
            theme="vs-dark"
          />
          
          <Button 
            variant="contained" 
            onClick={handleSubmit}
            sx={{ mt: 2 }}
          >
            Submit Solution
          </Button>
          
          {result && (
            <Paper sx={{ p: 2, mt: 2 }}>
              <Typography>
                Status: {result.passed ? 'Passed' : 'Failed'}
              </Typography>
              {result.error && (
                <Typography color="error">
                  Error: {result.error}
                </Typography>
              )}
              {result.output && (
                <Typography>
                  Output: {result.output}
                </Typography>
              )}
            </Paper>
          )}
        </Box>
      )}
    </Container>
  );
}

export default App;
