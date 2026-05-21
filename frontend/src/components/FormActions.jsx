export default function FormActions({ onDownload }) {
  return (
    <div className="form-actions">
      <button type="submit" className="btn btn-primary">
        <span className="btn-icon">&#128065;</span>
        Preview Certificate
      </button>
      <button type="button" className="btn btn-secondary" onClick={onDownload}>
        <span className="btn-icon">⬇</span>
        Download Certificate
      </button>
    </div>
  )
}
