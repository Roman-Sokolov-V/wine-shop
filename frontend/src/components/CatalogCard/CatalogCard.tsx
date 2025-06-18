import React, { useEffect, useState } from 'react';
import style from './CatalogCard.module.scss';
import { Pet } from '../../types/Pet';
import { Button, Heading } from 'react-bulma-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeart } from '@fortawesome/free-solid-svg-icons';

interface Props {
  petData: Pet;
}
export const CatalogCard: React.FC<Props> = ({ petData }) => {
  const [picture, setPicture] = useState('');

  useEffect(() => {
    if (petData.images.length < 1) {
      if (petData.pet_type === 'dog') {
        setPicture('/assets/dog-img-placeholder.png');
      } else if (petData.pet_type === 'cat') {
        setPicture('/assets/cat-img-placeholder.png');
      } else {
        setPicture('https://placehold.co/400x600?text=Comming+Soon');
      }
    } else {
      setPicture(petData.images[0]);
    }
  }, [petData]);
  if (!petData) {
    return <></>;
  }
  return (
    <div className={style.container}>
      <div className={style.cardImageContainer}>
        <img
          src={
            picture ? picture : 'https://placehold.co/400x600?text=Comming+Soon'
          }
          alt={`${petData.name}, a ${petData.breed}`}
        />
      </div>

      <div className={style.cardContent}>
        <Heading size={4}>{petData.name}</Heading>

        <div>
          <p>{petData.breed}</p>
          <p>{petData.age}</p>
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
