import { NavLink, Outlet } from "react-router-dom";

const navigation = [
  ["/", "Dashboard"],
  ["/hosts", "Hosty"],
  ["/subnets", "Podsieci"],
  ["/changes", "Zmiany"],
  ["/deployments", "Wdrożenia"],
  ["/logs", "Logi"],
  ["/audit", "Historia / audyt"],
  ["/admin", "Administracja"],
] as const;

export function AppLayout() {
  return (
    <div className="app-shell">
      <aside>
        <p className="brand">DHCP Manager</p>
        <p className="environment">Szkielet · bez połączeń z firewallami</p>
        <nav aria-label="Główna nawigacja">
          {navigation.map(([to, label]) => (
            <NavLink end={to === "/"} key={to} to={to}>
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main>
        <Outlet />
      </main>
    </div>
  );
}
