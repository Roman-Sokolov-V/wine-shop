import React from 'react';
import style from './CatalogSlider.module.scss';
import { Heading } from 'react-bulma-components';

import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination, Navigation, Scrollbar, A11y } from 'swiper/modules';
import { SliderCard } from './SliderCard';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import { Pet } from '../../types/Pet';

interface Props {
  title: string;
  pets: Pet[];
}

export const CatalogSlider: React.FC<Props> = ({ title, pets }) => {
  return (
    <div className={style.container}>
      <Heading>{title}</Heading>
      <Swiper
        modules={[Navigation, Pagination, Scrollbar, A11y]}
        className={style.container__swiper}
        spaceBetween={50}
        slidesPerView={3}
        navigation
        pagination={{ clickable: true }}
        scrollbar={{ draggable: true }}
      >
        {pets.map(pet => {
          return (
            <SwiperSlide key={pet.id}>
              <SliderCard petData={pet} />
            </SwiperSlide>
          );
        })}
      </Swiper>
    </div>
  );
};
