# DHCP Manager — szkielet projektu

Monorepo dla Web UI zarządzającego wyłącznie statyczną konfiguracją DHCP na Check Point R81.10 ClusterXL. Ten etap **nie łączy się z firewallami**, nie wykonuje wdrożeń i nie zawiera poleceń Gaia.

## Architektura

- **`frontend/`** — React + TypeScript + Vite; routowanie widoków Web UI.
- **`backend/`** — FastAPI, Pydantic, SQLAlchemy i Alembic; API, model domenowy, RBAC i generator konfiguracji.
- **`worker/`** — Celery/Redis i bezpieczny punkt rozszerzenia procesu wdrożenia.
- **`nginx/`** — lokalny reverse proxy dla UI i `/api`.
- **PostgreSQL** — konfiguracje, zmiany, wdrożenia i audyt.

Granice są celowe: warstwa API nie zna SSH, domena nie zna FastAPI ani SQLAlchemy, a adapter firewalla nie oferuje wykonania dowolnej komendy. Interfejs `FirewallAdapter` obsługuje wyłącznie: status, walidację konfiguracji, instalację i rollback. Implementacja `SshFirewallAdapter` to nieaktywny stub, a `FakeFirewallAdapter` służy do testów.

## Wymagania

- Docker Engine z Docker Compose v2, **lub** Python 3.12+ i Node.js 22+ do uruchamiania komponentów bez kontenerów.

## Start lokalny przez Docker Compose

```bash
cp .env.example .env
# Ustaw wyłącznie lokalne, nieprodukcyjne hasło dla PostgreSQL.
docker compose up --build
```

- UI przez Nginx: <http://localhost:8080>
- API health check: <http://localhost:8080/api/health>
- dokumentacja OpenAPI (bez auth): <http://localhost:8080/docs>

Aby zatrzymać środowisko:

```bash
docker compose down
```

## Testy i kontrole lokalne

Backend:

```bash
cd backend
python3 -m pip install -e '.[dev]'
python3 -m pytest -q
python3 -m ruff check .
python3 -m mypy app
```

Frontend:

```bash
cd frontend
npm install
npm run lint
npm run build
npm test
```

E2E (docelowo):

```bash
cd e2e
npm install
npx playwright test
```

## Bezpieczeństwo i świadomie odroczone elementy

- Brak sekretów, haseł, kluczy prywatnych i host fingerprintów w repozytorium.
- Uwierzytelnianie jest **provider-neutral stubem**. Kontrakt `AuthenticatedUser` oraz role `viewer`, `operator`, `approver`, `administrator` są gotowe do podłączenia OIDC albo LDAP/AD.
- Generator tworzy kompletny, deterministyczny `dhcpd.conf`, nie przyjmuje surowych fragmentów konfiguracji i odrzuca `range`.
- Nie ma `chattr`, kopiowania `/etc/dhcpd.conf`, restartu DHCP, prawdziwego SSH/SFTP ani wdrożeń ClusterXL.
- Przed kolejnym etapem potrzebne jest potwierdzenie w laboratorium: obsługiwanych poleceń Gaia/wrappera, modelu role ACTIVE/STANDBY, zachowania DHCP podczas failoveru oraz trwałości pliku po aktualizacjach.

Pełne wymagania i ryzyka znajdują się w niezmienionym [`PLAN_IMPLEMENTACJI.md`](PLAN_IMPLEMENTACJI.md).
