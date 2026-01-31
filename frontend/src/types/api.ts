export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}

export interface ErrorResponse {
  detail: string;
  status_code: number;
  error_type: string;
}