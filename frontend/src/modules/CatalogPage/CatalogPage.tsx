import React, { useEffect, useMemo, useState } from 'react';
import { Pet } from '../../types/Pet';
import { ModalError } from '../../components/ModalError';
import { ModalLoader } from '../../components/ModalLoader';
import { CatalogList } from '../../components/CatalogList';
import { CatalogViewSetter } from '../../components/CatalogViewSetter';
import { CatalogFilter } from '../../components/CatalogFilter';
import { Columns, Pagination } from 'react-bulma-components';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { useSearchParams } from 'react-router-dom';
import { QueryNames, SortOrder } from '../../types/ViewControlle';
import * as PetsAction from '../../features/pets';
import { Filters } from '../../types/Filters';
import { getPetsAvailableFilters } from '../../api/pets';
import { Axios, AxiosError, AxiosResponse } from 'axios';

const filterKeys: (keyof Filters)[] = [
  'pet_type',
  'minAge',
  'maxAge',
  'breed',
  'sex',
  'coloration',
  'weightMin',
  'weightMax',
  'isSterilized',
];

function genPages(items: Pet[], perPage: string) {
  if (perPage === 'all') {
    return [items];
  }
  const parsedCount = parseInt(perPage);
  if (parsedCount <= 0 || typeof parsedCount !== 'number') {
    console.warn("Invalid 'perPage' value. Defaulting to 1.");
    return [items];
  }

  const pages = [];
  const totalItems = items.length;

  const numPages = Math.ceil(totalItems / parsedCount);

  for (let i = 0; i < numPages; i++) {
    const startIndex = i * parsedCount;
    const endIndex = startIndex + parsedCount;

    const page = items.slice(startIndex, endIndex);
    pages.push(page);
  }
  return pages;
}

export const CatalogPage = () => {
  const { filteredPets } = useAppSelector(state => state.pet);
  const dispatch = useAppDispatch();

  const [searchParams, setSearchParams] = useSearchParams();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const currentPage = parseInt(
    searchParams.get(QueryNames.CUR_PAGE) || '1',
    10,
  );
  const itemsPerPage = searchParams.get(QueryNames.PER_PAGE) || '10';

  const [availableFilters, setAvailableFilters] = useState<Filters>({
    pet_type: [],
    minAge: 0,
    maxAge: 99,
    breed: [],
    sex: ['Male', 'Female', 'Unknown'],
    coloration: [],
    weightMin: 0,
    weightMax: 999,
    isSterilized: ['Yes', 'No', 'Unknown'],
  });

  useEffect(() => {
    const fetchFilters = async () => {
      setLoading(true);
      try {
        const res = await getPetsAvailableFilters();
        const data = res?.data;
        if (data) {
          setAvailableFilters({
            pet_type: data.pet_type,
            minAge: data.age_min,
            maxAge: data.age_max,
            breed: data.breed,
            sex: data.sex,
            coloration: data.coloration,
            weightMin: data.weight_min,
            weightMax: data.weight_max,
            isSterilized: data.is_sterilized,
          });
        }
      } catch (error: unknown) {
        if (error && typeof error === 'object' && 'message' in error) {
          setError((error as { message?: string }).message || 'Unknown error');
        } else {
          setError('Unknown error');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchFilters();
  }, []);

  const pages = useMemo(() => {
    return genPages(filteredPets, itemsPerPage);
  }, [filteredPets, itemsPerPage]);

  const petsToShow = pages[currentPage - 1] || [];

  useEffect(() => {
    const query = searchParams.get(QueryNames.QUERY) || '';
    const sortOrder =
      (searchParams.get(QueryNames.SORTED) as SortOrder) || 'acc';
    const currentFilters: Partial<Filters> = {};

    for (const key of filterKeys) {
      const values = searchParams.getAll(key);
      if (values.length > 0) {
        // Handle single number values vs multi-value arrays
        if (
          key === 'minAge' ||
          key === 'maxAge' ||
          key === 'weightMin' ||
          key === 'weightMax'
        ) {
          currentFilters[key] = parseInt(values[0], 10);
        } else {
          currentFilters[key] = values;
        }
      }
    }
    console.log('000000', currentFilters);
    dispatch(PetsAction.actions.search(query));
    dispatch(PetsAction.actions.sortFiltered(sortOrder));
    dispatch(PetsAction.actions.applyFilter(currentFilters as Filters));
  }, [searchParams, dispatch]);

  function handleQueryChange(newQuery: string) {
    const newParams = new URLSearchParams(searchParams);
    newParams.set(QueryNames.QUERY, newQuery);
    newParams.set(QueryNames.CUR_PAGE, '1');
    setSearchParams(newParams);
  }

  function handleFilterChange(filters: Filters) {
    const newParams = new URLSearchParams(searchParams);
    for (const key of Object.keys(availableFilters)) {
      newParams.delete(key);
    }

    for (const [key, value] of Object.entries(filters)) {
      if (Array.isArray(value) && value.length > 0) {
        value.forEach(item => {
          newParams.append(key, item);
        });
      } else if (!Array.isArray(value) && value !== null) {
        newParams.set(key, String(value));
      }
    }

    newParams.set(QueryNames.CUR_PAGE, '1');
    setSearchParams(newParams);
  }

  function handleSortChange(newOrder: SortOrder) {
    const newParams = new URLSearchParams(searchParams);
    newParams.set(QueryNames.SORTED, newOrder);
    setSearchParams(newParams);
  }

  function handlePerPageChange(newPerPage: string | number) {
    const newParams = new URLSearchParams(searchParams);
    newParams.set(QueryNames.PER_PAGE, newPerPage.toString());
    newParams.set(QueryNames.CUR_PAGE, '1');
    setSearchParams(newParams);
  }

  function handlePageChange(newPage: number) {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    const newParams = new URLSearchParams(searchParams);
    newParams.set(QueryNames.CUR_PAGE, String(newPage));
    setSearchParams(newParams);
  }

  return (
    <div>
      {!!error && (
        <ModalError
          title="Error"
          body={error}
          onClose={() => setError('')}
        />
      )}

      {loading && <ModalLoader />}

      <Columns className="mt-3">
        <Columns.Column size="one-quarter">
          <CatalogFilter
            filterData={availableFilters}
            onChange={handleFilterChange}
          />
        </Columns.Column>

        <Columns.Column>
          <div className="mb-5">
            <CatalogViewSetter
              onPerPage={handlePerPageChange}
              onSearch={handleQueryChange}
              onSort={handleSortChange}
            />
          </div>

          <CatalogList pets={petsToShow} />

          <div className="my-2">
            <Pagination
              total={pages.length - 1}
              current={currentPage}
              delta={2}
              next=">"
              previous="<"
              showPrevNext
              autoHide
              showFirstLast
              size="small"
              align="center"
              onChange={e => {
                handlePageChange(e);
              }}
              rounded
            />
          </div>
        </Columns.Column>
      </Columns>
    </div>
  );
};
