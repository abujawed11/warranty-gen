import FormInput from './FormInput'

export default function Format3Form({ form, onChange }) {
  return (
    <>
      {/* Section 01: Certificate Header */}
      <section className="form-section">
        <div className="section-header">
          <span className="section-badge">01</span>
          <h2 className="section-title">Certificate Header</h2>
        </div>
        <div className="form-grid">
          <FormInput
            label="Ref Number"
            name="tcRefNumber"
            value={form.tcRefNumber}
            onChange={onChange}
            placeholder="e.g. QA/SUN/729"
          />
          <FormInput
            label="Date"
            name="tcDate"
            type="date"
            value={form.tcDate}
            onChange={onChange}
          />
        </div>
      </section>

      {/* Section 02: Customer Details */}
      <section className="form-section">
        <div className="section-header">
          <span className="section-badge">02</span>
          <h2 className="section-title">Customer Details</h2>
        </div>
        <div className="form-grid">
          <FormInput
            label="Customer Name"
            name="tcCustomerName"
            value={form.tcCustomerName}
            onChange={onChange}
            placeholder="e.g. Freyr Energy Services Private Limited"
          />
          <FormInput
            label="Customer GSTIN"
            name="tcCustomerGstin"
            value={form.tcCustomerGstin}
            onChange={onChange}
            placeholder="e.g. 36AACCF3999A1ZM"
          />
          <FormInput
            label="Project Name"
            name="tcProjectName"
            value={form.tcProjectName}
            onChange={onChange}
            placeholder="e.g. Kayjay Forgings Private Limited"
          />
          <div className="form-field form-field--full">
            <label className="form-label" htmlFor="tcCustomerAddress">Customer Address</label>
            <textarea
              id="tcCustomerAddress"
              name="tcCustomerAddress"
              value={form.tcCustomerAddress}
              onChange={onChange}
              placeholder="Enter full customer address..."
              className="form-input form-textarea"
              rows={3}
            />
          </div>
        </div>
      </section>

      {/* Section 03: Supplier & PO Details */}
      <section className="form-section">
        <div className="section-header">
          <span className="section-badge">03</span>
          <h2 className="section-title">Supplier &amp; PO Details</h2>
        </div>
        <div className="form-grid">
          <FormInput
            label="Supplier Name"
            name="tcSupplierName"
            value={form.tcSupplierName}
            onChange={onChange}
          />
          <FormInput
            label="Supplier GSTIN"
            name="tcSupplierGstin"
            value={form.tcSupplierGstin}
            onChange={onChange}
          />
          <FormInput
            label="PO Number"
            name="tcPoNumber"
            value={form.tcPoNumber}
            onChange={onChange}
            placeholder="e.g. FESPL/22-23/7012"
          />
          <FormInput
            label="PO Date"
            name="tcPoDate"
            type="date"
            value={form.tcPoDate}
            onChange={onChange}
          />
          <FormInput
            label="Dispatch Date"
            name="tcDispatchDate"
            type="date"
            value={form.tcDispatchDate}
            onChange={onChange}
          />
          <div className="form-field form-field--full">
            <label className="form-label" htmlFor="tcSupplierAddress">Supplier Address</label>
            <textarea
              id="tcSupplierAddress"
              name="tcSupplierAddress"
              value={form.tcSupplierAddress}
              onChange={onChange}
              className="form-input form-textarea"
              rows={2}
            />
          </div>
        </div>
      </section>

      {/* Section 04: Material Details */}
      <section className="form-section">
        <div className="section-header">
          <span className="section-badge">04</span>
          <h2 className="section-title">Details of Material Supplied</h2>
        </div>
        <div className="form-grid">
          <FormInput
            label="Material Part Name"
            name="tcMaterialPartName"
            value={form.tcMaterialPartName}
            onChange={onChange}
            placeholder="e.g. Long Rail (MA-55)"
          />
          <FormInput
            label="Quantity (kWp)"
            name="tcQuantityKWp"
            value={form.tcQuantityKWp}
            onChange={onChange}
            placeholder="e.g. 509"
          />
          <div className="form-field form-field--full">
            <label className="form-label" htmlFor="tcRemarks">Remarks</label>
            <textarea
              id="tcRemarks"
              name="tcRemarks"
              value={form.tcRemarks}
              onChange={onChange}
              placeholder="Enter any remarks..."
              className="form-input form-textarea"
              rows={2}
            />
          </div>
        </div>
      </section>

      {/* Section 05: Chemical Composition */}
      <section className="form-section">
        <div className="section-header">
          <span className="section-badge">05</span>
          <h2 className="section-title">Chemical Composition — Actual Values (In %)</h2>
        </div>
        <div className="form-grid">
          <FormInput label="Si"    name="tcSi"    value={form.tcSi}    onChange={onChange} placeholder="e.g. 0.408" />
          <FormInput label="Mg"    name="tcMg"    value={form.tcMg}    onChange={onChange} placeholder="e.g. 0.52"  />
          <FormInput label="Fe"    name="tcFe"    value={form.tcFe}    onChange={onChange} placeholder="e.g. 0.274" />
          <FormInput label="Other" name="tcOther" value={form.tcOther} onChange={onChange} placeholder="e.g. 0.25"  />
          <FormInput label="Al"    name="tcAl"    value={form.tcAl}    onChange={onChange} placeholder="e.g. REM."  />
        </div>
      </section>

      {/* Section 06: Mechanical Properties */}
      <section className="form-section">
        <div className="section-header">
          <span className="section-badge">06</span>
          <h2 className="section-title">Mechanical Properties — Hardness Actual Values</h2>
        </div>
        <div className="form-grid">
          <FormInput label="B.H.N"  name="tcBHN"  value={form.tcBHN}  onChange={onChange} placeholder="e.g. NA" />
          <FormInput label="H.V 10" name="tcHV10" value={form.tcHV10} onChange={onChange} placeholder="e.g. 73" />
        </div>
      </section>
    </>
  )
}
