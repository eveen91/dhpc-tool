import { Route, Routes } from "react-router-dom";

import { AppLayout } from "./layouts/AppLayout";
import { DashboardPage } from "./pages/DashboardPage";
import { LoginPage } from "./pages/LoginPage";
import { PlaceholderPage } from "./pages/PlaceholderPage";

export function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<AppLayout />}>
        <Route index element={<DashboardPage />} />
        <Route path="hosts" element={<PlaceholderPage title="Hosty" description="Statyczne rezerwacje DHCP." />} />
        <Route path="subnets" element={<PlaceholderPage title="Podsieci" description="Definicje podsieci bez zakresów dynamicznych." />} />
        <Route path="changes" element={<PlaceholderPage title="Zmiany" description="Walidacja, diff i akceptacja zmian." />} />
        <Route path="deployments" element={<PlaceholderPage title="Wdrożenia" description="Postęp wdrożeń będzie komunikowany przez API." />} />
        <Route path="logs" element={<PlaceholderPage title="Logi" description="Wyszukiwanie znormalizowanych zdarzeń DHCP." />} />
        <Route path="audit" element={<PlaceholderPage title="Historia / audyt" description="Niezmienny ślad operacyjny." />} />
        <Route path="admin" element={<PlaceholderPage title="Administracja" description="Konfiguracja memberów i integracji tożsamości." />} />
      </Route>
    </Routes>
  );
}
