import React from 'react';
import './Articles.css'

const Articles = () => {
  const links = {
    "Эффективный поиск работы в 2024 - Habr": "https://habr.com/ru/articles/790304/",
    "В поисках лучшего работодателя - HH": "https://hh.ru/article/32883?hhtmFrom=article_applicants_job-search_list",
    "Востребованный способ поиска работы - CyberLeninka": "https://cyberleninka.ru/article/n/naibolee-vostrebovannyy-sposob-poiska-raboty-v-rossii",
  };
  return (
    <div className='articles'>
      <h3 className='articles__header'>Интересные статьи</h3>
      <ul className='articles__list'>
        {
          Object.keys(links).map(key => (
            <li 
              className='articles__list-item'
              key={key}
            >
              <a 
                href={links[key]} 
                target="_blank" 
                rel="noreferrer"
                className='articles__link'
              >
                {key}
                <span className='articles__link-arrow'>↗</span>
              </a>
            </li>
          ))
        }
      </ul>
      
    </div>
  );
}

export default Articles
