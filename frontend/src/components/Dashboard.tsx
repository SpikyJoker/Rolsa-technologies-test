import { useState, useEffect, ChangeEvent } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Button, Card, Typography } from '@shadcn/ui';

interface Pdf {
  pdf_id: string;
  filename: string;
  content?: string;
}

const Dashboard = () => {
  const [pdfs, setPdfs] = useState<Pdf[]>([]);
  const [selectedPdf, setSelectedPdf] = useState<Pdf | null>(null);
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
    } catch (error: any) {
      alert(`Failed to fetch PDFs: ${error.message}`);
    }
  };

  const handleFileUpload = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
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
    } catch (error: any) {
      alert(`Failed to upload PDF: ${error.message}`);
    }
  };

  const viewPdf = async (pdfId: string) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:8000/pdf/${pdfId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSelectedPdf(response.data);
    } catch (error: any) {
      alert(`Failed to view PDF: ${error.message}`);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) {
    return null;
  }

  return (
    <div className="max-w-7xl mx-auto mt-4 mb-4">
      <Card className="p-3 mb-4 bg-gradient-to-r from-gray-700 to-gray-800 text-white">
        <div className="flex justify-between items-center">
          <Typography variant="h4" className="font-semibold">Welcome, {user}</Typography>
          <Button 
            className="bg-red-500 text-white font-bold"
            onClick={handleLogout}
          >
            Logout
          </Button>
        </div>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-3">
          <Typography variant="h6" className="mb-2 font-medium">Upload New PDF</Typography>
          <div className="flex flex-col items-center mb-3">
            <input
              type="file"
              accept=".pdf"
              id="pdf-upload"
              onChange={handleFileUpload}
              className="hidden"
            />
            <label htmlFor="pdf-upload">
              <Button 
                className="w-full bg-blue-500 text-white"
              >
                Select PDF File
              </Button>
            </label>
          </div>
          
          <hr className="mb-3" />
          
          <Typography variant="h6" className="mb-2 font-medium">Your Documents</Typography>
          
          {pdfs.length === 0 ? (
            <div className="text-center py-4">
              <svg className="w-16 h-16 text-gray-400 mb-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
              </svg>
              <Typography variant="body2" className="text-gray-500">No PDFs available</Typography>
            </div>
          ) : (
            <ul className="max-h-96 overflow-auto">
              {pdfs.map((pdf) => (
                <li 
                  key={pdf.pdf_id}
                  className="mb-1.5 p-2 border rounded hover:shadow-md transition-all"
                >
                  <Button
                    className="flex items-center w-full text-left"
                    onClick={() => viewPdf(pdf.pdf_id)}
                  >
                    <svg className="w-6 h-6 text-red-500 mr-2" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
                    </svg>
                    <Typography variant="body2" className="truncate">{pdf.filename}</Typography>
                  </Button>
                </li>
              ))}
            </ul>
          )}
        </Card>
        
        <Card className="col-span-2 p-3 min-h-[600px] flex flex-col">
          {selectedPdf ? (
            <>
              <Typography variant="h6" className="mb-2 font-medium">{selectedPdf.filename}</Typography>
              <div className="flex-grow border rounded overflow-hidden">
                <embed
                  src={`data:application/pdf;base64,${selectedPdf.content}`}
                  type="application/pdf"
                  width="100%"
                  height="100%"
                  className="min-h-[500px]"
                />
              </div>
            </>
          ) : (
            <div className="flex flex-col justify-center items-center flex-grow text-gray-500">
              <svg className="w-24 h-24 text-gray-400 mb-3" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
              </svg>
              <Typography variant="h6">Select a PDF to view</Typography>
              <Typography variant="body2" className="mt-1">Click on a document from the list to display it here</Typography>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
