export interface Filters {
  pet_type?: string[];
  minAge?: number | null;
  maxAge?: number | null;
  breed?: string[];
  sex?: string[];
  coloration?: string[];
  weightMin?: number | null;
  weightMax?: number | null;
  isSterilized?: string[];
}

export interface FilterAPIResponce {
  pet_type: string[];
  breed: string[];
  coloration: string[];
  is_sterilized: string[];
  age_max: number;
  age_min: number;
  sex: string[];
  weight_max: number;
  weight_min: number;
}
