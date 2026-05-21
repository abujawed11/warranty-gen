import { useState } from 'react'
import { INITIAL_FORM } from '../utils/initialForm'
import { downloadCertificate } from '../utils/downloadCertificate'

export function useWarrantyForm() {
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
    downloadCertificate(form)
  }

  return {
    form,
    showPreview,
    sameAsBilling,
    handleChange,
    handleSameAsBilling,
    handlePreview,
    handleDownload,
    setShowPreview,
  }
}
