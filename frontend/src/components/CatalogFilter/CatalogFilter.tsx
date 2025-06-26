import React, { useState } from 'react';
import { Filters } from '../../types/Filters';

type Props = {
  filterData: Filters;
  onChange: (selectedFilters: Filters) => void;
};

const initialSelectedFilters: Filters = {
  pet_type: [],
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
  const [selectedFilters, setSelectedFilters] = useState<Filters>(
    initialSelectedFilters,
  );
  console.log('========', filterData);

  const handleCheckboxChange = (field: keyof Filters, value: string) => {
    const currentValues = selectedFilters[field] as string[];
    const newValues = currentValues.includes(value)
      ? currentValues.filter(item => item !== value)
      : [...currentValues, value];

    setSelectedFilters({ ...selectedFilters, [field]: newValues });
  };

  const handleNumberChange = (field: keyof Filters, value: string) => {
    const numericValue = value === '' ? null : parseInt(value, 10);
    setSelectedFilters({ ...selectedFilters, [field]: numericValue });
  };

  const handleMultiSelectChange = (
    field: keyof Filters,
    e: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    const selectedOptions = Array.from(
      e.target.selectedOptions,
      option => option.value,
    );
    setSelectedFilters({ ...selectedFilters, [field]: selectedOptions });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onChange(selectedFilters);
  };

  const handleReset = () => {
    setSelectedFilters(initialSelectedFilters);
    onChange(initialSelectedFilters);
  };

  if (!filterData) {
    return <div className="box">Loading filters...</div>;
  }

  return (
    <div className="box">
      <p className="title is-5">Filters</p>
      <form onSubmit={handleSubmit}>
        <div className="field">
          <label className="label">Type of Pet</label>
          <div className="control">
            {(filterData.pet_type || []).map(type => (
              <label
                className="checkbox mr-4"
                key={type}
              >
                <input
                  type="checkbox"
                  checked={
                    selectedFilters.pet_type
                      ? selectedFilters.pet_type.includes(type)
                      : false
                  }
                  onChange={() => handleCheckboxChange('pet_type', type)}
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
              <p className="control">
                <input
                  className="input"
                  type="number"
                  placeholder="Min"
                  value={selectedFilters.minAge ?? ''}
                  onChange={e => handleNumberChange('minAge', e.target.value)}
                />
              </p>
            </div>
            <div className="field">
              <p className="control">
                <input
                  className="input"
                  type="number"
                  placeholder="Max"
                  value={selectedFilters.maxAge ?? ''}
                  onChange={e => handleNumberChange('maxAge', e.target.value)}
                />
              </p>
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
                value={selectedFilters.breed}
                onChange={e => handleMultiSelectChange('breed', e)}
              >
                {(filterData.breed || []).map(breed => (
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
            <div className="select is-multiple is-fullwidth">
              <select
                multiple
                size={5}
                value={selectedFilters.coloration}
                onChange={e => handleMultiSelectChange('coloration', e)}
              >
                {(filterData.coloration || []).map(color => (
                  <option
                    key={color}
                    value={color}
                  >
                    {color}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="field">
          <label className="label">Sex</label>
          <div className="control">
            {(filterData.sex || []).map(sexOption => (
              <label
                className="checkbox mr-4"
                key={sexOption}
              >
                <input
                  type="checkbox"
                  checked={
                    selectedFilters.sex
                      ? selectedFilters.sex.includes(sexOption)
                      : false
                  }
                  onChange={() => handleCheckboxChange('sex', sexOption)}
                />
                {` ${sexOption}`}
              </label>
            ))}
          </div>
        </div>

        <div className="field">
          <label className="label">Sterilized</label>
          <div className="control">
            {(filterData.isSterilized || []).map(option => (
              <label
                className="checkbox mr-4"
                key={option}
              >
                <input
                  type="checkbox"
                  checked={
                    selectedFilters.isSterilized
                      ? selectedFilters.isSterilized.includes(option)
                      : false
                  }
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
              <p className="control">
                <input
                  className="input"
                  type="number"
                  placeholder="Min"
                  value={selectedFilters.weightMin ?? ''}
                  onChange={e =>
                    handleNumberChange('weightMin', e.target.value)
                  }
                />
              </p>
            </div>
            <div className="field">
              <p className="control">
                <input
                  className="input"
                  type="number"
                  placeholder="Max"
                  value={selectedFilters.weightMax ?? ''}
                  onChange={e =>
                    handleNumberChange('weightMax', e.target.value)
                  }
                />
              </p>
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
