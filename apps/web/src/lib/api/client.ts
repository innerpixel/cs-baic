import { browser } from '$app/environment';

const API_BASE = browser
	? (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000')
	: 'http://localhost:8000';

export interface ApiDocumentItem {
	id: string;
	filename: string;
	type: string;
	status: string;
	source: string | null;
	review_state: string | null;
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
	review_note: string | null;
	batch_id: string | null;
	pdf_path: string | null;
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

export interface ReviewStateResult {
	document_id: string;
	review_state: string;
	review_note: string | null;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
	const res = await fetch(`${API_BASE}${path}`, init);
	if (!res.ok) {
		const body = await res.text().catch(() => '');
		throw new Error(`API ${res.status}: ${body}`);
	}
	return res.json() as Promise<T>;
}

export function pdfUrl(docId: string): string {
	return `${API_BASE}/api/documents/${docId}/pdf`;
}

export const api = {
	listDocuments(): Promise<ApiDocumentItem[]> {
		return request('/api/documents');
	},

	getDocument(id: string): Promise<ApiDocumentDetail> {
		return request(`/api/documents/${id}`);
	},

	async uploadFile(file: File): Promise<{ id: string; status: string; batch?: boolean; count?: number }> {
		const form = new FormData();
		form.append('file', file);
		const res = await fetch(`${API_BASE}/api/uploads`, { method: 'POST', body: form });
		if (!res.ok) {
			const body = await res.text().catch(() => '');
			throw new Error(`API ${res.status}: ${body}`);
		}
		const data = await res.json();
		if ('batch_id' in data) {
			// ZIP batch: return the first doc id for polling, mark as batch
			const first = data.documents?.[0];
			return { id: first?.document_id ?? data.batch_id, status: 'queued', batch: true, count: data.documents?.length };
		}
		return { id: data.document_id, status: data.status };
	},

	approveDocument(id: string): Promise<ApproveResult> {
		return request(`/api/documents/${id}/approve`, { method: 'POST' });
	},

	reviewState(id: string, state: string, note?: string): Promise<ReviewStateResult> {
		return request(`/api/documents/${id}/review_state`, {
			method: 'PATCH',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ state, note: note ?? null }),
		});
	},

	listAuditEvents(limit = 50): Promise<ApiAuditEvent[]> {
		return request(`/api/audit?limit=${limit}`);
	}
};
