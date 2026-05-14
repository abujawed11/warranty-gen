const TERMS = [
  `M/s Sunrack Technologies, only provides the warranty against manufacturing defects and workmanship on the products supplied. Sunrack will, at its option, either repair the defect or replace the defective product or part there of with a new or remanufactured equivalent at cost within 15 working days of intimation.`,
  `Sunrack's total liability here under for such repair of replacement shall not exceed the original purchase price of the product. This will not provide the warranty replacements for structure products going faulty while operating due to conditions beyond specifications, improper installation, improper site conditions and/or act of god, cosmetic damage, damage from accident, negligence same shall not be covered under warranty and the service would be provided on chargeable basis as per mutual agreement`,
  `Any failure/damage arising out of improper unloading, stacking or moving to the site will not be covered under warranty.`,
  `In the event of any non-payment issues, this warranty becomes null and void. Shall also be void if the product has been modified, repaired, or reworked in a manner not previously authorized by Sunrack in writing.`,
  `Warranty shall not cover the consumable items & accessories supplied with viz. M8 Allen Bolt + Nut, tapered upper foot. Sunrack is not responsible for delay in delivering the warranty service/spares due to natural calamity or force majeure condition.`,
  `The foregoing warranties are in addition of all other warranties, whether express or implied and Sunrack does not make any warranty of Merchant ability or any warranty for fitness for a particular purpose. In no event, Sunrack be liable for or responsible to purchaser or any other party for any consequential, incidental or other damages, losses or expenses arising in connection with the use of or the inability to use the product.`,
  `All Claims related to this Warranty are subjected to Indian Law.`,
]

function formatAddress(address, state, pincode, country) {
  return [address, state, pincode, country].filter(Boolean).join(', ')
}

export default function CertificatePreview({ data }) {
  const billingFull = [
    data.billingCustomerName,
    formatAddress(data.billingAddress, data.billingState, data.billingPincode, data.billingCountry),
  ].filter(Boolean).join('\n')

  const shippingFull = [
    data.shippingCustomerName,
    formatAddress(data.shippingAddress, data.shippingState, data.shippingPincode, data.shippingCountry),
  ].filter(Boolean).join('\n')

  return (
    <div className="cert-preview">

      {/* ── Header ── */}
      <div className="cp-header">
        <div className="cp-header-left">
          S U N R A C K &nbsp; T E C H N O L O G I E S
        </div>
        <img src="/logo.svg" alt="Sunrack Logo" className="cp-header-logo-img" />
      </div>
      <div className="cp-divider" />

      {/* ── Title ── */}
      <div className="cp-title">WARRANTY CERTIFICATE</div>

      {/* ── Info table ── */}
      <table className="cp-info-table">
        <tbody>
          <tr>
            <td className="cp-info-label">Name of Customer (Billing):</td>
            <td className="cp-info-value cp-multiline">{billingFull || '—'}</td>
          </tr>
          <tr>
            <td className="cp-info-label">Name of Customer (Shipping):</td>
            <td className="cp-info-value cp-multiline">{shippingFull || '—'}</td>
          </tr>
          <tr>
            <td className="cp-info-label">Date of Dispatch:</td>
            <td className="cp-info-value">{data.dateOfDispatch || '—'}</td>
          </tr>
          <tr>
            <td className="cp-info-label">Invoice:</td>
            <td className="cp-info-value">{data.invoicePONumber || '—'}</td>
          </tr>
          <tr>
            <td className="cp-info-label">Warranty Period:</td>
            <td className="cp-info-value">{data.warrantyNumber ? `${data.warrantyNumber} ${data.warrantyUnit} from the date of dispatch and as per the terms below` : '—'}</td>
          </tr>
        </tbody>
      </table>

      {/* ── Material section ── */}
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
            <td className="cp-mat-td cp-mat-td--center">{data.materialPartName || '—'}</td>
            <td className="cp-mat-td cp-mat-td--center">{data.quantityKWp || '—'}</td>
            <td className="cp-mat-td cp-mat-td--center">{data.remarks || '—'}</td>
          </tr>
        </tbody>
      </table>

      {/* ── Terms ── */}
      <div className="cp-section-heading">Standard Terms &amp; Conditions:</div>
      <div className="cp-terms">
        {TERMS.map((para, i) => <p key={i}>{para}</p>)}
      </div>

      {/* ── Signature block ── */}
      <div className="cp-signature-block">
        <p className="cp-for-sunrack">For Sunrack Technologies</p>
        <img src="/signature.png" alt="Authorised Signatory" className="cp-signature-img" />
        <p className="cp-auth-text">Authorised Signatory</p>
      </div>

      {/* ── Footer bar ── */}
      <div className="cp-footer-bar">
        <span>SUNRACK TECHNOLOGIES LLP</span>
        <span>BOISAR, PALGHAR</span>
      </div>

    </div>
  )
}
