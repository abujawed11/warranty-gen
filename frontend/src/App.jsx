import Navbar from './components/Navbar'
import Footer from './components/Footer'
import FormatSelector from './components/FormatSelector'
import Format1Form from './components/Format1Form'
import Format2Form from './components/Format2Form'
import Format3Form from './components/Format3Form'
import FormActions from './components/FormActions'
import PreviewSection from './components/PreviewSection'
import { useWarrantyForm } from './hooks/useWarrantyForm'
import './App.css'

export default function App() {
  const {
    form,
    showPreview,
    sameAsBilling,
    handleChange,
    handleSameAsBilling,
    handlePreview,
    handleDownload,
    setShowPreview,
  } = useWarrantyForm()

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

          {form.certificateFormat === 'format3' && (
            <Format3Form form={form} onChange={handleChange} />
          )}

          {form.certificateFormat && <FormActions onDownload={handleDownload} />}

        </form>

        {showPreview && (
          <PreviewSection form={form} onClose={() => setShowPreview(false)} />
        )}
      </main>

      <Footer />
    </div>
  )
}
