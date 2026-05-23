function fmtDate(str) {
  if (!str) return ''
  try {
    return new Date(str + 'T00:00:00').toLocaleDateString('en-IN', {
      day: '2-digit', month: 'long', year: 'numeric',
    })
  } catch { return str }
}

export default function CertificatePreview3({ data }) {
  const refLabel = data.tcRefNumber
    ? `Ref: QUALITY ASSURANCE DEPARTMENT (${data.tcRefNumber})`
    : 'Ref: QUALITY ASSURANCE DEPARTMENT'

  return (
    <div className="cert-preview">

      {/* ── Header ── */}
      <div className="cp-header">
        <div className="cp-header-left">S U N R A C K &nbsp; T E C H N O L O G I E S</div>
        <img src="/logo.svg" alt="Sunrack Logo" className="cp-header-logo-img" />
      </div>
      <div className="cp-divider" />

      {/* ── Ref line ── */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', margin: '8px 0 10px' }}>
        <span style={{ fontWeight: 700, fontSize: '0.78rem', textDecoration: 'underline' }}>{refLabel}</span>
        <span style={{ fontSize: '0.78rem' }}>{fmtDate(data.tcDate)}</span>
      </div>

      {/* ── Info box ── */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #aaa', marginBottom: 12 }}>
        <tbody>
          {/* Title row */}
          <tr>
            <td colSpan={2} style={{ textAlign: 'center', fontWeight: 700, fontSize: '1rem', padding: '6px 0', borderBottom: '1px solid #aaa' }}>
              TEST CERTIFICATE
            </td>
          </tr>

          {/* Customer row */}
          <tr>
            <td colSpan={2} style={{ padding: '6px 8px', borderBottom: '1px solid #aaa', fontSize: '0.78rem', verticalAlign: 'top' }}>
              <div style={{ fontWeight: 700 }}>CUSTOMER:</div>
              {data.tcCustomerName && <div style={{ fontWeight: 700 }}>{data.tcCustomerName}</div>}
              {data.tcCustomerAddress && (
                <div style={{ whiteSpace: 'pre-line' }}>{data.tcCustomerAddress}</div>
              )}
              {data.tcCustomerGstin && <div>GSTIN {data.tcCustomerGstin}</div>}
              {data.tcProjectName && <div>Project Name: {data.tcProjectName}</div>}
            </td>
          </tr>

          {/* Supplier + PO row */}
          <tr>
            <td style={{ width: '55%', padding: '6px 8px', fontSize: '0.78rem', verticalAlign: 'top', borderRight: '1px solid #aaa' }}>
              <div style={{ fontWeight: 700 }}>SUPPLIER</div>
              {data.tcSupplierName && <div style={{ fontWeight: 700 }}>{data.tcSupplierName},</div>}
              {data.tcSupplierAddress && <div>{data.tcSupplierAddress}</div>}
              {data.tcSupplierGstin && <div>GSTIN: {data.tcSupplierGstin}</div>}
            </td>
            <td style={{ width: '45%', padding: 0, fontSize: '0.78rem', verticalAlign: 'top' }}>
              <div style={{ padding: '5px 8px', borderBottom: '1px solid #aaa', fontWeight: 700 }}>
                P.O. No.: {data.tcPoNumber || ''}
              </div>
              <div style={{ padding: '5px 8px', borderBottom: '1px solid #aaa' }}>
                PO Date : {fmtDate(data.tcPoDate)}
              </div>
              <div style={{ padding: '5px 8px' }}>
                Dispatch Date : {fmtDate(data.tcDispatchDate)}
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      {/* ── Material table ── */}
      <div className="cp-section-heading">Details of Material Supplied:</div>
      <table className="cp-material-table">
        <thead>
          <tr>
            <th className="cp-mat-th cp-mat-th--num">#</th>
            <th className="cp-mat-th">PART NAME</th>
            <th className="cp-mat-th">QTY(kWp)</th>
            <th className="cp-mat-th">Remark's</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="cp-mat-td cp-mat-td--center">1</td>
            <td className="cp-mat-td cp-mat-td--center">{data.tcMaterialPartName || '—'}</td>
            <td className="cp-mat-td cp-mat-td--center">{data.tcQuantityKWp || '—'}</td>
            <td className="cp-mat-td cp-mat-td--center">{data.tcRemarks || '—'}</td>
          </tr>
        </tbody>
      </table>

      {/* ── Chemical Composition ── */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #aaa', marginTop: 10, fontSize: '0.75rem' }}>
        <tbody>
          <tr>
            <td style={{ width: 28, borderRight: '1px solid #aaa', borderBottom: '1px solid #aaa', padding: '4px 6px' }} />
            <td colSpan={5} style={{ fontWeight: 700, padding: '4px 6px', borderBottom: '1px solid #aaa' }}>
              Required / Actual Chemical Composition (In %)
            </td>
          </tr>
          <tr style={{ fontWeight: 700, background: '#fff' }}>
            {['#', 'Elements', 'Si', 'Mg', 'Fe', 'Other', 'Al'].map((h, i) => (
              <td key={h} style={{ padding: '4px 6px', borderBottom: '1px solid #aaa', borderRight: i < 6 ? '1px solid #aaa' : 'none', textAlign: i >= 2 ? 'center' : 'left' }}>{h}</td>
            ))}
          </tr>
          <tr>
            {['1', 'Actual Values', data.tcSi, data.tcMg, data.tcFe, data.tcOther, data.tcAl].map((v, i) => (
              <td key={i} style={{ padding: '4px 6px', borderRight: i < 6 ? '1px solid #aaa' : 'none', textAlign: i >= 2 ? 'center' : 'left' }}>{v || '—'}</td>
            ))}
          </tr>
        </tbody>
      </table>

      {/* ── Mechanical Properties ── */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #aaa', marginTop: 8, fontSize: '0.75rem' }}>
        <tbody>
          <tr style={{ fontWeight: 700 }}>
            {['#', 'Mechanical Properties', 'B.H.N', 'H.V 10'].map((h, i) => (
              <td key={h} style={{ padding: '4px 6px', borderBottom: '1px solid #aaa', borderRight: i < 3 ? '1px solid #aaa' : 'none', textAlign: i >= 2 ? 'center' : 'left', width: i === 0 ? 28 : 'auto' }}>{h}</td>
            ))}
          </tr>
          <tr>
            {['1', 'Hardness Actual Values', data.tcBHN, data.tcHV10].map((v, i) => (
              <td key={i} style={{ padding: '4px 6px', borderRight: i < 3 ? '1px solid #aaa' : 'none', textAlign: i >= 2 ? 'center' : 'left' }}>{v || '—'}</td>
            ))}
          </tr>
        </tbody>
      </table>

      {/* ── Signature block ── */}
      <div className="cp-signature-block">
        <p className="cp-for-sunrack">For Sunrack Technologies</p>
        <img src="/Test_certificate_logo.png" alt="Authorised Signatory" className="cp-signature-img" />
        <p className="cp-auth-text">Authorised Signatory</p>
      </div>

      {/* ── Note ── */}
      <p style={{ fontSize: '0.75rem', margin: '8px 0 4px' }}>Note: Material conforms to IS: 733 – 1983</p>

      {/* ── Footer ── */}
      <div className="cp-footer-bar">
        <span>SUNRACK TECHNOLOGIES LLP</span>
        <span>BOISAR, PALGHAR</span>
      </div>

    </div>
  )
}
