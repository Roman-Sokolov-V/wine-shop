import React, { useState } from 'react';
import {
  Box,
  Button,
  Columns,
  Container,
  Heading,
} from 'react-bulma-components';
import { useNavigate } from 'react-router-dom';
import { userLogin } from '../../api/auth';
import { AxiosError, AxiosResponse } from 'axios';
import { ModalLoader } from '../../components/ModalLoader';
import { ModalError } from '../../components/ModalError';
import { useDispatch } from 'react-redux';
import { actions as AuthAction } from '../../features/authentication';

export const LogInPage = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !password) {
      setError('Email and Passord are mandatory fields');
      return;
    }

    setLoading(true);
    setError('');
    userLogin(email, password)
      .then((res: AxiosResponse) => {
        const token = res.data;

        if (res.status === 200 && token) {
          dispatch(AuthAction.login(token));
          navigate('/account');
        } else {
          throw Error('Errow with login');
        }
      })
      .catch((e: AxiosError) => {
        const data = e?.response?.data;
        if (
          data &&
          typeof data === 'object' &&
          Object.values(data).length > 0
        ) {
          setError(String(Object.values(data)[0]));
        } else {
          setError('Error during login');
        }
      })
      .finally(() => setLoading(false));
  };

  if (loading) {
    return <ModalLoader />;
  }

  if (error) {
    return (
      <ModalError
        title="Error"
        body={error}
        onClose={() => setError('')}
      />
    );
  }

  return (
    <Container className="mt-6">
      <Columns centered>
        <Columns.Column size="one-third">
          <Box>
            <Heading
              size={3}
              className="has-text-centered"
            >
              Login
            </Heading>

            <form
              onSubmit={handleSubmit}
              id="login-form"
            >
              <div className="field">
                <label className="label">Email</label>
                <div className="control">
                  <input
                    className="input"
                    type="email"
                    placeholder="Enter your email"
                    name="email"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="field">
                <label className="label">Password</label>
                <div className="control">
                  <input
                    className="input"
                    type="password"
                    placeholder="Enter your password"
                    name="password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    onKeyDown={e => {
                      if (e.key === 'Enter') {
                        handleSubmit(e);
                        return;
                      }
                    }}
                    required
                  />
                </div>
              </div>

              <Button
                color="primary"
                fullwidth
                type="submit"
                className="my-4"
                onClick={handleSubmit}
              >
                Log In
              </Button>

              <a>Reset the password</a>
            </form>
          </Box>
        </Columns.Column>
      </Columns>
    </Container>
  );
};
