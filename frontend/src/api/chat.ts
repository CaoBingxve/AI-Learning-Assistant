import request from "./request";

export interface ChatRequest{
  message: string
}

export interface ChatResponse{
  answer: string
}

export function chatApi(data:ChatRequest) {
  return request.post<ChatResponse>(
    "/chat",
    data
  )
}

export interface ChatMessage{
  role: 'user' | 'assistant',
  content: string
} 
export interface CopilotRequest
  extends ChatRequest {

  conversation_id: string
}

export function copilotApi(
  data: CopilotRequest
) {
  return request.post<ChatResponse>(
    '/chat/copilot',
    data
  )
}