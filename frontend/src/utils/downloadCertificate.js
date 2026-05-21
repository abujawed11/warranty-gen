export function downloadCertificate(form) {
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
