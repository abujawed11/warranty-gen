export default function CertificatePreview({ data }) {
  const rows = [
    { label: 'Billing Customer Name', value: data.billingCustomerName },
    { label: 'Billing Customer Address', value: data.billingCustomerAddress },
    { label: 'Shipping Customer Name', value: data.shippingCustomerName },
    { label: 'Shipping Customer Address', value: data.shippingCustomerAddress },
    { label: 'Date of Dispatch', value: data.dateOfDispatch },
    { label: 'Invoice / PO Number', value: data.invoicePONumber },
    { label: 'Warranty Period', value: data.warrantyPeriod },
    { label: 'Material Part Name', value: data.materialPartName },
    { label: 'Quantity (kWp)', value: data.quantityKWp },
    { label: 'Remarks', value: data.remarks },
  ]

  return (
    <div className="preview-card">
      <div className="preview-header">
        <div className="preview-header-left">
          <div className="preview-logo-placeholder">SUNRACK</div>
          <div className="preview-tagline">Solar Mounting Solutions</div>
        </div>
        <div className="preview-header-right">
          <h2 className="preview-title">WARRANTY CERTIFICATE</h2>
        </div>
      </div>

      <div className="preview-section-title">Certificate Details</div>

      <table className="preview-table">
        <tbody>
          {rows.map(({ label, value }) => (
            <tr key={label}>
              <td className="preview-table-label">{label}</td>
              <td className="preview-table-value">{value || <span className="preview-empty">—</span>}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="preview-footer">
        <p>This certificate is issued as a guarantee of product quality and performance.</p>
      </div>
    </div>
  )
}
