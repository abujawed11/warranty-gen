export default function Navbar({ certificateFormat }) {
  const title = certificateFormat === 'format3'
    ? 'Test Certificate Generator'
    : 'Warranty Certificate Generator'

  return (
    <header className="page-header">
      <div className="page-header-inner">
        <div className="brand">
          <img src="/black_back_photo.svg" alt="SUNRACK" className="brand-logo" />
          {/* <span className="brand-sub">Solar Mounting Solutions</span> */}
        </div>
        <h1 className="page-title">{title}</h1>
      </div>
    </header>
  )
}
