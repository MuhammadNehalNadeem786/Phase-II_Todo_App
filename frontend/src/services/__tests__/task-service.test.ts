// Mock the api client
jest.mock('../api-client', () => ({
  apiClientWithRetry: {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    patch: jest.fn(),
    delete: jest.fn(),
  }
}));

import { apiClientWithRetry } from '../api-client';
import { getTasks, createTask, updateTask, deleteTask, toggleTaskCompletion } from '../task-service';

describe('Task Service', () => {
  const userId = 'user123';
  const taskId = 1;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getTasks', () => {
    it('should fetch tasks for a user', async () => {
      const mockTasks = [{ id: 1, title: 'Test task', completed: false }];
      (apiClientWithRetry.get as jest.MockedFunction<any>).mockResolvedValueOnce({ data: mockTasks });

      const result = await getTasks(userId);

      expect(apiClientWithRetry.get).toHaveBeenCalledWith(`/users/${userId}/tasks`);
      expect(result).toEqual(mockTasks);
    });
  });

  describe('createTask', () => {
    it('should create a new task', async () => {
      const taskData = { title: 'New task', description: 'Task description' };
      const mockTask = { id: 123, ...taskData, user_id: userId };
      (apiClientWithRetry.post as jest.MockedFunction<any>).mockResolvedValueOnce({ data: mockTask });

      const result = await createTask(userId, taskData);

      expect(apiClientWithRetry.post).toHaveBeenCalledWith(`/users/${userId}/tasks`, {
        ...taskData,
        user_id: userId
      });
      expect(result).toEqual(mockTask);
    });
  });

  describe('updateTask', () => {
    it('should update a task', async () => {
      const taskData = { title: 'Updated task', completed: true };
      const mockTask = { id: taskId, ...taskData, user_id: userId };
      (apiClientWithRetry.put as jest.MockedFunction<any>).mockResolvedValueOnce({ data: mockTask });

      const result = await updateTask(userId, taskId, taskData);

      expect(apiClientWithRetry.put).toHaveBeenCalledWith(`/users/${userId}/tasks/${taskId}`, taskData);
      expect(result).toEqual(mockTask);
    });
  });

  describe('deleteTask', () => {
    it('should delete a task', async () => {
      (apiClientWithRetry.delete as jest.MockedFunction<any>).mockResolvedValueOnce({ status: 204 });

      const result = await deleteTask(userId, taskId);

      expect(apiClientWithRetry.delete).toHaveBeenCalledWith(`/users/${userId}/tasks/${taskId}`);
      expect(result).toBe(true);
    });
  });

  describe('toggleTaskCompletion', () => {
    it('should toggle task completion status', async () => {
      const completed = true;
      const mockTask = { id: taskId, title: 'Test task', completed };
      (apiClientWithRetry.patch as jest.MockedFunction<any>).mockResolvedValueOnce({ data: mockTask });

      const result = await toggleTaskCompletion(userId, taskId, completed);

      expect(apiClientWithRetry.patch).toHaveBeenCalledWith(`/users/${userId}/tasks/${taskId}/complete`, {
        completed
      });
      expect(result).toEqual(mockTask);
    });
  });
});