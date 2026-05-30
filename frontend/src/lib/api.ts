const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function fetchJson<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });
  if (!response.ok) {
    const error = await response.text();
    throw new ApiError(`API error ${response.status}: ${error}`, response.status);
  }
  return response.json();
}

export async function getHealth() {
  return fetchJson<{ status: string }>("/health/");
}

// ── Risk Assessment ─────────────────────────────────────────────────────────

export async function listRiskAssessments(page = 1, pageSize = 20) {
  return fetchJson<{ items: any[]; total: number }>(`/api/v1/risk-assessments?page=${page}&page_size=${pageSize}`);
}

export async function runRiskAssessment(data: { employee_name: string; employee_email: string; department: string; role: string; last_day?: string }) {
  return fetchJson<any>("/api/v1/risk-assessments/run", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getRiskAssessment(id: string) {
  return fetchJson<any>(`/api/v1/risk-assessments/${id}`);
}

export async function getRiskOverview() {
  return fetchJson<any>("/api/v1/risk-assessment/overview");
}

// ── Integration Hub ─────────────────────────────────────────────────────────

export async function listIntegrations(page = 1, pageSize = 20) {
  return fetchJson<{ items: any[]; total: number }>(`/api/v1/integrations?page=${page}&page_size=${pageSize}`);
}

export async function seedIntegrations() {
  return fetchJson<any>("/api/v1/integrations/seed", { method: "POST" });
}

export async function syncIntegration(id: string) {
  return fetchJson<any>(`/api/v1/integrations/${id}/sync`, { method: "POST" });
}

export async function getIntegrationOverview() {
  return fetchJson<any>("/api/v1/integration/overview");
}

// ── Team Transition ─────────────────────────────────────────────────────────

export async function listTeamTransitions(page = 1, pageSize = 20) {
  return fetchJson<{ items: any[]; total: number }>(`/api/v1/team-transitions?page=${page}&page_size=${pageSize}`);
}

export async function createTeamTransition(data: any) {
  return fetchJson<any>("/api/v1/team-transitions", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

// ── Compliance ──────────────────────────────────────────────────────────────

export async function listComplianceReports(page = 1, pageSize = 20) {
  return fetchJson<{ items: any[]; total: number }>(`/api/v1/compliance-reports?page=${page}&page_size=${pageSize}`);
}

export async function generateComplianceReport(data: any) {
  return fetchJson<any>("/api/v1/compliance-reports/generate", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

// ── Sentiment & Early Warning ───────────────────────────────────────────────

export async function listSentimentPulses(page = 1, pageSize = 20) {
  return fetchJson<{ items: any[]; total: number }>(`/api/v1/sentiment-pulses?page=${page}&page_size=${pageSize}`);
}

export async function createSentimentPulse(data: any) {
  return fetchJson<any>("/api/v1/sentiment-pulses", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function listFlightRiskAlerts(page = 1, pageSize = 20) {
  return fetchJson<{ items: any[]; total: number }>(`/api/v1/flight-risk-alerts?page=${page}&page_size=${pageSize}`);
}

export async function detectFlightRisk(name: string, email: string, dept: string) {
  return fetchJson<any>(`/api/v1/flight-risk-alerts/detect?employee_name=${encodeURIComponent(name)}&employee_email=${encodeURIComponent(email)}&department=${encodeURIComponent(dept)}`, {
    method: "POST",
  });
}

export async function getSentimentOverview() {
  return fetchJson<any>("/api/v1/sentiment/overview");
}

// ── Checklists (v1) ─────────────────────────────────────────────────────────

export async function listChecklists(page = 1, pageSize = 20) {
  return fetchJson<{ items: any[]; total: number }>(`/api/v1/checklists?page=${page}&page_size=${pageSize}`);
}

export async function getChecklist(id: string) {
  return fetchJson<any>(`/api/v1/checklists/${id}`);
}

export async function getDashboard() {
  return fetchJson<any>("/api/v1/dashboard");
}

export { ApiError };
