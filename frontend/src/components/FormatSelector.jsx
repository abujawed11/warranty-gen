export default function FormatSelector({ value, onChange }) {
  return (
    <div className="format-selector-bar">
      <span className="format-selector-label">Certificate Format:</span>
      <label className={`format-option${value === 'format1' ? ' format-option--active' : ''}`}>
        <input type="radio" name="certificateFormat" value="format1" checked={value === 'format1'} onChange={onChange} />
        Format 1 — Standard
      </label>
      <label className={`format-option${value === 'format2' ? ' format-option--active' : ''}`}>
        <input type="radio" name="certificateFormat" value="format2" checked={value === 'format2'} onChange={onChange} />
        Format 2 — Detailed Project
      </label>
    </div>
  )
}
