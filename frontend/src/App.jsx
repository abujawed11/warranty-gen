import { useState } from 'react'
import FormInput from './components/FormInput'
import FormSelect from './components/FormSelect'
import FormSearchSelect from './components/FormSearchSelect'
import CertificatePreview from './components/CertificatePreview'
import './App.css'

const INITIAL_FORM = {
  billingCustomerName: '',
  billingAddress: '',
  billingState: '',
  billingPincode: '',
  billingCountry: '',

  shippingCustomerName: '',
  shippingAddress: '',
  shippingState: '',
  shippingPincode: '',
  shippingCountry: '',

  dateOfDispatch: '',
  invoicePONumber: '',
  warrantyNumber: '',
  warrantyUnit: 'Years',
  materialPartName: '',
  quantityKWp: '',
  remarks: '',
}

export default function App() {
  const [form, setForm] = useState(INITIAL_FORM)
  const [showPreview, setShowPreview] = useState(false)
  const [sameAsBilling, setSameAsBilling] = useState(false)

  function handleChange(e) {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: value }))
    if (showPreview) setShowPreview(false)
  }

  function handleSameAsBilling(e) {
    const checked = e.target.checked
    setSameAsBilling(checked)
    if (checked) {
      setForm(prev => ({
        ...prev,
        shippingCustomerName: prev.billingCustomerName,
        shippingAddress: prev.billingAddress,
        shippingState: prev.billingState,
        shippingPincode: prev.billingPincode,
        shippingCountry: prev.billingCountry,
      }))
    }
    if (showPreview) setShowPreview(false)
  }

  function handlePreview(e) {
    e.preventDefault()
    setShowPreview(true)
  }

  function handleDownload(e) {
    e.preventDefault()
    const f = document.createElement('form')
    f.method = 'POST'
    const base = import.meta.env.VITE_API_URL || ''
    f.action = `${base}/api/download-certificate`
    const payload = {
      ...form,
      warrantyPeriod: form.warrantyNumber ? `${form.warrantyNumber} ${form.warrantyUnit}` : '',
    }
    delete payload.warrantyNumber
    delete payload.warrantyUnit

    Object.entries(payload).forEach(([key, value]) => {
      const input = document.createElement('input')
      input.type  = 'hidden'
      input.name  = key
      input.value = value || ''
      f.appendChild(input)
    })
    document.body.appendChild(f)
    f.submit()
    document.body.removeChild(f)
  }

  return (
    <div className="page">
      <header className="page-header">
        <div className="page-header-inner">
          <div className="brand">
            <span className="brand-name">SUNRACK</span>
            <span className="brand-sub">Solar Mounting Solutions</span>
          </div>
          <h1 className="page-title">Warranty Certificate Generator</h1>
        </div>
      </header>

      <main className="page-main">
        <form className="cert-form" onSubmit={handlePreview} noValidate>

          {/* ── Section 1: Warranty Certificate Details ── */}
          <section className="form-section">
            <div className="section-header">
              <span className="section-badge">01</span>
              <h2 className="section-title">Warranty Certificate Details</h2>
            </div>

            <div className="customer-groups">

              {/* Billing Customer */}
              <div className="customer-group" id="billing-group">
                <div className="customer-group-title">
                  <span className="group-dot group-dot--yellow" />
                  Billing Customer
                </div>
                <div className="customer-group-fields">
                  <FormInput
                    label="Full Name"
                    name="billingCustomerName"
                    value={form.billingCustomerName}
                    onChange={handleChange}
                    placeholder="Enter billing customer name"
                  />
                  <FormInput
                    label="Address Line"
                    name="billingAddress"
                    value={form.billingAddress}
                    onChange={handleChange}
                    placeholder="Street / locality / area"
                  />
                  <div className="address-row">
                    <FormSelect
                      label="State"
                      name="billingState"
                      value={form.billingState}
                      onChange={handleChange}
                    />
                    <FormInput
                      label="Pincode"
                      name="billingPincode"
                      type="number"
                      value={form.billingPincode}
                      onChange={handleChange}
                      placeholder="400001"
                    />
                  </div>
                  <FormSearchSelect
                    label="Country"
                    name="billingCountry"
                    value={form.billingCountry}
                    onChange={handleChange}
                  />
                </div>
              </div>

              {/* Same as billing checkbox — sits between the two groups */}
              <label className="same-as-billing">
                <input
                  type="checkbox"
                  checked={sameAsBilling}
                  onChange={handleSameAsBilling}
                  className="same-as-billing-checkbox"
                />
                <span className="same-as-billing-icon">⇄</span>
                <span className="same-as-billing-text">Same as<br/>Billing</span>
              </label>

              {/* Shipping Customer */}
              <div className={`customer-group${sameAsBilling ? ' customer-group--locked' : ''}`}>
                <div className="customer-group-title">
                  <span className="group-dot group-dot--black" />
                  Shipping Customer
                </div>
                <div className="customer-group-fields">
                  <FormInput
                    label="Full Name"
                    name="shippingCustomerName"
                    value={form.shippingCustomerName}
                    onChange={handleChange}
                    placeholder="Enter shipping customer name"
                    disabled={sameAsBilling}
                  />
                  <FormInput
                    label="Address Line"
                    name="shippingAddress"
                    value={form.shippingAddress}
                    onChange={handleChange}
                    placeholder="Street / locality / area"
                    disabled={sameAsBilling}
                  />
                  <div className="address-row">
                    <FormSelect
                      label="State"
                      name="shippingState"
                      value={form.shippingState}
                      onChange={handleChange}
                      disabled={sameAsBilling}
                    />
                    <FormInput
                      label="Pincode"
                      name="shippingPincode"
                      type="number"
                      value={form.shippingPincode}
                      onChange={handleChange}
                      placeholder="400001"
                      disabled={sameAsBilling}
                    />
                  </div>
                  <FormSearchSelect
                    label="Country"
                    name="shippingCountry"
                    value={form.shippingCountry}
                    onChange={handleChange}
                    disabled={sameAsBilling}
                  />
                </div>
              </div>

            </div>

            {/* Remaining certificate fields */}
            <div className="form-grid form-grid--mt">
              <FormInput
                label="Date of Dispatch"
                name="dateOfDispatch"
                type="date"
                value={form.dateOfDispatch}
                onChange={handleChange}
              />
              <FormInput
                label="Invoice / PO Number"
                name="invoicePONumber"
                value={form.invoicePONumber}
                onChange={handleChange}
                placeholder="e.g. INV-2024-001"
              />
              <div className="form-field">
                <label className="form-label">Warranty Period</label>
                <div className="warranty-period-input">
                  <input
                    className="form-input warranty-period-number"
                    type="number"
                    name="warrantyNumber"
                    value={form.warrantyNumber}
                    onChange={handleChange}
                    placeholder="e.g. 10"
                    min="1"
                    autoComplete="off"
                  />
                  <select
                    className="form-input warranty-period-unit"
                    name="warrantyUnit"
                    value={form.warrantyUnit}
                    onChange={handleChange}
                  >
                    <option value="Months">Months</option>
                    <option value="Years">Years</option>
                  </select>
                </div>
              </div>
            </div>
          </section>

          {/* ── Section 2: Material Details ── */}
          <section className="form-section">
            <div className="section-header">
              <span className="section-badge">02</span>
              <h2 className="section-title">Details of Material Supplied</h2>
            </div>
            <div className="form-grid">
              <FormInput
                label="Material Part Name"
                name="materialPartName"
                value={form.materialPartName}
                onChange={handleChange}
                placeholder="e.g. Solar Panel Module"
              />
              <FormInput
                label="Quantity (kWp)"
                name="quantityKWp"
                type="number"
                value={form.quantityKWp}
                onChange={handleChange}
                placeholder="e.g. 100"
              />
              <div className="form-field form-field--full">
                <label className="form-label" htmlFor="remarks">Remarks</label>
                <textarea
                  id="remarks"
                  name="remarks"
                  value={form.remarks}
                  onChange={handleChange}
                  placeholder="Enter any additional remarks..."
                  className="form-input form-textarea"
                  rows={3}
                />
              </div>
            </div>
          </section>

          {/* ── Actions ── */}
          <div className="form-actions">
            <button type="submit" className="btn btn-primary">
              <span className="btn-icon">&#128065;</span>
              Preview Certificate
            </button>
            <button type="button" className="btn btn-secondary" onClick={handleDownload}>
              <span className="btn-icon">⬇</span>
              Download Certificate
            </button>
          </div>

        </form>

        {showPreview && (
          <div className="preview-section">
            <div className="preview-section-header">
              <h2>Certificate Preview</h2>
              <button className="btn-close" onClick={() => setShowPreview(false)} aria-label="Close preview">&#x2715;</button>
            </div>
            <CertificatePreview data={form} />
          </div>
        )}
      </main>

      <footer className="page-footer">
        <p>Sunrack Solar &mdash; Warranty Certificate System</p>
      </footer>
    </div>
  )
}
