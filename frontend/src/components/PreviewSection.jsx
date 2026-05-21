import CertificatePreview from './CertificatePreview'
import CertificatePreview2 from './CertificatePreview2'

export default function PreviewSection({ form, onClose }) {
  return (
    <div className="preview-section">
      <div className="preview-section-header">
        <h2>Certificate Preview</h2>
        <button className="btn-close" onClick={onClose} aria-label="Close preview">&#x2715;</button>
      </div>
      {form.certificateFormat === 'format2'
        ? <CertificatePreview2 data={form} />
        : <CertificatePreview data={form} />
      }
    </div>
  )
}
