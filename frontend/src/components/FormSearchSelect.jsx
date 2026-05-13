import { useState, useRef, useEffect } from 'react'

const COUNTRIES = [
  'Afghanistan','Albania','Algeria','Andorra','Angola','Antigua and Barbuda',
  'Argentina','Armenia','Australia','Austria','Azerbaijan','Bahamas','Bahrain',
  'Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bhutan',
  'Bolivia','Bosnia and Herzegovina','Botswana','Brazil','Brunei','Bulgaria',
  'Burkina Faso','Burundi','Cabo Verde','Cambodia','Cameroon','Canada',
  'Central African Republic','Chad','Chile','China','Colombia','Comoros',
  'Congo (Congo-Brazzaville)','Costa Rica','Croatia','Cuba','Cyprus',
  'Czechia','Denmark','Djibouti','Dominica','Dominican Republic','Ecuador',
  'Egypt','El Salvador','Equatorial Guinea','Eritrea','Estonia','Eswatini',
  'Ethiopia','Fiji','Finland','France','Gabon','Gambia','Georgia','Germany',
  'Ghana','Greece','Grenada','Guatemala','Guinea','Guinea-Bissau','Guyana',
  'Haiti','Honduras','Hungary','Iceland','India','Indonesia','Iran','Iraq',
  'Ireland','Israel','Italy','Jamaica','Japan','Jordan','Kazakhstan','Kenya',
  'Kiribati','Kuwait','Kyrgyzstan','Laos','Latvia','Lebanon','Lesotho',
  'Liberia','Libya','Liechtenstein','Lithuania','Luxembourg','Madagascar',
  'Malawi','Malaysia','Maldives','Mali','Malta','Marshall Islands',
  'Mauritania','Mauritius','Mexico','Micronesia','Moldova','Monaco',
  'Mongolia','Montenegro','Morocco','Mozambique','Myanmar','Namibia','Nauru',
  'Nepal','Netherlands','New Zealand','Nicaragua','Niger','Nigeria',
  'North Korea','North Macedonia','Norway','Oman','Pakistan','Palau',
  'Palestine','Panama','Papua New Guinea','Paraguay','Peru','Philippines',
  'Poland','Portugal','Qatar','Romania','Russia','Rwanda',
  'Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines',
  'Samoa','San Marino','Sao Tome and Principe','Saudi Arabia','Senegal',
  'Serbia','Seychelles','Sierra Leone','Singapore','Slovakia','Slovenia',
  'Solomon Islands','Somalia','South Africa','South Korea','South Sudan',
  'Spain','Sri Lanka','Sudan','Suriname','Sweden','Switzerland','Syria',
  'Taiwan','Tajikistan','Tanzania','Thailand','Timor-Leste','Togo','Tonga',
  'Trinidad and Tobago','Tunisia','Turkey','Turkmenistan','Tuvalu','Uganda',
  'Ukraine','United Arab Emirates','United Kingdom','United States',
  'Uruguay','Uzbekistan','Vanuatu','Vatican City','Venezuela','Vietnam',
  'Yemen','Zambia','Zimbabwe',
]

export default function FormSearchSelect({ label, name, value, onChange }) {
  const [open, setOpen] = useState(false)
  const [query, setQuery] = useState('')
  const containerRef = useRef(null)
  const inputRef = useRef(null)

  const filtered = query.trim()
    ? COUNTRIES.filter(c => c.toLowerCase().includes(query.toLowerCase()))
    : COUNTRIES

  // Close on outside click
  useEffect(() => {
    function handleClick(e) {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setOpen(false)
        setQuery('')
      }
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  function handleSelect(country) {
    onChange({ target: { name, value: country } })
    setOpen(false)
    setQuery('')
  }

  function handleToggle() {
    setOpen(prev => {
      if (!prev) setTimeout(() => inputRef.current?.focus(), 10)
      else setQuery('')
      return !prev
    })
  }

  function handleClear(e) {
    e.stopPropagation()
    onChange({ target: { name, value: '' } })
    setQuery('')
    setOpen(false)
  }

  return (
    <div className="form-field" ref={containerRef}>
      <label className="form-label">{label}</label>

      {/* Trigger */}
      <div
        className={`search-select-trigger form-input${open ? ' search-select-trigger--open' : ''}`}
        onClick={handleToggle}
        role="combobox"
        aria-expanded={open}
        aria-haspopup="listbox"
        tabIndex={0}
        onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') handleToggle() }}
      >
        <span className={value ? 'search-select-value' : 'search-select-placeholder'}>
          {value || '— Select Country —'}
        </span>
        <span className="search-select-icons">
          {value && (
            <span className="search-select-clear" onClick={handleClear} title="Clear">&#x2715;</span>
          )}
          <svg
          className={`search-select-arrow${open ? ' search-select-arrow--up' : ''}`}
          width="12" height="8" viewBox="0 0 12 8"
          fill="none" xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <path d="M1 1l5 5 5-5" stroke="#9ca3af" strokeWidth="1.5" strokeLinecap="round"/>
        </svg>
        </span>
      </div>

      {/* Dropdown */}
      {open && (
        <div className="search-select-dropdown" role="listbox">
          <div className="search-select-search-wrap">
            <span className="search-select-search-icon">&#128269;</span>
            <input
              ref={inputRef}
              type="text"
              className="search-select-search-input"
              placeholder="Search country..."
              value={query}
              onChange={e => setQuery(e.target.value)}
              onClick={e => e.stopPropagation()}
            />
            {query && (
              <span className="search-select-search-clear" onClick={() => setQuery('')}>&#x2715;</span>
            )}
          </div>
          <ul className="search-select-list">
            {filtered.length === 0 ? (
              <li className="search-select-no-result">No countries found</li>
            ) : (
              filtered.map(country => (
                <li
                  key={country}
                  className={`search-select-option${value === country ? ' search-select-option--selected' : ''}`}
                  onClick={() => handleSelect(country)}
                  role="option"
                  aria-selected={value === country}
                >
                  {country}
                  {value === country && <span className="search-select-check">&#10003;</span>}
                </li>
              ))
            )}
          </ul>
        </div>
      )}
    </div>
  )
}
