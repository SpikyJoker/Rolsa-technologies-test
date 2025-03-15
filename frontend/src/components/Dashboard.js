import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Button, 
  List, 
  ListItem, 
  ListItemText, 
  Typography, 
  Paper, 
  Box, 
  Divider,
  IconButton,
  Grid,
  Card,
  CardContent
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import LogoutIcon from '@mui/icons-material/Logout';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [pdfs, setPdfs] = useState([]);
  const [selectedPdf, setSelectedPdf] = useState(null);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      navigate('/login');
    } else {
      fetchPdfs();
    }
  }, [user, navigate]);

  const fetchPdfs = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/pdfs', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.status === 200) {
        setPdfs(response.data || []);
      } else {
        alert('Failed to fetch pdfs');
      }
    } catch (error) {
      alert(`Failed to fetch PDFs: ${error.message}`);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) {
      return;
    }
    try {
      const formData = new FormData();
      formData.append('file', file);
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:8000/upload-pdf', formData, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      fetchPdfs();
    } catch (error) {
      alert(`Failed to upload PDF: ${error.message}`);
    }
  };

  const viewPdf = async (pdfId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:8000/pdf/${pdfId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSelectedPdf(response.data);
    } catch (error) {
      alert(`Failed to view PDF: ${error.message}`);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) {
    navigate('/login');
    return null;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper 
        elevation={3} 
        sx={{ 
          p: 3, 
          mb: 4, 
          borderRadius: 2,
          background: 'linear-gradient(to right, #4a6572, #334756)'
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h4" component="h1" sx={{ color: 'white', fontWeight: 600 }}>
            Welcome, {user}
          </Typography>
          <Button 
            variant="contained" 
            color="error" 
            onClick={handleLogout}
            startIcon={<LogoutIcon />}
            sx={{ fontWeight: 'bold' }}
          >
            Logout
          </Button>
        </Box>
      </Paper>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Paper elevation={2} sx={{ p: 3, borderRadius: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom sx={{ mb: 2, fontWeight: 500 }}>
              Upload New PDF
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
              <input
                type="file"
                accept=".pdf"
                id="pdf-upload"
                onChange={handleFileUpload}
                style={{ display: 'none' }}
              />
              <label htmlFor="pdf-upload">
                <Button 
                  variant="contained" 
                  component="span"
                  color="primary"
                  startIcon={<UploadFileIcon />}
                  fullWidth
                  sx={{ py: 1.5 }}
                >
                  Select PDF File
                </Button>
              </label>
            </Box>
            
            <Divider sx={{ mb: 3 }} />
            
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 500 }}>
              Your Documents
            </Typography>
            
            {pdfs.length === 0 ? (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <PictureAsPdfIcon sx={{ fontSize: 60, color: 'text.disabled', mb: 2 }} />
                <Typography variant="body1" color="text.secondary">
                  No PDFs available
                </Typography>
              </Box>
            ) : (
              <List component="nav" sx={{ maxHeight: '400px', overflow: 'auto' }}>
                {pdfs.map((pdf) => (
                  <Paper 
                    key={pdf.pdf_id}
                    elevation={1} 
                    sx={{ 
                      mb: 1.5,
                      transition: 'all 0.2s',
                      '&:hover': { 
                        transform: 'translateY(-2px)',
                        boxShadow: 3
                      }
                    }}
                  >
                    <ListItem 
                      button 
                      onClick={() => viewPdf(pdf.pdf_id)}
                      selected={selectedPdf && selectedPdf.pdf_id === pdf.pdf_id}
                      sx={{ 
                        borderRadius: 1,
                        '&.Mui-selected': {
                          backgroundColor: 'rgba(25, 118, 210, 0.12)',
                          '&:hover': {
                            backgroundColor: 'rgba(25, 118, 210, 0.18)',
                          },
                        },
                      }}
                    >
                      <PictureAsPdfIcon sx={{ mr: 2, color: 'error.main' }} />
                      <ListItemText 
                        primary={pdf.filename} 
                        primaryTypographyProps={{ noWrap: true }}
                      />
                    </ListItem>
                  </Paper>
                ))}
              </List>
            )}
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={8}>
          <Paper 
            elevation={2} 
            sx={{ 
              p: 3, 
              borderRadius: 2, 
              minHeight: '600px',
              display: 'flex',
              flexDirection: 'column'
            }}
          >
            {selectedPdf ? (
              <>
                <Typography variant="h6" gutterBottom sx={{ mb: 2, fontWeight: 500 }}>
                  {selectedPdf.filename}
                </Typography>
                <Box 
                  sx={{ 
                    flexGrow: 1, 
                    border: '1px solid #e0e0e0', 
                    borderRadius: 1,
                    overflow: 'hidden'
                  }}
                >
                  <embed
                    src={`data:application/pdf;base64,${selectedPdf.content}`}
                    type="application/pdf"
                    width="100%"
                    height="100%"
                    style={{ minHeight: '500px' }}
                  />
                </Box>
              </>
            ) : (
              <Box 
                sx={{ 
                  display: 'flex', 
                  flexDirection: 'column', 
                  justifyContent: 'center', 
                  alignItems: 'center', 
                  height: '100%',
                  color: 'text.secondary'
                }}
              >
                <PictureAsPdfIcon sx={{ fontSize: 100, color: 'text.disabled', mb: 3 }} />
                <Typography variant="h6">
                  Select a PDF to view
                </Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Click on a document from the list to display it here
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Dashboard;