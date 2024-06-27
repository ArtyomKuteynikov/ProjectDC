import React from 'react';
import './SearchForm.css'

const SearchForm = ({ handleSubmit, inputValue, onInputChange, isShort, onCheckboxChange }) => {
  return (
    <form 
      action="/" 
      onSubmit={handleSubmit} 
      name="search-form" 
      noValidate 
      className="search-form"
    >
      <div className='search-form__input-area'>
        <label className="search-form__field">
          <input
            id="search-input"
            type="text"
            name="search-input"
            placeholder="Фильм"
            value={inputValue}
            onChange={onInputChange}
            required
            className="search-form__input"
          />
          <span className="search-form-input-error"></span>
        </label>
        <button type="submit" className="search-form__button"></button>
      </div>
      <label className='search-form__field-checkbox'>
        <input 
          id="search-input-checkbox"
          type='checkbox' 
          name="search-checkbox"
          value={isShort}
          checked={isShort}
          onChange={onCheckboxChange}
          required
          className="search-form__checkbox"
        />
        <div className="search-form__visible-checkbox"></div>
        <span className='search-form__checkbox-description'>Короткометражки</span>
      </label>
    </form>
  )
}

export default SearchForm;
