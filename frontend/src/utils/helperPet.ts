import { Filters } from '../types/Filters';
import { Pet } from '../types/Pet';

//TODO: this for debuggging, delet for production
export function randomImageGenerator(quantity: number) {
  // An array of possible words to use in the image text
  const textOptions = [
    'Sky',
    'Nature',
    'Forest',
    'Mountain',
    'River',
    'Beach',
    'Desert',
    'City',
    'Tech',
    'Code',
    'Future',
    'Explore',
    'Art',
    'Music',
    'Food',
    'Travel',
    'Animal',
    'Abstract',
    'Minimal',
    'Creative',
  ];

  const generatedUrls = [];

  // Loop 'quantity' times to create the specified number of URLs
  for (let i = 0; i < quantity; i++) {
    // Generate a random width between 300 and 800
    const width = Math.floor(Math.random() * 2001) + 100;

    // Generate a random height between 300 and 800
    const height = Math.floor(Math.random() * 2001) + 1000;

    // Select a random word from the textOptions array
    const randomText =
      textOptions[Math.floor(Math.random() * textOptions.length)];

    // Construct the URL with the random parameters
    const imageUrl = `https://placehold.co/${width}x${height}?text=${encodeURIComponent(randomText)}`;

    // Add the generated URL to our array
    generatedUrls.push(imageUrl);
  }

  return generatedUrls;
}

function capitalizeFirstLetter(str: string) {
  if (str.length === 0) {
    return ''; // Handle empty strings
  }
  return str.charAt(0).toUpperCase() + str.slice(1);
}

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

  const filted = pets.filter(pet => {
    const bulkTxt = Object.values(pet).join(' ').toLocaleLowerCase();
    return bulkTxt.includes(query.toLocaleLowerCase());
  });

  return filted;
}

export function getAvaliableFilters(data: Pet[]): Filters {
  if (!data.length) {
    return {
      pet_type: [],
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
    pet_type: Array.from(
      new Set(data.map(itm => capitalizeFirstLetter(itm.pet_type))),
    ),
    minAge: Math.min(...data.map(itm => itm.age)),
    maxAge: Math.max(...data.map(itm => itm.age)),
    breed: Array.from(
      new Set(data.map(itm => capitalizeFirstLetter(itm.breed))),
    ),
    sex: ['Male', 'Female', 'Unknown'],
    coloration: Array.from(
      new Set(data.map(itm => capitalizeFirstLetter(itm.coloration))),
    ),
    weightMin: Math.min(...data.map(itm => itm.weight)),
    weightMax: Math.max(...data.map(itm => itm.weight)),
    isSterilized: ['Yes', 'No', 'Unknown'],
  };
}

export function getRandomSampleFromArray<T>(inputArray: T[], quantity: number) {
  if (inputArray.length <= quantity) {
    return [...inputArray];
  } else {
    const shuffled = [...inputArray];

    let currentIndex = shuffled.length;
    let randomIndex;

    while (currentIndex !== 0) {
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;

      [shuffled[currentIndex], shuffled[randomIndex]] = [
        shuffled[randomIndex],
        shuffled[currentIndex],
      ];
    }

    return shuffled.slice(0, quantity);
  }
}
