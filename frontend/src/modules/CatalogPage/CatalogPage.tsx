import React, { useEffect, useState } from 'react';
import { Pet } from '../../types/Pet';
import { ModalError } from '../../components/ModalError';
import { ModalLoader } from '../../components/ModalLoader';
import { CatalogList } from '../../components/CatalogList';
import { CatalogViewSetter } from '../../components/CatalogViewSetter';
import { CatalogFilter } from '../../components/CatalogFilter';
import { Columns, Pagination } from 'react-bulma-components';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { useLocation, useSearchParams } from 'react-router-dom';
import { QueryNames, SortOrder } from '../../types/ViewControlle';
import * as PetsAction from '../../features/pets';
import { getAvaliableFilters } from '../../utils/helperPet';

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
  const { pets, filteredPets } = useAppSelector(state => state.pet);
  const dispatch = useAppDispatch();

  const [searchParams, setSearchParams] = useSearchParams();
  const [prevSearchParams, setPrevSearchParams] = useState<string>(
    searchParams.toString(),
  );
  const location = useLocation();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [pages, setPages] = useState<Pet[][]>([]);
  const [curPage, setCurPage] = useState(0);
  const [strQuery, setStrQuery] = useState('');
  const [sorted, setSorted] = useState<SortOrder>('acc');

  const [filters, setFilters] = useState<any>(undefined);
  const [petsToShow, setPetsToShow] = useState<Pet[]>([]);

  useEffect(() => {
    if (!searchParams.get(QueryNames.CUR_PAGE)) {
      updateSearchParams(QueryNames.CUR_PAGE, '1');
    }
    if (!searchParams.get(QueryNames.PER_PAGE)) {
      updateSearchParams(QueryNames.PER_PAGE, '10');
    }
    setFilters(getAvaliableFilters(pets));
    setCurPage(1);
  }, []);

  useEffect(() => {
    const x = new URLSearchParams(prevSearchParams);
    handlePerPageChange(searchParams.get(QueryNames.PER_PAGE));
    handleSortChange(
      (searchParams.get(QueryNames.SORTED) || 'acc') as keyof SortOrder,
    );
    handleSearch(searchParams.get(QueryNames.QUERY) || '');
  }, [searchParams]);

  useEffect(() => {
    // handlePageChange(1);
    setPages(
      genPages(
        filteredPets,
        (searchParams.get(QueryNames.PER_PAGE) ?? '10').toString(),
      ),
    );
  }, [filteredPets]);

  function updateSearchParams(key: string, val: string | number) {
    setPrevSearchParams(searchParams.toString());
    const newSearchParams = new URLSearchParams(searchParams);
    if (!val) {
      newSearchParams.delete(String(key));
      setSearchParams(newSearchParams);
      return;
    }

    newSearchParams.set(key, val.toString());
    setSearchParams(newSearchParams);
  }

  function handleSearch(query: string) {
    dispatch(PetsAction.actions.searchFilted(query));
  }

  function handlePerPageChange(count: string | null) {
    if (!count) {
      setPages(genPages(filteredPets, '10'));
      return;
    }
    setPages(genPages(filteredPets, count));
  }

  function handleSortChange(order: keyof SortOrder) {
    dispatch(PetsAction.actions.sortFiltered(order.toString()));
  }

  function handlePageChange(page: number) {
    window.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
    setCurPage(page);
    updateSearchParams(QueryNames.CUR_PAGE, page.toString());
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

      <Columns>
        <Columns.Column size="one-quarter">
          <CatalogFilter
            filterData={filters}
            onChange={() => {}}
          />
        </Columns.Column>

        <Columns.Column>
          <div className="mb-2">
            <CatalogViewSetter
              onPerPage={val => updateSearchParams(QueryNames.PER_PAGE, val)}
              onSearch={val => updateSearchParams(QueryNames.QUERY, val)}
              onSort={val => updateSearchParams(QueryNames.SORTED, val)}
            />
          </div>

          <CatalogList pets={pages[curPage]} />

          <div className="my-2">
            <Pagination
              total={pages.length - 1}
              current={curPage}
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
