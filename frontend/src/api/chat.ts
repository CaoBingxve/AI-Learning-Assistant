import request from './request'

export interface CopilotRequest {
  message: string
  conversation_id: string
}

export interface ChatResponse {
  answer: string
}

export function copilotApi(
  data: CopilotRequest
) {
  return request.post<ChatResponse>(
    '/chat/copilot',
    data
  )
}