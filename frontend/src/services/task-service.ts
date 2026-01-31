import apiClientWithRetry from './api-client';
import { ApiResponse } from '../types/api';
import { Task } from '../types/task';

// Get all tasks for the logged-in user (from JWT)
export const getTasks = async () => {
  try {
    const response = await apiClientWithRetry.get<ApiResponse<Task[]>>(`/signup/users/from-token/tasks`);
    return response.data ?? [];
  } catch (error) {
    throw error;
  }
};

export const createTask = async (taskData: { title: string; description?: string; completed?: boolean }) => {
  try {
    const response = await apiClientWithRetry.post<ApiResponse<Task>>(
      `/signup/users/from-token/tasks`,
      taskData
    );
    if (!response.data) throw new Error('Task creation failed: no data returned');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateTask = async (taskId: number, taskData: { title?: string; description?: string; completed?: boolean }) => {
  try {
    const response = await apiClientWithRetry.put<ApiResponse<Task>>(
      `/signup/users/from-token/tasks/${taskId}`,
      taskData
    );
    if (!response.data) throw new Error('Task update failed: no data returned');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteTask = async (taskId: number) => {
  try {
    await apiClientWithRetry.delete(`/signup/users/from-token/tasks/${taskId}`);
    return true;
  } catch (error) {
    throw error;
  }
};

export const toggleTaskCompletion = async (taskId: number, completed: boolean) => {
  try {
    const response = await apiClientWithRetry.patch<ApiResponse<Task>>(
      `/signup/users/from-token/tasks/${taskId}/complete`,
      { completed }
    );
    if (!response.data) throw new Error('Task completion toggle failed: no data returned');
    return response.data;
  } catch (error) {
    throw error;
  }
};
