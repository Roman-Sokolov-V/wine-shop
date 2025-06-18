import React, { useEffect, useState } from 'react';
import style from './App.module.scss';
import '../../styles/main.scss';
import { Outlet } from 'react-router-dom';
import { Section, Container } from 'react-bulma-components';
import classNames from 'classnames';
import { Header } from '../../components/Header';

import '../../styles/main.scss';
import { FooterElem } from '../../components/FooterElem';
import ScrollToTop from '../../components/ScrollToTop/ScrollToTop';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { getPetsData } from '../../api/pets';
import { ModalLoader } from '../../components/ModalLoader';
import { ModalError } from '../../components/ModalError';
import * as PetActions from '../../features/pets';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { visible: mobileMenuVisible } = useAppSelector(
    state => state.menuVisible,
  );

  const dispatch = useAppDispatch();

  useEffect(() => {
    setLoading(true);
    getPetsData()
      .then(res => {
        if (res?.data) {
          dispatch(PetActions.actions.setPets(res.data));
        }
      })
      .catch(e => {
        setError(e?.message ? e.message : 'Error Occured');
      })
      .then(() => setLoading(false));
  }, []);

  if (error) {
    return (
      <ModalError
        title="Error"
        body={error}
        onClose={() => setError('')}
      />
    );
  }

  if (loading) {
    return <ModalLoader />;
  }

  return (
    <Section
      className={classNames(
        'p-0 is-flex is-flex-direction-column has-background-white',
        style.app,
        {
          [style.menu_visible]: mobileMenuVisible,
        },
      )}
      size="full"
    >
      <Container>
        <Header />
      </Container>

      {!mobileMenuVisible && (
        <Container className={classNames(style.main_container)}>
          <Outlet />
        </Container>
      )}

      {!mobileMenuVisible && <FooterElem />}

      <ScrollToTop />
    </Section>
  );
}

export default App;
