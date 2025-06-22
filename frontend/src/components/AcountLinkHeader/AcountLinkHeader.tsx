import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import classNames from 'classnames';
import { Button, Navbar } from 'react-bulma-components';
import { useNavigate } from 'react-router-dom';
import { useAppSelector } from '../../app/hooks';
import style from './AcountLinkHeader.module.scss';
import { faUser } from '@fortawesome/free-solid-svg-icons';
import { useDispatch } from 'react-redux';
import { actions as AuthAction } from '../../features/authentication';

export const AcountLinkHeader = () => {
  const naviagate = useNavigate();
  const dispatch = useDispatch();
  const { visible: mobileMenuVisible } = useAppSelector(
    state => state.menuVisible,
  );
  const { loggedIn } = useAppSelector(state => state.auth);

  function handleLogout() {
    dispatch(AuthAction.logout());
    naviagate('/');
  }

  if (loggedIn) {
    return (
      <>
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
                <span
                  className={classNames('icon')}
                  onClick={() => naviagate('/account')}
                >
                  <FontAwesomeIcon
                    icon={faUser}
                    size="2x"
                    className={classNames('has-text-black')}
                  />
                </span>

                <span className={classNames('has-text-black')}>Account</span>
              </span>
            </Navbar.Link>

            <Navbar.Dropdown right>
              <Navbar.Item onClick={() => naviagate('/account')}>
                <Navbar.Link arrowless>Account</Navbar.Link>
              </Navbar.Item>

              <Navbar.Item onClick={handleLogout}>
                <Navbar.Link arrowless>Logout</Navbar.Link>
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
      </>
    );
  }

  return (
    <>
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
              <span
                className={classNames('icon')}
                onClick={() => naviagate('/account')}
              >
                <FontAwesomeIcon
                  icon={faUser}
                  size="2x"
                  className={classNames('has-text-black')}
                />
              </span>

              <span className={classNames('has-text-black')}>Account</span>
            </span>
          </Navbar.Link>

          <Navbar.Dropdown right>
            <Navbar.Item onClick={() => naviagate('/login')}>
              <Navbar.Link arrowless>Login</Navbar.Link>
            </Navbar.Item>

            <Navbar.Item onClick={() => naviagate('/register')}>
              <Navbar.Link arrowless>Register</Navbar.Link>
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
    </>
  );
};
