// 用户相关类型
export interface UserInfo {
  user_id: number
  username: string
  phone?: string
  email?: string
  avatar_url?: string
  nickname?: string
  gender?: number
  birthday?: string
  status: number
  last_login_at?: string
  created_at?: string
}

export interface LoginForm {
  username: string
  password: string
  login_type?: string
}

export interface RegisterForm {
  username: string
  password: string
  phone?: string
  email?: string
}

export interface TokenInfo {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

// 问诊相关类型
export interface Consultation {
  consultation_id: number
  user_id: number
  title?: string
  symptoms?: string
  ai_suggestion?: string
  doctor_review?: string
  severity_level?: number
  status: number
  created_at: string
  updated_at?: string
}

export interface ConsultationCreate {
  title?: string
  symptoms: string
}

// 健康相关类型
export interface VitalSign {
  sign_id: number
  user_id: number
  sign_type: string
  value: number
  value_ext?: number
  unit: string
  measured_at: string
  source?: string
  notes?: string
}

export interface VitalSignCreate {
  sign_type: string
  value: number
  value_ext?: number
  unit: string
  measured_at: string
}

export interface HealthRecord {
  record_id: number
  user_id: number
  blood_type?: string
  height?: number
  weight?: number
  bmi?: number
  medical_history?: string
  family_history?: string
  allergy_history?: string
}

// 文章相关类型
export interface Article {
  article_id: number
  title: string
  summary?: string
  content: string
  cover_image?: string
  tags?: string
  view_count: number
  like_count: number
  comment_count: number
  status: number
  published_at?: string
  created_at: string
}

export interface Category {
  category_id: number
  category_name: string
  parent_id?: number
  description?: string
  sort_order: number
}

// 医生相关类型
export interface Doctor {
  doctor_id: number
  name: string
  department: string
  title?: string
  avatar_url?: string
  introduction?: string
  specialties?: string
  status: number
}

// 知识库相关类型
export interface MedicalKnowledge {
  knowledge_id: number
  title: string
  summary?: string
  keywords?: string
  content: string
  view_count: number
  status: number
}

export interface DrugInfo {
  drug_id: number
  drug_name: string
  generic_name?: string
  specification?: string
  manufacturer?: string
  usage?: string
  indication?: string
  contraindication?: string
  side_effect?: string
}

// 通知相关类型
export interface Notification {
  notification_id: number
  notification_type: string
  title: string
  content: string
  link_url?: string
  is_read: number
  created_at: string
}
