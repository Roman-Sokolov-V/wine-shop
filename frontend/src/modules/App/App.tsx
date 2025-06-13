import React from 'react';
import style from './App.module.scss';
import '../../styles/main.scss';
import { Outlet } from 'react-router-dom';
import { Section, Container } from 'react-bulma-components';
import classNames from 'classnames';
import { Header } from '../../components/Header';

import '../../styles/main.scss';
import { FooterElem } from '../../components/FooterElem';
import ScrollToTop from '../../components/ScrollToTop/ScrollToTop';
import { useAppSelector } from '../../app/hooks';

function App() {
  const { visible: mobileMenuVisible } = useAppSelector(
    state => state.menuVisible,
  );

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
      <Header />

      {!mobileMenuVisible && (
        <Container className={classNames('', style.main_container)}>
          <Outlet />
        </Container>
      )}

      {!mobileMenuVisible && <FooterElem />}

      <ScrollToTop />
    </Section>
  );
}

export default App;
