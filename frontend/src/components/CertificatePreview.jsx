function AddressBlock({ address, state, pincode, country }) {
  const parts = [address, state, pincode, country].filter(Boolean)
  return parts.length ? parts.join(', ') : <span className="preview-empty">—</span>
}

export default function CertificatePreview({ data }) {
  const certRows = [
    { label: 'Date of Dispatch', value: data.dateOfDispatch },
    { label: 'Invoice / PO Number', value: data.invoicePONumber },
    { label: 'Warranty Period', value: data.warrantyPeriod },
  ]

  const materialRows = [
    { label: 'Material Part Name', value: data.materialPartName },
    { label: 'Quantity (kWp)', value: data.quantityKWp },
    { label: 'Remarks', value: data.remarks },
  ]

  return (
    <div className="preview-card">

      {/* Header */}
      <div className="preview-header">
        <div className="preview-header-left">
          <div className="preview-logo-placeholder">SUNRACK</div>
          <div className="preview-tagline">Solar Mounting Solutions</div>
        </div>
        <div className="preview-header-right">
          <h2 className="preview-title">WARRANTY CERTIFICATE</h2>
        </div>
      </div>

      {/* Customer groups */}
      <div className="preview-customer-groups">

        <div className="preview-customer-block">
          <div className="preview-customer-heading">
            <span className="group-dot group-dot--yellow" /> Billing Customer
          </div>
          <p className="preview-customer-name">{data.billingCustomerName || <span className="preview-empty">—</span>}</p>
          <p className="preview-customer-address">
            <AddressBlock
              address={data.billingAddress}
              state={data.billingState}
              pincode={data.billingPincode}
              country={data.billingCountry}
            />
          </p>
        </div>

        <div className="preview-customer-divider" />

        <div className="preview-customer-block">
          <div className="preview-customer-heading">
            <span className="group-dot group-dot--black" /> Shipping Customer
          </div>
          <p className="preview-customer-name">{data.shippingCustomerName || <span className="preview-empty">—</span>}</p>
          <p className="preview-customer-address">
            <AddressBlock
              address={data.shippingAddress}
              state={data.shippingState}
              pincode={data.shippingPincode}
              country={data.shippingCountry}
            />
          </p>
        </div>

      </div>

      {/* Certificate details */}
      <div className="preview-section-title">Certificate Details</div>
      <table className="preview-table">
        <tbody>
          {certRows.map(({ label, value }) => (
            <tr key={label}>
              <td className="preview-table-label">{label}</td>
              <td className="preview-table-value">{value || <span className="preview-empty">—</span>}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Material details */}
      <div className="preview-section-title">Material Supplied</div>
      <table className="preview-table">
        <tbody>
          {materialRows.map(({ label, value }) => (
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
