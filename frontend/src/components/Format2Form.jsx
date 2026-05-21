import FormInput from './FormInput'

export default function Format2Form({ form, onChange }) {
  return (
    <section className="form-section">
      <div className="section-header">
        <span className="section-badge">01</span>
        <h2 className="section-title">Project Details</h2>
      </div>
      <div className="form-grid">
        <FormInput label="Project Name" name="f2ProjectName" value={form.f2ProjectName} onChange={onChange} placeholder="e.g. Solar Plant Phase 1" />
        <FormInput label="Client" name="f2Client" value={form.f2Client} onChange={onChange} placeholder="e.g. ABC Solar Pvt Ltd" />
        <FormInput label="Solar Consultant" name="f2SolarConsultant" value={form.f2SolarConsultant} onChange={onChange} placeholder="" />
        <FormInput label="Solar Developer" name="f2SolarDeveloper" value={form.f2SolarDeveloper} onChange={onChange} placeholder="" />
        <FormInput label="Main Contractor" name="f2MainContractor" value={form.f2MainContractor} onChange={onChange} placeholder="" />
        <FormInput label="Location" name="f2Location" value={form.f2Location} onChange={onChange} placeholder="e.g. Rajasthan, India" />
      </div>

      <div className="section-header" style={{ marginTop: '24px' }}>
        <span className="section-badge">02</span>
        <h2 className="section-title">Product &amp; Warranty Details</h2>
      </div>
      <div className="form-grid">
        <FormInput label="Product Description" name="f2ProductDescription" value={form.f2ProductDescription} onChange={onChange} placeholder="e.g. UX Long Rail with 25mm Strut Rail" />
        <FormInput label="Product Warranty" name="f2ProductWarranty" value={form.f2ProductWarranty} onChange={onChange} placeholder="e.g. 15 years" />
        <FormInput label="Design Warranty" name="f2DesignWarranty" value={form.f2DesignWarranty} onChange={onChange} placeholder="e.g. 25 years" />
        <FormInput label="Warranty Period Note" name="f2WarrantyPeriodNote" value={form.f2WarrantyPeriodNote} onChange={onChange} placeholder="e.g. STARTS FROM SHIPPING DATE." />
        <FormInput label="Date of Issue" name="f2DateOfIssue" type="date" value={form.f2DateOfIssue} onChange={onChange} />
      </div>
    </section>
  )
}
