import { Pet } from '../types/Pet';

export function filterPetBy(pets: Pet[], filterName: keyof Pet, value: string) {
  if (pets.length === 0) {
    return [];
  }
  if (!Object.keys(pets[0]).includes(filterName)) {
    return pets;
  }

  const filteredPets = pets.filter(pet => pet[filterName] === value);

  return filteredPets;
}

export function searchPets(pets: Pet[], query: string) {
  if (!query || !pets) {
    return [];
  }

  return pets.filter(pet => {
    const bulkTxt = Object.values(pet).join(' ').toLocaleLowerCase();
    return bulkTxt.includes(query.toLocaleLowerCase());
  });
}

export function getAvaliableFilters(data: Pet[]) {
  if (!data.length) {
    return {
      type: [],
      minAge: 0,
      maxAge: 99,
      breed: [],
      sex: ['Male', 'Female', 'Unknown'],
      coloration: [],
      weightMin: 0,
      weightMax: 999,
      isSterilized: ['Yes', 'No', 'Unknown'],
    };
  }
  return {
    type: Array.from(new Set(data.map(itm => itm.pet_type))),
    minAge: Math.min(...data.map(itm => itm.age)),
    maxAge: Math.max(...data.map(itm => itm.age)),
    breed: Array.from(new Set(data.map(itm => itm.breed))),
    sex: ['Male', 'Female', 'UnKnown'],
    coloration: Array.from(new Set(data.map(itm => itm.coloration))),
    weightMin: Math.min(...data.map(itm => itm.weight)),
    weightMax: Math.max(...data.map(itm => itm.weight)),
    isSterilized: ['Yes', 'No', 'Unknown'],
  };
}
