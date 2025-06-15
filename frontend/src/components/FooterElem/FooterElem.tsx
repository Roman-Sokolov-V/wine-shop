import React from 'react';
import classNames from 'classnames';
import style from './FooterElem.module.scss';
import { Columns, Container, Footer } from 'react-bulma-components';
import { v4 as uuidv4 } from 'uuid';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useAppSelector } from '../../app/hooks';

export const FooterElem = () => {
  const { loggedIn } = useAppSelector(state => state.auth);

  return (
    <Footer
      className={classNames(
        'is-fixed-bottom has-background-primary px-0 py-4',
        style.contaniner,
      )}
    >
      Footer
    </Footer>
  );
};
