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
import classNames from 'classnames';
import { toggle as toggleFavote } from '../../features/favorites';
import * as FavoriteAction from '../../features/favorites';
import { useNavigate } from 'react-router-dom';
import { updatePetsApi } from '../../api/pets';
import { PetInfoSwiper } from '../../components/PetInfoSwiper';
import { randomImageGenerator } from '../../utils/helperPet';
import { ModalSuccess } from '../../components/ModalSuccess';

interface AppointmentFormData {
  name: string;
  email: string;
  phone: string;
  date: string;
  message?: string;
}

export const PetInfoPage = () => {
  const { favorites } = useAppSelector(state => state.favorite);
  const { loggedIn } = useAppSelector(state => state.auth);

  const dispatch = useAppDispatch();
  const location = useLocation();
  const [pet, setPet] = useState<Pet | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
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
      })
      .catch((e: AxiosError) => {
        setError(`Failed to fetch pet details: ${e.message}`);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [id]);

  const handleAppointmentSubmit = (formData: AppointmentFormData): void => {
    //Todo: Add API call when BE ready
    // eslint-disable-next-line no-console
    console.log('Appointment request submitted:', formData);
    setSuccess(
      'Appointment request submitted, someone will contact you to confirm appoitment.',
    );
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

  if (success) {
    return (
      <ModalSuccess
        isActive
        title="Succsess"
        body={success}
        onClose={() => setSuccess('')}
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
          <div>
            <PetInfoSwiper
              images={pet?.images}
              //TODO: delete for production
              // images={randomImageGenerator(20)}
              petType={pet.pet_type}
            />
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
                  dispatch(FavoriteAction.toggle(pet.id));

                  if (loggedIn) {
                    updatePetsApi(favorites).catch(() =>
                      console.error('Error toggling favorites'),
                    );
                  }
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
