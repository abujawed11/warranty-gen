export default function FormInput({ label, name, value, onChange, type = 'text', placeholder = '', disabled = false }) {
  return (
    <div className="form-field">
      <label className="form-label" htmlFor={name}>{label}</label>
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        disabled={disabled}
        className={`form-input${disabled ? ' form-input--disabled' : ''}`}
        autoComplete="off"
      />
    </div>
  )
}
