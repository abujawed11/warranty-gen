import FormInput from './FormInput'
import FormSelect from './FormSelect'
import FormSearchSelect from './FormSearchSelect'

export default function Format1Form({ form, onChange, sameAsBilling, onSameAsBilling }) {
  return (
    <>
      {/* Section 1: Warranty Certificate Details */}
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
              <FormInput label="Full Name" name="billingCustomerName" value={form.billingCustomerName} onChange={onChange} placeholder="Enter billing customer name" />
              <FormInput label="Address Line" name="billingAddress" value={form.billingAddress} onChange={onChange} placeholder="Street / locality / area" />
              <div className="address-row">
                <FormSelect label="State" name="billingState" value={form.billingState} onChange={onChange} />
                <FormInput label="Pincode" name="billingPincode" type="number" value={form.billingPincode} onChange={onChange} placeholder="400001" />
              </div>
              <FormSearchSelect label="Country" name="billingCountry" value={form.billingCountry} onChange={onChange} />
            </div>
          </div>

          {/* Same as billing checkbox */}
          <label className="same-as-billing">
            <input type="checkbox" checked={sameAsBilling} onChange={onSameAsBilling} className="same-as-billing-checkbox" />
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
              <FormInput label="Full Name" name="shippingCustomerName" value={form.shippingCustomerName} onChange={onChange} placeholder="Enter shipping customer name" disabled={sameAsBilling} />
              <FormInput label="Address Line" name="shippingAddress" value={form.shippingAddress} onChange={onChange} placeholder="Street / locality / area" disabled={sameAsBilling} />
              <div className="address-row">
                <FormSelect label="State" name="shippingState" value={form.shippingState} onChange={onChange} disabled={sameAsBilling} />
                <FormInput label="Pincode" name="shippingPincode" type="number" value={form.shippingPincode} onChange={onChange} placeholder="400001" disabled={sameAsBilling} />
              </div>
              <FormSearchSelect label="Country" name="shippingCountry" value={form.shippingCountry} onChange={onChange} disabled={sameAsBilling} />
            </div>
          </div>

        </div>

        {/* Remaining certificate fields */}
        <div className="form-grid form-grid--mt">
          <FormInput label="Date of Dispatch" name="dateOfDispatch" type="date" value={form.dateOfDispatch} onChange={onChange} />
          <FormInput label="Invoice / PO Number" name="invoicePONumber" value={form.invoicePONumber} onChange={onChange} placeholder="e.g. INV-2024-001" />
          <div className="form-field">
            <label className="form-label">Warranty Period</label>
            <div className="warranty-period-input">
              <input
                className="form-input warranty-period-number"
                type="number"
                name="warrantyNumber"
                value={form.warrantyNumber}
                onChange={onChange}
                placeholder="e.g. 10"
                min="1"
                autoComplete="off"
              />
              <select className="form-input warranty-period-unit" name="warrantyUnit" value={form.warrantyUnit} onChange={onChange}>
                <option value="Months">Months</option>
                <option value="Years">Years</option>
              </select>
            </div>
          </div>
        </div>
      </section>

      {/* Section 2: Material Details */}
      <section className="form-section">
        <div className="section-header">
          <span className="section-badge">02</span>
          <h2 className="section-title">Details of Material Supplied</h2>
        </div>
        <div className="form-grid">
          <FormInput label="Material Part Name" name="materialPartName" value={form.materialPartName} onChange={onChange} placeholder="e.g. Solar Panel Module" />
          <FormInput label="Quantity (kWp)" name="quantityKWp" type="number" value={form.quantityKWp} onChange={onChange} placeholder="e.g. 100" />
          <div className="form-field form-field--full">
            <label className="form-label" htmlFor="remarks">Remarks</label>
            <textarea
              id="remarks"
              name="remarks"
              value={form.remarks}
              onChange={onChange}
              placeholder="Enter any additional remarks..."
              className="form-input form-textarea"
              rows={3}
            />
          </div>
        </div>
      </section>
    </>
  )
}
