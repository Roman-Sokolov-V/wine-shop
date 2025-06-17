import React from 'react';
import { Pet } from '../../types/Pet';
import { CatalogCard } from '../CatalogCard';

interface Props {
  pets: Pet[];
}
export const CatalogList: React.FC<Props> = ({ pets }) => {
  if (!pets) {
    return <></>;
  }

  return (
    <>
      {pets.map((itm, indx) => {
        return (
          <CatalogCard
            key={indx}
            petData={itm}
          />
        );
      })}
    </>
  );
};
