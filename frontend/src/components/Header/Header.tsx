import React, { useState } from 'react';
import { useEffect } from 'react';
import style from './Header.module.scss';
import { v4 as uuidv4 } from 'uuid';
import classNames from 'classnames';
import { Link, useLocation } from 'react-router-dom';

import { Container, Navbar } from 'react-bulma-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faUser,
  faCartShopping,
  faWineBottle,
} from '@fortawesome/free-solid-svg-icons';

import { NavLinks } from '../NavLinks';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { actions as menuActions } from '../../features/mobilMenu';

export const Header = () => {
  const { visible: mobileMenuVisible } = useAppSelector(
    state => state.menuVisible,
  );

  const [favCount, setFavCount] = useState(99);
  const [cartCount, setCartCount] = useState(99);
  const dispatch = useAppDispatch();
  const location = useLocation();

  useEffect(() => onLinkClick(), [location]);

  useEffect(() => {
    window.addEventListener('resize', function () {
      if (document.body.clientWidth > 1024) {
        dispatch(menuActions.setMenuVisibility(false));
      }
    });
  }, []);

  function onLinkClick() {
    dispatch(menuActions.setMenuVisibility(false));
  }

  return (
    <Navbar className="mx-6 mt-2">
      <Navbar.Brand>
        <a
          className={classNames(' p-0 ')}
          href="/"
        >
          <img
            src="icons/header-logo.png"
            className={style.logo_image}
          />
        </a>

        <a
          role="button"
          className="navbar-burger"
          aria-label="menu"
          aria-expanded="false"
          data-target="navbarStore"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </Navbar.Brand>

      <Navbar.Menu>
        <Navbar.Container align="left">
          <Navbar.Item href="/">
            <Navbar.Link arrowless>
              <span className={style.header_txt}>Home</span>
            </Navbar.Link>
          </Navbar.Item>

          <Navbar.Item
            href="#"
            hoverable
          >
            <Navbar.Link>
              <span className={style.header_txt}>Shop All</span>
            </Navbar.Link>

            <Navbar.Dropdown>
              <Navbar.Item href="#">
                <Navbar.Link arrowless>Red Wine</Navbar.Link>
              </Navbar.Item>

              <Navbar.Item href="#">
                <Navbar.Link arrowless>White Wine</Navbar.Link>
              </Navbar.Item>
            </Navbar.Dropdown>
          </Navbar.Item>

          <Navbar.Item href="/">
            <Navbar.Link arrowless>
              <span className={style.header_txt}>Discounted</span>
            </Navbar.Link>
          </Navbar.Item>
        </Navbar.Container>

        <Navbar.Container align="right">
          <Navbar.Item
            href="/"
            className="px-3"
          >
            <Navbar.Link
              arrowless
              to="/"
              onClick={onLinkClick}
              className={classNames(
                'navbar-item my-0 p-1',
                style.custom_hover,
                style.link_container,
              )}
            >
              <span
                className={classNames(
                  'icon-text has-text-link',
                  'is-align-items-center',
                  'is-flex-direction-column',
                  style.icon_text_header,
                )}
              >
                <span className={classNames('icon')}>
                  <FontAwesomeIcon
                    icon={faWineBottle}
                    size="3x"
                    className={classNames('has-text-black')}
                  />
                </span>
                <span className={classNames('has-text-black')}>Favorite</span>
              </span>

              {favCount > 0 && (
                <div className={style.container_count}>
                  <span className={style.count}>{49}</span>
                </div>
              )}
            </Navbar.Link>
          </Navbar.Item>

          <Navbar.Item
            href="/"
            hoverable
            className="px-3"
          >
            <Navbar.Link
              arrowless
              to="/"
              onClick={onLinkClick}
              className={classNames(
                'navbar-item my-0 p-1',
                style.custom_hover,
                style.link_container,
              )}
            >
              <span
                className={classNames(
                  'icon-text has-text-link',
                  'is-align-items-center',
                  'is-flex-direction-column',
                  style.icon_text_header,
                )}
              >
                <span className={classNames('icon')}>
                  <FontAwesomeIcon
                    icon={faUser}
                    size="2x"
                    className={classNames('has-text-black')}
                  />
                </span>
                <span className={classNames('has-text-black')}>User</span>
              </span>
            </Navbar.Link>

            <Navbar.Dropdown right>
              <Navbar.Item href="#">
                <Navbar.Link arrowless>Login</Navbar.Link>
              </Navbar.Item>

              <Navbar.Item href="#">
                <Navbar.Link arrowless>Signup</Navbar.Link>
              </Navbar.Item>
            </Navbar.Dropdown>
          </Navbar.Item>

          <Navbar.Item
            href="/"
            className="px-3"
          >
            <Navbar.Link
              arrowless
              to="/"
              onClick={onLinkClick}
              className={classNames(
                'navbar-item my-0 p-1',
                style.custom_hover,
                style.link_container,
              )}
            >
              <span
                className={classNames(
                  'icon-text has-text-link',
                  'is-align-items-center',
                  'is-flex-direction-column',
                  style.icon_text_header,
                  style.custom_hover,
                )}
              >
                <span className={classNames('icon')}>
                  <FontAwesomeIcon
                    icon={faCartShopping}
                    size="2x"
                    className={classNames('has-text-black')}
                  />
                </span>
                <span className={classNames('has-text-black')}>Cart</span>
              </span>

              {cartCount > 0 && (
                <div className={style.container_count}>
                  <span className={style.count}>{49}</span>
                </div>
              )}
            </Navbar.Link>
          </Navbar.Item>
        </Navbar.Container>
      </Navbar.Menu>
    </Navbar>
  );
};
