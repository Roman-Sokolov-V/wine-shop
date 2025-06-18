import React, { useEffect, useState } from 'react';
import 'react-calendar/dist/Calendar.css';
import { Container, Section } from 'react-bulma-components';
import { SubscribeNews } from '../../components/SubscribeNews';
import { OneShotNotification } from '../../components/OneShotNotification';
import classNames from 'classnames';
import style from './HomePage.module.scss';
import { HomeBanner1 } from '../../components/HomeBanner1';
import { CatalogSlider } from '../../components/CatalogSlider';
import { useAppSelector } from '../../app/hooks';
import { Pet } from '../../types/Pet';
import { filterPetBy, getRandomSampleFromArray } from '../../utils/helperPet';

export const HomePage = () => {
  const { pets } = useAppSelector(state => state.pet);
  const [dogs, setDogs] = useState<Pet[]>([]);
  const [cats, setCats] = useState<Pet[]>([]);
  useEffect(() => {
    setDogs(
      getRandomSampleFromArray(
        filterPetBy(pets, 'pet_type' as keyof Pet, 'dog'),
        10,
      ),
    );
    setCats(
      getRandomSampleFromArray(
        filterPetBy(pets, 'pet_type' as keyof Pet, 'cat'),
        10,
      ),
    );
  }, [pets]);

  return (
    <Container className={classNames('', style.container)}>
      <OneShotNotification />

      <Section className="p-2">
        <HomeBanner1 />
      </Section>

      <Section className="p-2">
        <CatalogSlider
          title="Our Dogs"
          pets={dogs}
        />
      </Section>

      <Section className="p-2">
        <CatalogSlider
          title="Our Cats"
          pets={cats}
        />
      </Section>

      <Section className="p-2">
        <SubscribeNews />
      </Section>
    </Container>
  );
};
