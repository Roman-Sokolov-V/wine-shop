import {
  // faUser,
  // faCircleQuestion,
  faDoorOpen,
  // faCampground,
  // faPeopleGroup,
  faEnvelope,
  faHouseUser,
  faRightFromBracket,
} from '@fortawesome/free-solid-svg-icons';
// import { faCoffee, faEy } from '@fortawesome/free-brands-svg-icons';
// import { faCoffee, faEy } from '@fortawesome/free-regular-svg-icons';

export const MENU_LINKS_NO_AUTH = [
  {
    name: 'Categoty 1',
    icon: faDoorOpen,
    link: '/',
  },
  {
    name: 'Categoty 2',
    icon: faDoorOpen,
    link: '/',
  },
  {
    name: 'Categoty 3',
    icon: faDoorOpen,
    link: '/',
  },
  {
    name: 'Categoty 4',
    icon: faDoorOpen,
    link: '/',
  },
  {
    name: 'Login',
    icon: faHouseUser,
    link: '/account',
  },
  {
    name: 'Contact Us',
    icon: faEnvelope,
    link: '/contact-us',
  },
];

export const MENU_LINKS_AUTH = [
  {
    name: 'Categoty 1',
    icon: faDoorOpen,
    link: '/',
  },
  {
    name: 'Categoty 2',
    icon: faDoorOpen,
    link: '/',
  },
  {
    name: 'Categoty 3',
    icon: faDoorOpen,
    link: '/',
  },
  {
    name: 'Categoty 4',
    icon: faDoorOpen,
    link: '/',
  },
  {
    name: 'Log out',
    icon: faRightFromBracket,
    link: '/logout',
  },
  {
    name: 'Account',
    icon: faHouseUser,
    link: '/account',
  },
  {
    name: 'Contact Us',
    icon: faEnvelope,
    link: '/contact-us',
  },
];
