import { useState, FormEvent, ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Input, Button, Card, Typography } from '@shadcn/ui';

interface RegisterError {
  detail?: string;
  response?: {
    data?: {
      detail?: string;
    };
  };
  message?: string;
}

const Register = () => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/register', {
        username,
        password
      });
      // After successful registration, redirect to login
      navigate('/login');
    } catch (err) {
      const error = err as RegisterError;
      setError(error.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <div className="max-w-xs mx-auto">
      <Card>
        <Typography variant="h4" className="mb-4">Register</Typography>
        {error && (
          <Typography variant="body2" className="text-red-500 mb-4">
            {error}
          </Typography>
        )}
        <form onSubmit={handleSubmit}>
          <Input
            type="text"
            placeholder="Username"
            className="w-full p-2 mb-4"
            value={username}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setUsername(e.target.value)}
            required
          />
          <Input
            type="password"
            placeholder="Password"
            className="w-full p-2 mb-4"
            value={password}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
            required
          />
          <Button 
            type="submit" 
            className="w-full p-2 bg-blue-500 text-white rounded mt-2"
          >
            Register
          </Button>
          <Button 
            type="button" 
            onClick={() => navigate('/login')} 
            className="w-full p-2 text-blue-500 mt-1"
          >
            Already have an account? Login
          </Button>
        </form>
      </Card>
    </div>
  );
};

export default Register;
