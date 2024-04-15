import React from 'react';

import NotFoundWebp from '../../assets/404_web.webp'


const PageNotFound: React.FC = () => {
  return (
    <div className='error-page'>
        <img src={NotFoundWebp} alt="Page not found" />
        <h1>Ошибка 404: Страница не найдена</h1>
        <p>К сожалению, запрашиваемый ресурс не существует или находится в разработке</p>
    </div>
  );
}

export default PageNotFound;