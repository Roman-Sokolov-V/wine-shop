import React from 'react';
import style from './SliderCard.module.scss';
import { Pet } from '../../../types/Pet';
import { Button, Heading } from 'react-bulma-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeart } from '@fortawesome/free-solid-svg-icons';

interface Props {
  petData: Pet;
}
export const SliderCard: React.FC<Props> = ({ petData }) => {
  if (!petData) {
    return <></>;
  }
  return (
    <div className={style.container}>
      {/* 1. This container defines the space for the image */}
      <div className={style.cardImageContainer}>
        <img
          src={petData.picture}
          alt={`${petData.name}, a ${petData.breed}`}
        />
      </div>

      <div className={style.cardContent}>
        <Heading size={4}>{petData.name}</Heading>

        <div>
          <p>Bread: {petData.breed}</p>
          <p>Age: {petData.age}</p>
        </div>

        <div className={style.cardActions}>
          <Button
            rounded
            color="primary"
          >
            Adopt
          </Button>
          <Button rounded>
            <FontAwesomeIcon
              icon={faHeart}
              size="lg"
            />
          </Button>
        </div>
      </div>
    </div>
  );
};
