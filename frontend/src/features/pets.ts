import { createSlice } from '@reduxjs/toolkit';
import { accessLocalStorage } from '../utils/accessLocalStorage';
import { LocalAccessKeys } from '../types/LocalAccessKeys';
import { ApiPet, Pet } from '../types/Pet';
import { Filters } from '../types/Filters';
import { searchPets } from '../utils/helperPet';

type Initial = {
  pets: Pet[];
  filteredPets: Pet[];
};
const initialValue: Initial = {
  pets: [],
  filteredPets: [],
};

const PetSlice = createSlice({
  name: 'pet',
  initialState: initialValue,
  reducers: {
    setPets: (state, action: { payload: ApiPet[] }) => {
      const processedPets = action.payload.map(pet => {
        let sex;
        if (pet.sex === 'M') {
          sex = 'Male';
        } else if (pet.sex === 'F') {
          sex = 'Female';
        } else if (pet.sex === 'U') {
          sex = 'Unknown';
        } else {
          sex = pet.sex;
        }

        let is_sterilized;
        if (pet.is_sterilized === true) {
          is_sterilized = 'Yes';
        } else if (pet.is_sterilized === false) {
          is_sterilized = 'No';
        } else {
          is_sterilized = 'Unknown';
        }

        return { ...pet, sex, is_sterilized };
      });
      state.pets = processedPets;
      state.filteredPets = processedPets;
      accessLocalStorage.set(LocalAccessKeys.PETS, action.payload);
    },

    search(state, action: { payload: string }) {
      if (action.payload) {
        const temp = searchPets(state.pets, action.payload);
        state.filteredPets = temp;
      } else {
        state.filteredPets = state.pets;
      }
    },

    sortFiltered(state, action: { payload: string }) {
      if (action.payload === 'acc') {
        state.filteredPets = state.filteredPets
          .slice()
          .toSorted((a, b) => a.name.localeCompare(b.name));
      } else if (action.payload === 'dec') {
        state.filteredPets = state.filteredPets
          .slice()
          .toSorted((a, b) => b.name.localeCompare(a.name));
      }
    },

    applyFilter(state, action: { payload: Filters }) {
      // console.log(action.payload);

      const {
        pet_type,
        minAge,
        maxAge,
        breed,
        sex,
        coloration,
        weightMin,
        weightMax,
        isSterilized,
      }: Filters = action.payload;

      //Pet Type filtering
      if (pet_type && pet_type.length > 0) {
        state.filteredPets = state.filteredPets.filter(pet =>
          pet_type
            .map(i => i.toLocaleLowerCase())
            .includes(pet.pet_type.toLocaleLowerCase()),
        );
      }

      //Pet Min Age filtering
      if (minAge && minAge > 0) {
        state.filteredPets = state.filteredPets.filter(
          pet => pet.age >= minAge,
        );
      }

      //Pet Max Age filtering
      if (maxAge && maxAge > 0) {
        state.filteredPets = state.filteredPets.filter(
          pet => pet.age <= maxAge,
        );
      }

      //Pet breed filtering
      if (breed && breed.length > 0) {
        state.filteredPets = state.filteredPets.filter(pet =>
          breed
            .map(i => i.toLocaleLowerCase())
            .includes(pet.breed.toLocaleLowerCase()),
        );
      }

      //Pet Coloration filtering
      if (coloration && coloration.length > 0) {
        state.filteredPets = state.filteredPets.filter(pet =>
          coloration
            .map(i => i.toLocaleLowerCase())
            .includes(pet.coloration.toLocaleLowerCase()),
        );
      }

      //Pet Sex filtering
      if (sex && sex.length > 0) {
        state.filteredPets = state.filteredPets.filter(pet => {
          return sex.includes(pet.sex);
        });
      }

      //Pet Sterilized filtering
      if (isSterilized && isSterilized.length > 0) {
        state.filteredPets = state.filteredPets.filter(pet =>
          isSterilized.includes(pet.is_sterilized),
        );
      }

      //Pet Min Weight filtering
      if (weightMin && weightMin > 0) {
        state.filteredPets = state.filteredPets.filter(
          pet => pet.weight >= weightMin,
        );
      }

      //Pet Max Weight filtering
      if (weightMax && weightMax > 0) {
        state.filteredPets = state.filteredPets.filter(
          pet => pet.weight <= weightMax,
        );
      }
    },
  },
});

export default PetSlice.reducer;
export const { actions } = PetSlice;
