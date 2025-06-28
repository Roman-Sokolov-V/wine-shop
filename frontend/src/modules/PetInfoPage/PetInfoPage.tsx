import React, { useEffect, useMemo, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { getPetById } from '../../api/pets';
import { Pet } from '../../types/Pet';
import { ModalError } from '../../components/ModalError';
import { ModalLoader } from '../../components/ModalLoader';
import { AxiosError } from 'axios';
import { Box, Button, Columns, Content, Heading } from 'react-bulma-components';
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
import * as FavoriteAction from '../../features/favorites';
import { updatePetsApi } from '../../api/pets';
import { PetInfoSwiper } from '../../components/PetInfoSwiper';
import { ModalSuccess } from '../../components/ModalSuccess';
import { PetAdoptionFormModal } from '../../components/PetAdoptionFormModal';
import { AdoptionFormData } from '../../types/AdoptionFormData';
import { submitAdotptionForm, submitAppointmentForm } from '../../api/users';
import { AppointmentFormData } from '../../types/AppointmentFormData';

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
  const [isAdoptionFormModalOpen, setIsAdoptionFormModalOpen] = useState(false);

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
    // eslint-disable-next-line no-console
    console.log('Appointment request submitted:', formData);

    setLoading(true);

    submitAppointmentForm(formData)
      .then(res => {
        if (res?.status === 400) {
          setSuccess(
            'Appointment request submitted, someone will contact you to confirm appoitment.',
          );
        } else {
          throw new Error('uknown error');
        }
      })
      .catch((e: AxiosError) => {
        setError(`Failed to submit appointment form: ${e.message}`);
      })
      .finally(() => {
        setLoading(false);
        setIsAdoptionFormModalOpen(false);
      });
  };

  const handleAdoptionFormSubmit = (formData: AdoptionFormData) => {
    setLoading(true);

    submitAdotptionForm(formData)
      .then(res => {
        if (res?.status === 400) {
          setSuccess('Your form was submited, some will contact you shortly.');
        } else {
          throw new Error('uknown error');
        }
      })
      .catch((e: AxiosError) => {
        setError(`Failed to submit adoption form: ${e.message}`);
      })
      .finally(() => {
        setLoading(false);
        setIsAdoptionFormModalOpen(false);
      });
  };

  if (!pet) {
    return <p>Pet not found.</p>;
  }

  return (
    <div>
      {loading && <ModalLoader />}

      <ModalError
        isActive={!!error}
        title="Error"
        body={error}
        onClose={() => setError('')}
      />

      <ModalSuccess
        isActive={!!success}
        title="Succsess"
        body={success}
        onClose={() => setSuccess('')}
      />

      <PetAdoptionFormModal
        petId={pet.id}
        isActive={isAdoptionFormModalOpen}
        onSubmit={handleAdoptionFormSubmit}
        onClose={() => setIsAdoptionFormModalOpen(false)}
      />

      <AppointmentModal
        isOpen={isAppointmentModalOpen}
        onClose={() => setIsAppointmentModalOpen(false)}
        petName={pet.name}
        onSubmit={handleAppointmentSubmit}
      />

      <div className={style.pageContainer}>
        <Columns>
          <Columns.Column size="half">
            <div>
              <PetInfoSwiper
                images={pet?.images?.map(img => img.file)}
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
                  <strong>Sterilized:</strong>{' '}
                  {pet.is_sterilized ? 'Yes' : 'No'}
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
                  onClick={() => setIsAdoptionFormModalOpen(true)}
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
      </div>
    </div>
  );
};
