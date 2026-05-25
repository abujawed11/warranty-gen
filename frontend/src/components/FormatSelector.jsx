import { useState } from 'react'

export default function FormatSelector({ value, onChange }) {
  const [warrantyOpen, setWarrantyOpen] = useState(
    value === 'format1' || value === 'format2'
  )

  const isWarrantyActive = value === 'format1' || value === 'format2'
  const isTestActive = value === 'format3'

  function handleWarrantyClick() {
    setWarrantyOpen(true)
    if (value === 'format3') {
      onChange({ target: { name: 'certificateFormat', value: '' } })
    }
  }

  function handleTestClick() {
    setWarrantyOpen(false)
    onChange({ target: { name: 'certificateFormat', value: 'format3' } })
  }

  function handleSubFormat(fmt) {
    onChange({ target: { name: 'certificateFormat', value: fmt } })
  }

  return (
    <div className="cert-type-selector">
      <p className="cert-type-heading">Select Certificate Type</p>
      <div className="cert-type-cards">

        {/* Warranty Certificate */}
        <div
          className={`cert-type-card${warrantyOpen ? ' cert-type-card--open' : ''}${isWarrantyActive ? ' cert-type-card--active' : ''}`}
        >
          <button type="button" className="cert-type-card-header" onClick={handleWarrantyClick}>
            <span className="cert-type-card-text">
              <span className="cert-type-card-title">Warranty Certificate</span>
              <span className="cert-type-card-subtitle">Format 1 &amp; Format 2 available</span>
            </span>
            <span className="cert-type-card-chevron">{warrantyOpen ? '▲' : '▼'}</span>
          </button>

          {warrantyOpen && (
            <div className="cert-subformats">
              <button
                type="button"
                className={`cert-subformat-btn${value === 'format1' ? ' cert-subformat-btn--active' : ''}`}
                onClick={() => handleSubFormat('format1')}
              >
                <span className="cert-subformat-name">Format 1</span>
                <span className="cert-subformat-desc">Standard</span>
              </button>
              <button
                type="button"
                className={`cert-subformat-btn${value === 'format2' ? ' cert-subformat-btn--active' : ''}`}
                onClick={() => handleSubFormat('format2')}
              >
                <span className="cert-subformat-name">Format 2</span>
                <span className="cert-subformat-desc">Detailed Project</span>
              </button>
            </div>
          )}
        </div>

        {/* Test Certificate */}
        <div
          className={`cert-type-card${isTestActive ? ' cert-type-card--active' : ''}`}
        >
          <button type="button" className="cert-type-card-header" onClick={handleTestClick}>
            <span className="cert-type-card-text">
              <span className="cert-type-card-title">Test Certificate</span>
              <span className="cert-type-card-subtitle">Chemical &amp; mechanical properties</span>
            </span>
            {isTestActive && <span className="cert-type-card-check">&#10003;</span>}
          </button>
        </div>

      </div>
    </div>
  )
}
