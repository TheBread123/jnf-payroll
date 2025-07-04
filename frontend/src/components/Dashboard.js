import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Alert,
  Card,
  CardContent,
  Grid,
  Chip
} from '@mui/material';
import axios from 'axios';

const Dashboard = ({ user, onLogout }) => {
  const [protectedData, setProtectedData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProtectedData();
  }, []);

  const fetchProtectedData = async () => {
    setLoading(true);
    setError('');    try {
      const token = localStorage.getItem('authToken');
      const apiUrl = process.env.REACT_APP_API_URL || window.location.origin;
      
      const response = await axios.get(`${apiUrl}/api/protected`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      setProtectedData(response.data);
    } catch (error) {
      if (error.response && error.response.data && error.response.data.error) {
        setError(error.response.data.error);
      } else {
        setError('Failed to fetch protected data. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    onLogout();
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4" component="h1">
          JNF Payroll Dashboard
        </Typography>
        <Button variant="outlined" color="secondary" onClick={handleLogout}>
          Logout
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* User Info Card */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                User Information
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Username
                </Typography>
                <Typography variant="body1">
                  {user.username}
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Email
                </Typography>
                <Typography variant="body1">
                  {user.email}
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Role
                </Typography>
                <Chip 
                  label={user.role} 
                  color={user.role === 'admin' ? 'primary' : 'secondary'}
                  variant="outlined"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* API Integration Demo Card */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Backend Integration Demo
              </Typography>
              {loading ? (
                <Typography>Loading protected data...</Typography>
              ) : protectedData ? (
                <Box>
                  <Alert severity="success" sx={{ mb: 2 }}>
                    Successfully connected to Flask backend!
                  </Alert>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Protected API Response:
                  </Typography>
                  <Paper sx={{ p: 2, bgcolor: 'grey.100' }}>
                    <Typography variant="body2" component="pre">
                      {JSON.stringify(protectedData, null, 2)}
                    </Typography>
                  </Paper>
                </Box>
              ) : (
                <Button 
                  variant="contained" 
                  onClick={fetchProtectedData}
                  disabled={loading}
                >
                  Test Protected API
                </Button>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* System Status Card */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Status
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <Box textAlign="center">
                    <Chip label="Frontend: Active" color="success" />
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      React App Running
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box textAlign="center">
                    <Chip 
                      label={protectedData ? "Backend: Connected" : "Backend: Checking..."} 
                      color={protectedData ? "success" : "warning"} 
                    />
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      Flask API Status
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box textAlign="center">
                    <Chip label="Azure: Deployed" color="info" />
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      Cloud Deployment
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
