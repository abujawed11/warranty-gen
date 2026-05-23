import CertificatePreview from './CertificatePreview'
import CertificatePreview2 from './CertificatePreview2'
import CertificatePreview3 from './CertificatePreview3'

export default function PreviewSection({ form, onClose }) {
  return (
    <div className="preview-section">
      <div className="preview-section-header">
        <h2>Certificate Preview</h2>
        <button className="btn-close" onClick={onClose} aria-label="Close preview">&#x2715;</button>
      </div>
      {form.certificateFormat === 'format2' && <CertificatePreview2 data={form} />}
      {form.certificateFormat === 'format3' && <CertificatePreview3 data={form} />}
      {form.certificateFormat === 'format1' && <CertificatePreview  data={form} />}
    </div>
  )
}
