import { useState, FormEvent, ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Typography } from '@/components/ui/typography';

const Login = () => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [loginError, setLoginError] = useState<string>('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
      setLoginError('Login failed. Please check your credentials.');
    }
  };

  return (
    <div className="max-w-xs mx-auto mt-4 mb-4 p-4">
      <Card>
        <Typography variant="h4" className="mb-4">Login</Typography>
        {loginError && (
          <Typography variant="p" className="text-red-500 mb-4">
            {loginError}
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
            Login
          </Button>
          <Button 
            type="button" 
            onClick={() => navigate('/register')} 
            className="w-full p-2 text-blue-500 mt-1"
          >
            Register
          </Button>
        </form>
      </Card>
    </div>
  );
};

export default Login;
