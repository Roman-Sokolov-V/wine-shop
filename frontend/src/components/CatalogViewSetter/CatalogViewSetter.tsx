import React, { useState } from 'react';
import {
  faAngleDown,
  faSearch,
  faXmark,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import classNames from 'classnames';
import { Button, Dropdown } from 'react-bulma-components';
import { PageSize, SortOrder } from '../../types/ViewControlle';

interface Props {
  onSort: (order: SortOrder) => void;
  onPerPage: (num: PageSize) => void;
  onSearch: (query: string) => void;
}

export const CatalogViewSetter: React.FC<Props> = ({
  onSort,
  onPerPage,
  onSearch,
}) => {
  const [query, setQuery] = useState<string>('');

  return (
    <div className="is-flex">
      <div>
        <Dropdown
          icon={
            <FontAwesomeIcon
              icon={faAngleDown}
              className={classNames('has-text-black pl-1')}
            />
          }
          label="Sort"
          closeOnSelect
          onChange={(e: SortOrder) => onSort(e)}
          className="mr-5"
        >
          <Dropdown.Item
            renderAs="a"
            value="acc"
          >
            Accendign
          </Dropdown.Item>

          <Dropdown.Item
            renderAs="a"
            value="dec"
          >
            Decending
          </Dropdown.Item>
        </Dropdown>

        <Dropdown
          icon={
            <FontAwesomeIcon
              icon={faAngleDown}
              className={classNames('has-text-black pl-1')}
            />
          }
          label="Pets Per Page"
          closeOnSelect
          onChange={(e: PageSize) => onPerPage(e)}
          className="ml-5"
        >
          <Dropdown.Item
            renderAs="a"
            value={5}
          >
            5
          </Dropdown.Item>

          <Dropdown.Item
            renderAs="a"
            value={10}
          >
            10
          </Dropdown.Item>

          <Dropdown.Item
            renderAs="a"
            value={15}
          >
            15
          </Dropdown.Item>

          <Dropdown.Item
            renderAs="a"
            value={25}
          >
            25
          </Dropdown.Item>

          <Dropdown.Item
            renderAs="a"
            value="all"
          >
            All
          </Dropdown.Item>
        </Dropdown>
      </div>

      <div className="field is-flex has-addons ml-5 is-flex-grow-1 is-align-items-center">
        <Button
          className={classNames('icon is-small is-left mr-1', {
            'is-invisible': !query,
          })}
          color="danger"
          colorVariant="light"
          rounded
          style={{ height: '90%', width: '36px' }}
          onClick={() => {
            setQuery('');
            onSearch('');
          }}
        >
          <FontAwesomeIcon
            icon={faXmark}
            size="2x"
            className={classNames('pl-1')}
          />
        </Button>
        <p className="control has-icons-left is-flex-grow-1">
          <input
            className="input"
            type="text"
            placeholder="Seach here"
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter') {
                onSearch(query);
                return;
              }
              if (e.key === 'Escape') {
                setQuery('');
                onSearch('');
                return;
              }
            }}
          />
          <span className="icon is-small is-left">
            <FontAwesomeIcon
              icon={faSearch}
              className={classNames(' pl-1')}
            />
          </span>
        </p>

        <div className="control">
          <button
            onClick={() => onSearch(query)}
            className="button is-primary"
          >
            Search
          </button>
        </div>
      </div>
    </div>
  );
};
