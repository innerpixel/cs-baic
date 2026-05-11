import { browser } from '$app/environment';

const API_BASE = browser
	? (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000')
	: 'http://localhost:8000';

export interface SourceDoc {
	doc_id?: string;
	filename?: string;
}

export interface AskAnswer {
	answer: string;
	source_documents: (string | SourceDoc)[];
	confidence: 'low' | 'medium' | 'high';
	missing_information: string[];
	recommended_next_action: string | null;
	requires_human_review: boolean;
}

export function sourceLabel(src: string | SourceDoc): string {
	if (typeof src === 'string') return src;
	return src.filename ?? src.doc_id ?? 'document';
}

export function sourceHref(src: string | SourceDoc): string {
	if (typeof src === 'string') return '/app/inbox';
	if (src.doc_id) return `/app/inbox?focus=${src.doc_id}`;
	return '/app/inbox';
}

export async function askQuestion(query: string): Promise<AskAnswer> {
	const res = await fetch(`${API_BASE}/api/ask`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ query })
	});
	if (!res.ok) {
		const body = await res.text().catch(() => '');
		throw new Error(`API ${res.status}: ${body}`);
	}
	return res.json() as Promise<AskAnswer>;
}
