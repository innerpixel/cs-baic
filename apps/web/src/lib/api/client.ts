import { browser } from '$app/environment';

const API_BASE = browser
	? (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000')
	: 'http://localhost:8000';

export interface ApiDocumentItem {
	id: string;
	filename: string;
	type: string;
	status: string;
	created_at: string;
}

export interface ApiAuditEvent {
	id: string;
	document_id: string | null;
	event_type: string;
	event_data: Record<string, unknown>;
	created_at: string;
}

export interface ApiAnalysis {
	id: string;
	fields: Record<string, unknown> | null;
	missing_fields: string[] | null;
	risk_flags: string[] | null;
	summary: string | null;
	suggested_action: string | null;
	detected_type: string | null;
	confidence: number | null;
	language: string | null;
	urgency: string | null;
	analyzer_outputs: Record<string, unknown> | null;
	created_at: string;
}

export interface ApiDocumentDetail extends ApiDocumentItem {
	analysis: ApiAnalysis | null;
	audit_events: ApiAuditEvent[];
}

export interface UploadResult {
	id: string;
	status: string;
}

export interface ApproveResult {
	document_id: string;
	approved_at: string;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
	const res = await fetch(`${API_BASE}${path}`, init);
	if (!res.ok) {
		const body = await res.text().catch(() => '');
		throw new Error(`API ${res.status}: ${body}`);
	}
	return res.json() as Promise<T>;
}

export const api = {
	listDocuments(): Promise<ApiDocumentItem[]> {
		return request('/api/documents');
	},

	getDocument(id: string): Promise<ApiDocumentDetail> {
		return request(`/api/documents/${id}`);
	},

	async uploadDocument(text: string, filename: string, type: string): Promise<UploadResult> {
		const form = new FormData();
		form.append('text', text);
		form.append('filename', filename);
		form.append('type', type);
		return request('/api/documents', { method: 'POST', body: form });
	},

	approveDocument(id: string): Promise<ApproveResult> {
		return request(`/api/documents/${id}/approve`, { method: 'POST' });
	},

	listAuditEvents(limit = 50): Promise<ApiAuditEvent[]> {
		return request(`/api/audit?limit=${limit}`);
	}
};
