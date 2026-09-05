import request from "./request";

export interface loginData{
  username: string,
  password: string
}

export interface loginResponse{
  access_token: string,
  token_type:string
}

export function loginApi(data:loginData) {
  return request.post<loginResponse>(
    "/users/login",
    data
  )
}