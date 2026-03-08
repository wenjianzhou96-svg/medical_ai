/**
 * 医疗智能体系统 - 问诊API服务
 */

import request from '@/api/request'
import type { AxiosPromise } from 'axios'

// 问诊相关类型
export interface Consultation {
  consultation_id: number
  user_id: number
  doctor_id?: number
  title?: string
  symptoms?: string
  conversation_history?: ConversationMessage[]
  ai_suggestion?: string
  doctor_review?: string
  severity_level?: number
  status: number
  created_at: string
  updated_at?: string
}

export interface ConversationMessage {
  sender_type: string
  sender_id?: number
  content: string
  created_at: string
}

export interface Message {
  message_id: number
  consultation_id: number
  sender_type: string
  sender_id?: number
  content: string
  created_at: string
}

export interface Report {
  report_id: number
  consultation_id: number
  user_id: number
  report_type: string
  report_content?: Record<string, any>
  report_file_url?: string
  created_at: string
}

// 问诊列表响应
export interface ConsultationListResponse {
  items: Consultation[]
  total: number
  page: number
  page_size: number
}

// 创建问诊请求
export interface CreateConsultationRequest {
  title?: string
  symptoms: string
}

// 发送消息请求
export interface SendMessageRequest {
  message: string
}

// 发送消息响应
export interface SendMessageResponse {
  reply: string
  suggestion?: string
  is_emergency: boolean
  follow_up_questions: string[]
  messages: Message[]
}

// 生成报告请求
export interface GenerateReportRequest {
  report_type: string
}

// 医生审核请求
export interface DoctorReviewRequest {
  review_content: string
}

// 严重程度响应
export interface SeverityResponse {
  level: number
  label: string
  description: string
  is_emergency: boolean
}

// 统计响应
export interface StatisticsResponse {
  total: number
  completed: number
  in_progress: number
  pending_review: number
  cancelled: number
  emergency_count: number
  average_severity: number
}

// 问诊API服务
export const consultationApi = {
  /**
   * 创建问诊
   */
  create(data: CreateConsultationRequest): AxiosPromise<Consultation> {
    return request({
      url: '/consultations',
      method: 'post',
      data
    })
  },

  /**
   * 获取问诊列表
   */
  getList(params?: {
    page?: number
    page_size?: number
    status?: number
  }): AxiosPromise<ConsultationListResponse> {
    return request({
      url: '/consultations',
      method: 'get',
      params
    })
  },

  /**
   * 获取问诊详情
   */
  getDetail(consultationId: number): AxiosPromise<Consultation> {
    return request({
      url: `/consultations/${consultationId}`,
      method: 'get'
    })
  },

  /**
   * 发送消息
   */
  sendMessage(consultationId: number, data: SendMessageRequest): AxiosPromise<SendMessageResponse> {
    return request({
      url: `consultations/${consultationId}/messages`,
      method: 'post',
      data
    })
  },

  /**
   * 获取消息列表
   */
  getMessages(consultationId: number, params?: {
    skip?: number
    limit?: number
  }): AxiosPromise<Message[]> {
    return request({
      url: `consultations/${consultationId}/messages`,
      method: 'get',
      params
    })
  },

  /**
   * 完成问诊
   */
  finish(consultationId: number): AxiosPromise<Consultation> {
    return request({
      url: `consultations/${consultationId}/finish`,
      method: 'post'
    })
  },

  /**
   * 生成报告
   */
  generateReport(consultationId: number, data: GenerateReportRequest): AxiosPromise<Report> {
    return request({
      url: `consultations/${consultationId}/report`,
      method: 'post',
      data
    })
  },

  /**
   * 获取报告列表
   */
  getReports(consultationId: number): AxiosPromise<Report[]> {
    return request({
      url: `consultations/${consultationId}/reports`,
      method: 'get'
    })
  },

  /**
   * 获取严重程度
   */
  getSeverity(consultationId: number): AxiosPromise<SeverityResponse> {
    return request({
      url: `consultations/${consultationId}/severity`,
      method: 'get'
    })
  },

  /**
   * 取消问诊
   */
  cancel(consultationId: number): AxiosPromise<Consultation> {
    return request({
      url: `consultations/${consultationId}/cancel`,
      method: 'post'
    })
  },

  /**
   * 删除问诊记录
   */
  remove(consultationId: number): AxiosPromise<void> {
    return request({
      url: `/consultations/${consultationId}`,
      method: 'delete'
    })
  },

  // ========== 管理后台API ==========

  /**
   * 获取所有问诊列表（管理）
   */
  getAdminList(params?: {
    page?: number
    page_size?: number
    status?: number
    severity_level?: number
    user_id?: number
    doctor_id?: number
  }): AxiosPromise<ConsultationListResponse> {
    return request({
      url: `/consultations/admin/list`,
      method: 'get',
      params
    })
  },

  /**
   * 获取问诊详情（管理）
   */
  getAdminDetail(consultationId: number): AxiosPromise<Consultation> {
    return request({
      url: `consultations/admin/${consultationId}`,
      method: 'get'
    })
  },

  /**
   * 医生审核
   */
  doctorReview(consultationId: number, data: DoctorReviewRequest): AxiosPromise<Consultation> {
    return request({
      url: `consultations/admin/${consultationId}/review`,
      method: 'post',
      data
    })
  },

  /**
   * 获取问诊统计
   */
  getStatistics(): AxiosPromise<StatisticsResponse> {
    return request({
      url: `/consultations/admin/statistics`,
      method: 'get'
    })
  }
}

export default consultationApi
