import React, { useState } from 'react';
import { useEffect } from 'react';
import style from './Header.module.scss';
import classNames from 'classnames';
import { Link, useNavigate } from 'react-router-dom';

import { Button, Navbar } from 'react-bulma-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faPaw } from '@fortawesome/free-solid-svg-icons';

import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { actions as menuActions } from '../../features/mobilMenu';

export const Header = () => {
  const { visible: mobileMenuVisible } = useAppSelector(
    state => state.menuVisible,
  );
  const navigate = useNavigate();
  const [favCount, setFavCount] = useState(99);
  const dispatch = useAppDispatch();

  useEffect(() => {
    window.addEventListener('resize', function () {
      if (document.body.clientWidth > 1024) {
        dispatch(menuActions.setMenuVisibility(false));
      }
    });
  }, []);

  function onLinkClick(pth: string) {
    dispatch(menuActions.setMenuVisibility(false));
    navigate(pth);
  }

  return (
    <Navbar
      className={classNames('mx-2', style.header, {
        [style.full_page]: mobileMenuVisible,
      })}
      active={mobileMenuVisible}
    >
      <Navbar.Brand className="mr-5">
        <a
          className={classNames('is-flex is-align-items-center', {
            [style.custom_hover]: !mobileMenuVisible,
          })}
          href="/"
          onClick={() => onLinkClick('/')}
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
          onClick={() => dispatch(menuActions.toggle())}
        >
          <span
            aria-hidden="true"
            className="has-text-black"
          ></span>

          <span
            aria-hidden="true"
            className="has-text-black"
          ></span>

          <span
            aria-hidden="true"
            className="has-text-black"
          ></span>

          <span
            aria-hidden="true"
            className="has-text-black"
          ></span>
        </a>
      </Navbar.Brand>

      <Navbar.Menu
        className={classNames({ [style.full_page]: mobileMenuVisible })}
      >
        <Navbar.Container
          align="left"
          className=""
        >
          <Navbar.Item
            className=""
            onClick={() => onLinkClick('/')}
          >
            <Button
              rounded
              className={style.header_txt}
            >
              Home
            </Button>
          </Navbar.Item>

          <Navbar.Item
            className=""
            hoverable
            onClick={() => onLinkClick('/animals')}
          >
            <Button rounded>
              <Navbar.Link
                arrowless
                // arrowless={mobileMenuVisible}
                className={classNames('', style.header_txt)}
              >
                Animals
              </Navbar.Link>
            </Button>

            {!mobileMenuVisible && (
              <>
                <Navbar.Dropdown>
                  <Navbar.Item href="#">
                    <Navbar.Link arrowless>
                      <Link to="/">Cats</Link>
                    </Navbar.Link>
                  </Navbar.Item>

                  <Navbar.Item href="#">
                    <Navbar.Link arrowless>
                      <Link to="/">Dogs</Link>
                    </Navbar.Link>
                  </Navbar.Item>

                  <Navbar.Item href="#">
                    <Navbar.Link arrowless>
                      <Link to="/">Other animals</Link>
                    </Navbar.Link>
                  </Navbar.Item>
                </Navbar.Dropdown>
              </>
            )}
          </Navbar.Item>

          <Navbar.Item
            className="pr-4"
            onClick={() => onLinkClick('/how-to-help')}
          >
            <Button
              rounded
              className={style.header_txt}
            >
              How to help
            </Button>
          </Navbar.Item>
        </Navbar.Container>

        <Navbar.Container
          align="right"
          className=""
        >
          <Navbar.Item
            className={classNames('navbar-item', {
              [style.custom_hover]: !mobileMenuVisible,
              [style.header_txt]: mobileMenuVisible,
            })}
            onClick={() => onLinkClick('/favorites')}
          >
            {!mobileMenuVisible ? (
              <Navbar.Link
                arrowless
                className="p-0"
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
                      icon={faPaw}
                      size="3x"
                      className={classNames('has-text-black')}
                    />
                  </span>
                  <span className={classNames('has-text-black')}>Favorite</span>
                </span>

                {favCount > 0 && !mobileMenuVisible && (
                  <div className={style.container_count}>
                    <span className={style.count}>{49}</span>
                  </div>
                )}
              </Navbar.Link>
            ) : (
              <Button
                rounded
                className={style.header_txt}
              >
                Favoties
              </Button>
            )}
          </Navbar.Item>

          <Navbar.Item
            hoverable
            onClick={() => onLinkClick('/account')}
          >
            {!mobileMenuVisible ? (
              <>
                <Navbar.Link
                  arrowless
                  className={classNames('p-0', {
                    [style.custom_hover]: !mobileMenuVisible,
                    [style.header_txt]: mobileMenuVisible,
                  })}
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

                    <span className={classNames('has-text-black')}>
                      Account
                    </span>
                  </span>
                </Navbar.Link>

                <Navbar.Dropdown right>
                  <Navbar.Item>
                    <Navbar.Link arrowless>
                      <Link to="/login">Login</Link>
                    </Navbar.Link>
                  </Navbar.Item>

                  <Navbar.Item href="#">
                    <Navbar.Link arrowless>
                      <Link to="/signup">Signup</Link>
                    </Navbar.Link>
                  </Navbar.Item>
                </Navbar.Dropdown>
              </>
            ) : (
              <Button
                rounded
                className={style.header_txt}
              >
                Account
              </Button>
            )}
          </Navbar.Item>
        </Navbar.Container>
      </Navbar.Menu>
    </Navbar>
  );
};
