export default function FormInput({ label, name, value, onChange, type = 'text', placeholder = '' }) {
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
        className="form-input"
        autoComplete="off"
      />
    </div>
  )
}
