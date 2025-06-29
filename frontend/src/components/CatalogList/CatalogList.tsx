import React from 'react';
import { Pet } from '../../types/Pet';
import { CatalogCard } from '../CatalogCard';
import { Heading } from 'react-bulma-components';

interface Props {
  pets: Pet[];
}
export const CatalogList: React.FC<Props> = ({ pets }) => {
  if (pets.length === 0) {
    return <Heading>No pets found</Heading>;
  }

  return (
    <div
      className="grid is-col-min-9 is-gap-2"
      style={{ width: '100%' }}
    >
      {pets.map((itm, indx) => {
        return (
          <div
            key={indx}
            className="cell"
          >
            <CatalogCard petData={itm} />
          </div>
        );
      })}
    </div>
  );
};
