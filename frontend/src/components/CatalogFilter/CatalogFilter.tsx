import React, { useEffect, useState } from 'react';

export interface FilterProps {
  type: string[];
  minAge: number | null;
  maxAge: number | null;
  breed: string[];
  sex: string[];
  coloration: string[];
  weightMin: number | null;
  weightMax: number | null;
  isSterilized: string[];
}

type Props = {
  filterData: FilterProps;
  onChange: (fltr: FilterProps) => void;
};

const initialFilterState: FilterProps = {
  type: [],
  minAge: null,
  maxAge: null,
  breed: [],
  sex: [],
  coloration: [],
  weightMin: null,
  weightMax: null,
  isSterilized: [],
};

export const CatalogFilter: React.FC<Props> = ({ filterData, onChange }) => {
  const [filter, setFilter] = useState<FilterProps>(initialFilterState);

  useEffect(() => {
    if (filterData) {
      setFilter(filterData);
    }
  }, [filterData]);

  // Toggles a value in a string array (for checkboxes).
  const handleCheckboxChange = (field: keyof FilterProps, value: string) => {
    const currentValues = filter[field] as string[];
    const newValues = currentValues.includes(value)
      ? currentValues.filter(item => item !== value) // Remove if it exists
      : [...currentValues, value]; // Add if it doesn't

    setFilter({ ...filter, [field]: newValues });
  };

  // Updates a number field, converting empty strings to null.
  const handleNumberChange = (field: keyof FilterProps, value: string) => {
    const numericValue = value === '' ? null : parseInt(value, 10);
    setFilter({ ...filter, [field]: numericValue });
  };

  // Handles the multi-select dropdown for breeds.
  const handleMultiSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedBreeds = Array.from(
      e.target.selectedOptions,
      option => option.value,
    );
    setFilter({ ...filter, breed: selectedBreeds });
  };

  // Handles text input for comma-separated values like 'coloration'.
  const handleArrayInputChange = (field: keyof FilterProps, value: string) => {
    const newValues = value
      .split(',')
      .map(s => s.trim())
      .filter(Boolean);
    setFilter({ ...filter, [field]: newValues });
  };

  // --- Handlers to communicate with the parent component ---

  // When the form is submitted, call the parent's onChange with the new filters.
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onChange(filter);
  };

  // Reset the local form and notify the parent of the reset.
  const handleReset = () => {
    setFilter(initialFilterState);
    onChange(initialFilterState);
  };

  return (
    <div className="box">
      <p className="title is-5">Filters</p>
      <form onSubmit={handleSubmit}>
        <div className="field">
          <label className="label">Type of Pet</label>
          <div className="control">
            {filter.type.map(type => (
              <label
                className="checkbox mr-4"
                key={type}
              >
                <input
                  type="checkbox"
                  checked={filter.type.includes(type)}
                  onChange={() => handleCheckboxChange('type', type)}
                />
                {` ${type}`}
              </label>
            ))}
          </div>
        </div>

        <div className="field">
          <label className="label">Age Range (Years)</label>
          <div className="field-body">
            <div className="field">
              <div className="control">
                <input
                  className="input"
                  type="number"
                  placeholder="Min"
                  value={filter.minAge ?? ''}
                  onChange={e => handleNumberChange('minAge', e.target.value)}
                />
              </div>
            </div>
            <div className="field">
              <div className="control">
                <input
                  className="input"
                  type="number"
                  placeholder="Max"
                  value={filter.maxAge ?? ''}
                  onChange={e => handleNumberChange('maxAge', e.target.value)}
                />
              </div>
            </div>
          </div>
        </div>

        <div className="field">
          <label className="label">Breed</label>
          <div className="control">
            <div className="select is-multiple is-fullwidth">
              <select
                multiple
                size={5}
                value={filter.breed}
                onChange={handleMultiSelectChange}
                style={{ width: '100%' }}
              >
                {filter.breed.map(breed => (
                  <option
                    key={breed}
                    value={breed}
                  >
                    {breed}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="field">
          <label className="label">Coloration</label>
          <div className="control">
            <input
              className="input"
              type="text"
              placeholder="e.g. Black, White, Golden"
              value={filter.coloration.join(', ')}
              onChange={e =>
                handleArrayInputChange('coloration', e.target.value)
              }
            />
          </div>
          <p className="help">Enter colors separated by commas</p>
        </div>

        <div className="field">
          <label className="label">Sex</label>
          <div className="control">
            {filter.sex.map(sex => (
              <label
                className="checkbox mr-4"
                key={sex}
              >
                <input
                  type="checkbox"
                  checked={filter.sex.includes(sex)}
                  onChange={() => handleCheckboxChange('sex', sex)}
                />
                {` ${sex}`}
              </label>
            ))}
          </div>
        </div>

        <div className="field">
          <label className="label">Sterilized</label>
          <div className="control">
            {filter.isSterilized.map(option => (
              <label
                className="checkbox mr-4"
                key={option}
              >
                <input
                  type="checkbox"
                  checked={filter.isSterilized.includes(option)}
                  onChange={() => handleCheckboxChange('isSterilized', option)}
                />
                {` ${option}`}
              </label>
            ))}
          </div>
        </div>

        <div className="field">
          <label className="label">Weight Range (kg)</label>
          <div className="field-body">
            <div className="field">
              <div className="control">
                <input
                  className="input"
                  type="number"
                  placeholder="Min"
                  value={filter.weightMin ?? ''}
                  onChange={e =>
                    handleNumberChange('weightMin', e.target.value)
                  }
                />
              </div>
            </div>
            <div className="field">
              <div className="control">
                <input
                  className="input"
                  type="number"
                  placeholder="Max"
                  value={filter.weightMax ?? ''}
                  onChange={e =>
                    handleNumberChange('weightMax', e.target.value)
                  }
                />
              </div>
            </div>
          </div>
        </div>

        <div className="field is-grouped mt-5">
          <div className="control is-expanded">
            <button
              className="button is-primary is-fullwidth"
              type="submit"
            >
              Apply Filters
            </button>
          </div>
          <div className="control is-expanded">
            <button
              className="button is-fullwidth"
              type="button"
              onClick={handleReset}
            >
              Reset
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};
