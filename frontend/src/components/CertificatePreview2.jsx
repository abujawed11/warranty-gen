export default function CertificatePreview2({ data }) {
  const rows = [
    ['PROJECT NAME',        data.f2ProjectName],
    ['CLIENT',              data.f2Client],
    ['SOLAR CONSULTANT',    data.f2SolarConsultant],
    ['SOLAR DEVELOPER',     data.f2SolarDeveloper],
    ['MAIN CONTRACTOR',     data.f2MainContractor],
    ['LOCATION',            data.f2Location],
    ['PRODUCT DESCRIPTION', data.f2ProductDescription],
    ['PRODUCT WARRANTY',    data.f2ProductWarranty],
    ['DESIGN WARRANTY',     data.f2DesignWarranty],
    ['WARRANTY PERIOD',     data.f2WarrantyPeriodNote],
  ]

  return (
    <div className="cert-preview cp2">

      {/* ── Header ── */}
      <div className="cp2-header">
        <div className="cp2-header-inner">
          <span className="cp2-company-name">S U N R A C K &nbsp; T E C H N O L O G I E S</span>
          <img src="/logo.svg" alt="Sunrack Logo" className="cp-header-logo-img" />
        </div>
        <div className="cp-divider" />
      </div>

      {/* ── Title ── */}
      <div className="cp-title">WARRANTY CERTIFICATE</div>

      {/* ── Info table ── */}
      <table className="cp2-info-table">
        <tbody>
          {rows.map(([label, value]) => (
            <tr key={label}>
              <td className="cp2-info-label">{label}</td>
              <td className="cp2-info-value">{value || ''}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* ── Body ── */}
      <div className="cp2-body">

        <p className="cp2-subheading">M/s Sunrack Technologies</p>
        <p>This Warranty Certificate ("Warranty") is issued by <strong>M/s Sunrack Technologies</strong>, hereinafter referred to as <strong>"Sunrack"</strong>, for its solar structure products ("Product") supplied to the customer.</p>

        {/* Section 1 */}
        <p className="cp2-section-heading">1. Warranty Coverage</p>
        <p>Sunrack provides this warranty solely against <strong>manufacturing defects and workmanship</strong> in the products supplied.</p>
        <p>In the event of a valid claim, Sunrack shall, at its sole discretion:</p>
        <ul className="cp2-list">
          <li>Repair the defective component; or</li>
          <li>Replace the defective product or part with a new or remanufactured equivalent.</li>
        </ul>
        <p>Such action will be taken <strong>within 15 (fifteen) working days</strong> from the date of written intimation and acknowledgment by Sunrack.</p>
        <p>Sunrack's <strong>total liability</strong> for such repair or replacement shall <strong>not exceed the original purchase price</strong> of the product in question.</p>
        <p>Warranty is directly transferred from the raw material supplier Arcelor Mittal/Nalco and will be adhered to the documentation provided for C5 level corrosion.</p>

        {/* Section 2 */}
        <p className="cp2-section-heading">2. Exclusions from Warranty</p>
        <p>This warranty shall be deemed <strong>void</strong> and <strong>not applicable</strong> in the following cases:</p>
        <ul className="cp2-list">
          <li>Structural failures arising from conditions beyond product specifications, improper installation, unsuitable site conditions, or environmental stressors not accounted for in the original design.</li>
          <li>Damage caused by <strong>Acts of God</strong> such as earthquakes, floods, storms, lightning, or other natural disasters.</li>
          <li>Cosmetic wear and tear including rust, discoloration, surface blemishes, or fading that does not impact structural integrity.</li>
          <li>Physical damage resulting from <strong>accidents, negligence, third-party handling</strong>, or improper maintenance.</li>
          <li>Any damage arising during <strong>unloading, stacking, or site transportation</strong>, unless handled by Sunrack or its authorized representatives.</li>
          <li><strong>Unauthorized modifications, reworking, or repairs</strong> carried out without prior written approval from Sunrack.</li>
          <li>Non-compliance with recommended installation manuals or engineering drawings.</li>
          <li>Warranty shall be rendered <strong>null and void</strong> in case of <strong>non-payment or partial payment</strong> of agreed dues.</li>
          <li>Service delays due to <strong>force majeure conditions</strong>, including strikes, supply chain disruptions, or government regulations.</li>
        </ul>

        {/* Section 3 */}
        <p className="cp2-section-heading">3. Exclusions of Consumables and Accessories</p>
        <p>This warranty <strong>does not cover</strong> the following items, which are considered consumables or ancillary parts:</p>
        <ul className="cp2-list">
          <li><strong>Bolts, nuts, fasteners, clamps, washers, rivets</strong>, and similar hardware items.</li>
          <li><strong>Cable trays, conduit supports, wire management clips</strong>, and accessories unless specified otherwise in writing.</li>
          <li><strong>Packaging material</strong>, wooden pallets, wrapping film, or protective foam used during transport.</li>
          <li>Items provided by third-party vendors or procured locally by the client, even if recommended by Sunrack.</li>
          <li><strong>Accessories not manufactured by Sunrack</strong>, even if supplied as part of the package.</li>
        </ul>
        <p>All these items are excluded from warranty and shall be replaced or maintained at the customer's cost.</p>

        {/* Section 4 */}
        <p className="cp2-section-heading">4. Limitation of Liability</p>
        <ul className="cp2-list">
          <li>Sunrack's responsibility is strictly limited to the <strong>repair or replacement of defective parts</strong> as defined under this warranty.</li>
          <li><strong>No claims will be entertained</strong> for project delays, indirect losses, or business interruptions resulting from the failure or delay of any Sunrack product.</li>
          <li>Sunrack shall not be liable for <strong>loss of revenue, loss of contracts, loss of data, or third-party liabilities</strong> incurred by the purchaser.</li>
          <li>The purchaser shall indemnify and hold Sunrack harmless from any claims arising due to improper installation or misuse.</li>
          <li>Sunrack shall not be held responsible for <strong>electrical, civil, or mechanical failures</strong> in systems integrated with Sunrack structures, which are outside the design scope.</li>
          <li>This warranty does <strong>not cover logistics, handling, removal, or reinstallation costs</strong> at the site unless specifically agreed in writing.</li>
          <li>Sunrack makes <strong>no express or implied warranties</strong> beyond those stated herein, including but not limited to warranties of merchantability or fitness for a particular purpose.</li>
          <li>In no event shall Sunrack's total liability exceed the original invoice value of the product supplied under this warranty.</li>
        </ul>

        {/* Section 5 */}
        <p className="cp2-section-heading">5. Governing Law</p>
        <p>All claims, disputes, or legal proceedings arising from or relating to this Warranty shall be governed by and construed in accordance with the <strong>laws of the Republic of India</strong>. The competent courts of <strong>Mumbai, India</strong> shall have exclusive jurisdiction.</p>

      </div>

      {/* ── Signature block ── */}
      <div className="cp-signature-block">
        <p style={{ fontWeight: 700, marginBottom: 2 }}>Issued By:</p>
        <p style={{ fontWeight: 700, marginBottom: 2 }}>M/s Sunrack Technologies</p>
        <p style={{ marginBottom: 8 }}>Authorized Signatory</p>
        <img src="/signature.png" alt="Signature" className="cp-signature-img" />
        {data.f2DateOfIssue && (
          <p className="cp-auth-text">Date of Issue: {data.f2DateOfIssue}</p>
        )}
      </div>

      {/* ── Footer ── */}
      <div className="cp-footer-bar">
        <span>SUNRACK TECHNOLOGIES LLP, BOISAR, PALGHAR</span>
      </div>

    </div>
  )
}
