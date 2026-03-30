import { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../api/axiosInstance";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      // In a real app, you might call a /me endpoint here
      // For now, we'll assume the token is valid if it exists
      setUser({ token });
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
      // 1. Create a URLSearchParams object (This sends data as application/x-www-form-urlencoded)
      const params = new URLSearchParams();
      params.append('username', email); 
      params.append('password', password);

      try {
          // 2. Pass 'params' instead of a raw object
          const response = await axiosInstance.post('/auth/login', params, {
              headers: {
                  'Content-Type': 'application/x-www-form-urlencoded'
              }
          });

          const { access_token } = response.data;
          
          localStorage.setItem('token', access_token);
          setUser({ token: access_token });
          navigate('/events');
      } catch (err) {
          console.error("Login Error Details:", err.response?.data);
          throw err; // Re-throw so the UI shows the error message
      }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    navigate("/login");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
