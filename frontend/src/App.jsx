import { useState } from 'react'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import FormatSelector from './components/FormatSelector'
import Format1Form from './components/Format1Form'
import Format2Form from './components/Format2Form'
import FormActions from './components/FormActions'
import PreviewSection from './components/PreviewSection'
import './App.css'

const INITIAL_FORM = {
  certificateFormat: 'format1',

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

  f2ProjectName: '',
  f2Client: '',
  f2SolarConsultant: 'Roofsol Energy Pvt Ltd',
  f2SolarDeveloper: 'Roofsol Energy Pvt Ltd',
  f2MainContractor: 'Roofsol Energy Pvt Ltd',
  f2Location: '',
  f2ProductDescription: '',
  f2ProductWarranty: '15 years',
  f2DesignWarranty: '25 years',
  f2WarrantyPeriodNote: 'STARTS FROM SHIPPING DATE',
  f2DateOfIssue: '',
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
    const payload = { ...form }
    delete payload.warrantyNumber
    delete payload.warrantyUnit
    if (form.certificateFormat !== 'format2') {
      payload.warrantyPeriod = form.warrantyNumber ? `${form.warrantyNumber} ${form.warrantyUnit}` : ''
    }
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
      <Navbar />

      <main className="page-main">
        <form className="cert-form" onSubmit={handlePreview} noValidate>

          <FormatSelector value={form.certificateFormat} onChange={handleChange} />

          {form.certificateFormat === 'format1' && (
            <Format1Form
              form={form}
              onChange={handleChange}
              sameAsBilling={sameAsBilling}
              onSameAsBilling={handleSameAsBilling}
            />
          )}

          {form.certificateFormat === 'format2' && (
            <Format2Form form={form} onChange={handleChange} />
          )}

          <FormActions onDownload={handleDownload} />

        </form>

        {showPreview && (
          <PreviewSection form={form} onClose={() => setShowPreview(false)} />
        )}
      </main>

      <Footer />
    </div>
  )
}
