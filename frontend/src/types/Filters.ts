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
