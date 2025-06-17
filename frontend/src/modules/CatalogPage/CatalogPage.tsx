import React, { useEffect, useState } from 'react';
import { getFilters, getPetDataAsync } from '../../api/pets';
import { Pet } from '../../types/Pet';
import { ModalError } from '../../components/ModalError';
import { ModalLoader } from '../../components/ModalLoader';
import { CatalogList } from '../../components/CatalogList';
import { CatalogViewSetter } from '../../components/CatalogViewSetter';
import { CatalogFilter } from '../../components/CatalogFilter';
import { Pagination } from 'react-bulma-components';
import { current } from '@reduxjs/toolkit';

export const CatalogPage = () => {
  const [petData, setPetData] = useState<Pet[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [curPage, setCurPage] = useState(1);
  const [filters, setFilters] = useState<any>(undefined);

  useEffect(() => {
    setLoading(true);
    getPetDataAsync()
      .then(res => setPetData(res as Pet[]))
      .catch(e => setError(e))
      .finally(() => {
        setLoading(false);
      });

    setLoading(true);
    getFilters()
      .then(res => setFilters(res as any))
      .catch(e => setError(e))
      .finally(() => {
        setLoading(false);
      });
  }, []);

  function handleSearch(query) {
    console.log(query);
  }

  function handlePerPageChange(count) {
    console.log(count);
  }

  function handleSortChange(order) {
    console.log(order);
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

      <div>
        <div>
          <CatalogViewSetter
            onPerPage={handlePerPageChange}
            onSearch={handleSearch}
            onSort={handleSortChange}
          />
        </div>

        <div>
          <CatalogFilter
            filterData={filters}
            onChange={() => {}}
          />
        </div>
        <div>
          <CatalogList pets={petData} />
        </div>
        <div>
          <Pagination
            total={100}
            current={curPage}
            delta={2}
            next=">"
            previous="<"
            showPrevNext
            autoHide
            showFirstLast
            size="small"
            align="center"
            onChange={e => setCurPage(e)}
            rounded
          />
        </div>
      </div>
    </div>
  );
};
