import React from 'react';
import { ApolloProvider } from '@apollo/client';
import {
  BrowserRouter as Router,
  Navigate,
  Route,
  Routes,
} from 'react-router-dom';
import { HomePage } from '../HomePage';
import { CatalogPage } from '../CatalogPage';
import App from '../App/App';
import client from '../../lib/apollos';
import { ProtectedRoute } from '../../components/ProtectedRoute/ProtectedRoute';
import { VALID_ROUTES } from '../../types/validRoutes';
import { FavoritePage } from '../FavoritePage';

export const Root = () => {
  return (
    <ApolloProvider client={client}>
      <Router>
        <Routes>
          <Route
            path="/"
            element={<App />}
          >
            <Route
              index
              element={<HomePage />}
            />

            <Route
              path={VALID_ROUTES.HOME}
              element={
                <Navigate
                  to="/"
                  replace
                />
              }
            />

            <Route
              path={VALID_ROUTES.CATALOG}
              element={<CatalogPage />}
            />

            <Route
              path={VALID_ROUTES.FAVORITES}
              element={<FavoritePage />}
            />

            <Route
              path={VALID_ROUTES.LOGIN}
              element={<p>Login</p>}
            />

            <Route
              path={VALID_ROUTES.LOGOUT}
              element={<p>Logout</p>}
            />

            <Route element={<ProtectedRoute />}>
              <Route path={VALID_ROUTES.ACCOUNT}>
                <Route
                  index
                  element={<p>Account</p>}
                />
              </Route>
            </Route>
          </Route>

          <Route
            path="*"
            element={<p>PAGE NOT FOUND</p>}
          />
        </Routes>
      </Router>
    </ApolloProvider>
  );
};
