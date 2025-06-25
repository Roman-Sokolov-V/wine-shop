import React, { useEffect } from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { actions as authActions } from '../../features/authentication';

type Props = {
  redirectPath?: string;
};

export const ProtectedRoute: React.FC<Props> = ({ redirectPath = 'login' }) => {
  const { loggedIn, user } = useAppSelector(state => state.auth);
  const dispatch = useAppDispatch();
  const location = useLocation();
  useEffect(() => {
    if (loggedIn === undefined || !user) {
      dispatch(authActions.init());
    }
  }, [location]);

  if (!loggedIn) {
    return (
      <Navigate
        to={redirectPath}
        replace
      />
    );
  }

  return <Outlet />;
};
