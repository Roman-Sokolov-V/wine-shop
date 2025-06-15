import classNames from 'classnames';
import React from 'react';
import { Button, Heading } from 'react-bulma-components';
import { useNavigate } from 'react-router-dom';
import style from './HomeBanner1.module.scss';

export const HomeBanner1 = () => {
  const navigate = useNavigate();
  return (
    <div className={style.bunnerFirst}>
      <div
        className={classNames(
          'is-flex is-flex-direction-column is-justify-content-space-between p-6',
          style.bunnerFirst__txt_container,
        )}
      >
        <Heading
          co
          className={classNames(
            'is-size-1 has-text-weight-extrabold has-text-secondary',
          )}
        >
          Your New Family Member is Waiting. Adopt.
        </Heading>

        <div className="is-flex is-justify-content-space-between">
          <Button
            rounded
            size="large"
            onClick={() => {
              navigate('/catalog');
            }}
          >
            Adopt
          </Button>

          <Button
            rounded
            size="large"
            onClick={() => {
              navigate('/donate');
            }}
          >
            Suport the cause
          </Button>
        </div>
      </div>
    </div>
  );
};
