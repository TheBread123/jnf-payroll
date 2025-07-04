import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  Box,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

const Login = ({ onLoginSuccess }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    // Clear errors when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // Use environment variable for API URL, fallback to same origin for production deployment
      const apiUrl = process.env.REACT_APP_API_URL || window.location.origin;
      
      console.log('API URL:', apiUrl); // Debug logging
      console.log('Login data:', { username: formData.username, password: '***' }); // Debug logging
      
      const response = await axios.post(`${apiUrl}/api/login`, {
        username: formData.username,
        password: formData.password
      });

      console.log('Login response:', response.data); // Debug logging

      if (response.data.success) {
        setSuccess('Login successful!');
        
        // Store token in localStorage
        localStorage.setItem('authToken', response.data.token);
        localStorage.setItem('userData', JSON.stringify(response.data.user));
        
        // Call parent component's success handler
        if (onLoginSuccess) {
          onLoginSuccess(response.data.user, response.data.token);
        }
      }
    } catch (error) {
      console.error('Login error:', error); // Debug logging
      if (error.response && error.response.data && error.response.data.error) {
        setError(error.response.data.error);
      } else {
        setError('Login failed. Please check your internet connection and try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = (username, password) => {
    setFormData({ username, password });
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box textAlign="center" mb={3}>
          <Typography variant="h4" component="h1" gutterBottom>
            JNF Payroll System
          </Typography>
          <Typography variant="h5" component="h2" color="primary" gutterBottom>
            Login
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Username"
            name="username"
            type="text"
            value={formData.username}
            onChange={handleChange}
            margin="normal"
            required
            disabled={loading}
            autoComplete="username"
          />

          <TextField
            fullWidth
            label="Password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            margin="normal"
            required
            disabled={loading}
            autoComplete="current-password"
          />

          <Button
            type="submit"
            fullWidth
            variant="contained"
            disabled={loading}
            sx={{ mt: 3, mb: 2, py: 1.5 }}
          >
            {loading ? (
              <>
                <CircularProgress size={24} sx={{ mr: 1 }} />
                Signing In...
              </>
            ) : (
              'Sign In'
            )}
          </Button>
        </form>

        <Box sx={{ mt: 3 }}>
          <Typography variant="h6" gutterBottom>
            Demo Accounts:
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
            <Button
              variant="outlined"
              size="small"
              onClick={() => handleDemoLogin('admin', 'password123')}
              disabled={loading}
            >
              Admin (admin/password123)
            </Button>
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              variant="outlined"
              size="small"
              onClick={() => handleDemoLogin('demo', 'demo123')}
              disabled={loading}
            >
              Demo User (demo/demo123)
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default Login;
