import React from 'react';
import 'react-calendar/dist/Calendar.css';
import { Button, Container, Heading, Section } from 'react-bulma-components';
import { SubscribeNews } from '../../components/SubscribeNews';
import { OneShotNotification } from '../../components/OneShotNotification';
import classNames from 'classnames';
import style from './HomePage.module.scss';

export const HomePage = () => {
  return (
    <Container className={classNames('', style.container)}>
      <OneShotNotification />

      <Section className={style.bunnerFirst}>
        <div style={{ width: '100%', height: '500px' }}>
          <div
            className={classNames(
              'is-flex is-flex-direction-column is-justify-content-space-between',
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
              >
                Adopt
              </Button>

              <Button
                rounded
                size="large"
              >
                Suport the cause
              </Button>
            </div>
          </div>
        </div>
      </Section>

      <Section>
        <SubscribeNews />
      </Section>
    </Container>
  );
};
