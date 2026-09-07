import request from "./request";

export interface RecordCreate{
  title: string,
  content: string,
  study_time:number
}

export interface RecordResponse{
  id: number,
  user_id: number,
  title: string,
  content: string,
  study_time: number,
  // 后端返回的是ISO时间字符串
  created_at:string
}

// 创建学习记录
export function createRecordApi(data: RecordCreate) {
  return request.post<RecordResponse>(
    "/records",data
  )
}

// 获取当前用户全部学习记录
export function getRecordsApi() {
  return request.get<RecordResponse[]>('/records')
}