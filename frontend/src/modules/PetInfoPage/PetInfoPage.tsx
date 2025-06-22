import React, { useEffect, useMemo, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { getPetById } from '../../api/pets';
import { Pet } from '../../types/Pet';
import { ModalError } from '../../components/ModalError';
import { ModalLoader } from '../../components/ModalLoader';
import { AxiosError } from 'axios';
import {
  Box,
  Button,
  Columns,
  Content,
  Heading,
  Image,
} from 'react-bulma-components';
import style from './PetInfoPage.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faPaw,
  faWeightScale,
  faPalette,
  faCheckCircle,
  faTimesCircle,
  faHeart,
} from '@fortawesome/free-solid-svg-icons';
import { AppointmentModal } from '../../components/AppointmentModal';

import { useAppDispatch, useAppSelector } from '../../app/hooks';
import * as FavoriteAction from '../../features/favorites';
import classNames from 'classnames';

interface AppointmentFormData {
  name: string;
  email: string;
  phone: string;
  date: string;
  message?: string;
}

export const PetInfoPage = () => {
  const { favorites } = useAppSelector(state => state.favorite);
  const dispatch = useAppDispatch();
  const location = useLocation();
  const [pet, setPet] = useState<Pet | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeImage, setActiveImage] = useState('');
  const [isAppointmentModalOpen, setIsAppointmentModalOpen] = useState(false);

  const inFav = useMemo(
    () => pet?.id !== undefined && favorites.includes(pet.id),
    [pet, favorites],
  );

  const id = useMemo(() => {
    return location.pathname.split('/').slice(-1)[0];
  }, [location]);

  useEffect(() => {
    setLoading(true);

    getPetById(id)
      .then(res => {
        const petData = res?.data as Pet;
        setPet(petData);
        // Set the first image as active, or a placeholder if none exist
        setActiveImage(() => {
          if (petData.images && petData.images.length > 0) {
            return petData.images[0];
          }
          if (petData.pet_type === 'dog') {
            return '/assets/dog-img-placeholder.png';
          } else if (petData.pet_type === 'cat') {
            return '/assets/cat-img-placeholder.png';
          } else {
            return 'https://placehold.co/400x600?text=Comming+Soon';
          }
        });
      })
      .catch((e: AxiosError) => {
        setError(`Failed to fetch pet details: ${e.message}`);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [id]);

  const handleAppointmentSubmit = (formData: AppointmentFormData): void => {
    // eslint-disable-next-line no-console
    console.log('Appointment request submitted:', formData);
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

  if (!pet) {
    return <p>Pet not found.</p>;
  }

  return (
    <div className={style.pageContainer}>
      <Columns>
        <Columns.Column size="half">
          <div className={style.galleryContainer}>
            <div className={style.mainImageContainer}>
              <Image
                src={activeImage}
                alt={`${pet.name}'s main picture`}
              />
            </div>
            <div className={style.thumbnailContainer}>
              {pet.images &&
                pet.images.map((img, index) => (
                  <div
                    key={index}
                    className={`${style.thumbnail} ${img === activeImage ? style.activeThumbnail : ''}`}
                    onClick={() => setActiveImage(img)}
                  >
                    <Image
                      src={img}
                      alt={`${pet.name}'s thumbnail ${index + 1}`}
                    />
                  </div>
                ))}
            </div>
          </div>
        </Columns.Column>

        <Columns.Column size="half">
          <Content>
            <div className="is-flex is-justify-content-space-between">
              <div>
                <Heading size={1}>{pet.name}</Heading>
                <Heading
                  subtitle
                  size={4}
                >
                  {pet.breed}
                  <span className={style.sexIndicator}>
                    {pet.sex === 'M' ? ' (Male)' : ' (Female)'}
                  </span>
                </Heading>
              </div>

              <Button
                rounded
                onClick={() => {
                  dispatch(FavoriteAction.actions.toggle(pet.id));
                }}
              >
                <FontAwesomeIcon
                  className={classNames({ 'has-text-danger': inFav })}
                  icon={faHeart}
                  size="2x"
                />
              </Button>
            </div>
            <hr />

            <Box className={style.detailsBox}>
              <div className={style.detailItem}>
                <FontAwesomeIcon
                  icon={faPaw}
                  className="mr-2"
                />
                <strong>Age:</strong> {pet.age} years
              </div>
              <div className={style.detailItem}>
                <FontAwesomeIcon
                  icon={faWeightScale}
                  className="mr-2"
                />
                <strong>Weight:</strong> {pet.weight} kg
              </div>
              <div className={style.detailItem}>
                <FontAwesomeIcon
                  icon={faPalette}
                  className="mr-2"
                />
                <strong>Color:</strong> {pet.coloration}
              </div>
              <div className={style.detailItem}>
                {pet.is_sterilized ? (
                  <FontAwesomeIcon
                    icon={faCheckCircle}
                    className="has-text-success mr-2"
                  />
                ) : (
                  <FontAwesomeIcon
                    icon={faTimesCircle}
                    className="has-text-danger mr-2"
                  />
                )}
                <strong>Sterilized:</strong> {pet.is_sterilized ? 'Yes' : 'No'}
              </div>
            </Box>

            <Heading
              size={5}
              className="mt-5"
            >
              About Me
            </Heading>
            <p>{pet.description}</p>

            <div className={style.actionButtons}>
              <Button
                color="primary"
                size="large"
              >
                Apply to Adopt Me
              </Button>

              <Button
                color="light"
                size="large"
                onClick={() => setIsAppointmentModalOpen(true)}
              >
                Schedule Appointment to see me
              </Button>
            </div>
          </Content>
        </Columns.Column>
      </Columns>

      <AppointmentModal
        isOpen={isAppointmentModalOpen}
        onClose={() => setIsAppointmentModalOpen(false)}
        petName={pet.name}
        onSubmit={handleAppointmentSubmit}
      />
    </div>
  );
};
