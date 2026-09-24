export function DashboardPage() {
  return (
    <section>
      <h1>Dashboard</h1>
      <p>Stan klastra, DHCP i konfiguracji będzie pobierany wyłącznie przez backend API.</p>
      <div className="status-grid">
        <article><h2>Member A</h2><p>Nie skonfigurowano</p></article>
        <article><h2>Member B</h2><p>Nie skonfigurowano</p></article>
        <article><h2>Wdrożenia</h2><p>Wykonanie wyłączone</p></article>
      </div>
    </section>
  );
}
