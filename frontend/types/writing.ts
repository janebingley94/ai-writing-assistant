export type BlogTone = "professional" | "casual" | "academic" | "creative";
export type BlogLength = "short" | "medium" | "long";
export type EmailType =
  | "business"
  | "follow_up"
  | "introduction"
  | "complaint"
  | "thank_you";
export type EmailTone = "formal" | "friendly" | "urgent";
export type SummaryType = "bullet_points" | "paragraph" | "tldr" | "executive";

export interface BlogGenerateRequest {
  topic: string;
  keywords: string[];
  tone: BlogTone;
  length: BlogLength;
  language: string;
  outline_first: boolean;
}

export interface EmailGenerateRequest {
  email_type: EmailType;
  recipient_name?: string | null;
  sender_name?: string | null;
  context: string;
  tone: EmailTone;
  language: string;
}

export interface SummaryRequest {
  content: string;
  summary_type: SummaryType;
  max_length: number;
  language: string;
}

export interface SEOArticleRequest {
  keyword: string;
  secondary_keywords: string[];
  word_count: number;
  target_audience: string;
  include_faq: boolean;
  language: string;
}

export interface GenerationResponse {
  id: string;
  content: string;
  word_count: number;
  generation_type: string;
  metadata: Record<string, unknown>;
  created_at: string;
}
