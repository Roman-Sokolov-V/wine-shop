import React from 'react';
import 'react-calendar/dist/Calendar.css';
import { Container, Section } from 'react-bulma-components';
import { SubscribeNews } from '../../components/SubscribeNews';
import { OneShotNotification } from '../../components/OneShotNotification';
import classNames from 'classnames';
import style from './HomePage.module.scss';
import { HomeBanner1 } from '../../components/HomeBanner1';
import { CatalogSlider } from '../../components/CatalogSlider';
import { getHomePageCatData, getHomePageDogData } from '../../api/pets';

export const HomePage = () => {
  return (
    <Container className={classNames('', style.container)}>
      <OneShotNotification />

      <Section className="p-2">
        <HomeBanner1 />
      </Section>

      <Section className="p-2">
        <CatalogSlider
          title="Our Dogs"
          pets={getHomePageDogData()}
        />
      </Section>

      <Section className="p-2">
        <CatalogSlider
          title="Our Cats"
          pets={getHomePageCatData()}
        />
      </Section>

      <Section className="p-2">
        <SubscribeNews />
      </Section>
    </Container>
  );
};
