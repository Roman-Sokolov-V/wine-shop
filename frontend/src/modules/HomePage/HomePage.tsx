import React from 'react';
import 'react-calendar/dist/Calendar.css';
import { Container, Heading, Section } from 'react-bulma-components';
import { SubscribeNews } from '../../components/SubscribeNews';

export const HomePage = () => {
  return (
    <Container className="px-3">
      <h1 style={{ position: 'absolute', visibility: 'hidden' }}>
        Test Deploy 0.0.1
      </h1>

      <Heading
        className="m-0 mt-3 p-0"
        textAlign="center"
        size={1}
      >
        The Bottle Reserve
      </Heading>

      <Section>
        <div
          className="is-flex"
          style={{ width: '100%', height: '500px' }}
        >
          <Heading className="m-auto">Catalog here</Heading>
        </div>
      </Section>

      <Section>
        <SubscribeNews />
      </Section>
    </Container>
  );
};
