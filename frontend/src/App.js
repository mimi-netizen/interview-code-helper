import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { 
  Container, Box, Typography, Button, Paper, Select, MenuItem, 
  TextField, CircularProgress, Snackbar, Alert, AppBar, Toolbar 
} from '@mui/material';
import axios from 'axios';

function App() {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [code, setCode] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

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

  const handleLogin = async () => {
    try {
      setLoading(true);
      const response = await axios.post('http://localhost:8000/login', {
        email,
        password
      });
      setUser({ email, token: response.data.access_token });
      localStorage.setItem('user', JSON.stringify({ email, token: response.data.access_token }));
      setError(null);
    } catch (err) {
      setError('Login failed: ' + (err.response?.data?.detail || 'Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  const handleSignup = async () => {
    try {
      setLoading(true);
      await axios.post('http://localhost:8000/signup', {
        email,
        password
      });
      handleLogin();
    } catch (err) {
      setError('Signup failed: ' + (err.response?.data?.detail || 'Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  const handleQuestionChange = (event) => {
    const question = questions.find(q => q.id === event.target.value);
    setCurrentQuestion(question);
    setCode('def solution():\n    # Write your code here\n    pass');
    setResult(null);
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const response = await axios.post('http://localhost:8000/submit', {
        code,
        question_id: currentQuestion.id,
        test_cases: currentQuestion.test_cases,
        user_id: user?.id || 1
      });
      setResult(response.data.result);
      setError(null);
    } catch (err) {
      setError('Submission failed: ' + (err.response?.data?.detail || 'Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <Container maxWidth="sm">
        <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="h4" align="center">Interview Coder</Typography>
          <TextField
            label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button variant="contained" onClick={handleLogin} disabled={loading}>
            {loading ? <CircularProgress size={24} /> : 'Login'}
          </Button>
          <Button variant="outlined" onClick={handleSignup} disabled={loading}>
            Sign Up
          </Button>
        </Box>
      </Container>
    );
  }

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>Interview Coder</Typography>
          <Typography sx={{ mr: 2 }}>{user.email}</Typography>
          <Button color="inherit" onClick={() => {
            setUser(null);
            localStorage.removeItem('user');
          }}>Logout</Button>
        </Toolbar>
      </AppBar>

      <Container>
        <Box sx={{ my: 4 }}>
          <Select
            value={currentQuestion?.id || ''}
            onChange={handleQuestionChange}
            fullWidth
            sx={{ mb: 2 }}
          >
            {questions.map(q => (
              <MenuItem key={q.id} value={q.id}>{q.title}</MenuItem>
            ))}
          </Select>
          
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
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                  tabSize: 4,
                  automaticLayout: true,
                  formatOnPaste: true,
                  formatOnType: true
                }}
              />
              
              <Button 
                variant="contained" 
                onClick={handleSubmit}
                disabled={loading}
                sx={{ mt: 2 }}
              >
                {loading ? <CircularProgress size={24} /> : 'Submit Solution'}
              </Button>
              
              {result && (
                <Paper sx={{ p: 2, mt: 2 }}>
                  <Typography variant="h6" color={result.passed ? 'success.main' : 'error.main'}>
                    Status: {result.passed ? 'Passed' : 'Failed'}
                  </Typography>
                  {result.error && (
                    <Typography color="error" sx={{ whiteSpace: 'pre-wrap' }}>
                      Error: {result.error}
                    </Typography>
                  )}
                  {result.output && (
                    <Typography sx={{ whiteSpace: 'pre-wrap' }}>
                      Output: {result.output}
                    </Typography>
                  )}
                </Paper>
              )}
            </Box>
          )}
        </Box>
      </Container>

      <Snackbar 
        open={!!error} 
        autoHideDuration={6000} 
        onClose={() => setError(null)}
      >
        <Alert severity="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      </Snackbar>
    </>
  );
}

export default App;
