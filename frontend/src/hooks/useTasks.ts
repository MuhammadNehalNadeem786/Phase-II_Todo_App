// import { useState, useEffect } from 'react';
// import { Task } from '../types/task';
// import {
//   getTasks,
//   createTask,
//   updateTask,
//   deleteTask,
//   toggleTaskCompletion,
// } from '../services/task-service';
// import { ApiResponse } from '../types/api';

// /**
//  * useTasks Hook
//  * ------------------
//  * Responsibility:
//  * - Handle task CRUD state
//  * - Communicate with backend services
//  * - Keep React state strictly typed as Task[]
//  *
//  * IMPORTANT RULE:
//  * - NEVER store ApiResponse in state
//  * - Always unwrap response.data first
//  */
// export const useTasks = () => {
//   // ------------------------------
//   // STATE
//   // ------------------------------
//   const [tasks, setTasks] = useState<Task[]>([]);
//   const [loading, setLoading] = useState<boolean>(true);
//   const [error, setError] = useState<string | null>(null);

//   /**
//    * Utility:
//    * Ensures only valid Task objects are stored in state
//    * Prevents backend garbage or malformed responses
//    */
//   const toTaskArray = (arr: unknown[]): Task[] =>
//     arr.filter(
//       (item): item is Task =>
//         typeof item === 'object' &&
//         item !== null &&
//         'id' in item &&
//         'title' in item &&
//         'completed' in item
//     );

//   // ------------------------------
//   // FETCH TASKS ON FIRST LOAD
//   // ------------------------------
//   useEffect(() => {
//     fetchTasks();
//   }, []);

//   /**
//    * GET /tasks
//    * Loads all tasks for logged-in user (JWT-based)
//    */
//   const fetchTasks = async () => {
//     try {
//       setLoading(true);
//       setError(null);

//       // Service already returns Task[]
//       const data = await getTasks();
//       setTasks(Array.isArray(data) ? toTaskArray(data) : []);
//     } catch (err) {
//       setError('Failed to fetch tasks');
//       console.error(err);
//     } finally {
//       setLoading(false);
//     }
//   };

//   /**
//    * POST /tasks
//    * Creates a task with optimistic UI update
//    */
//   const addTask = async (taskData: {
//     title: string;
//     description?: string;
//     completed?: boolean;
//   }) => {
//     /**
//      * TEMP ID
//      * - Prevents UI freeze
//      * - Avoids sending fake ID to backend
//      * - Backend replaces it later
//      */
//     const tempId = -Date.now();

//     const tempTask: Task = {
//       id: tempId,
//       title: taskData.title,
//       description: taskData.description,
//       completed: taskData.completed ?? false,
//       user_id: 'temp',
//       created_at: new Date().toISOString(),
//       updated_at: new Date().toISOString(),
//     };

//     // Optimistic UI update
//     setTasks(prev => [...prev, tempTask]);

//     try {
//       const response: ApiResponse<Task> = await createTask(taskData);
//       const newTask = response.data;

//       // Replace temp task with real backend task
//       if (newTask) {
//         setTasks(prev =>
//           prev.map(task => (task.id === tempId ? newTask : task))
//         );
//       }

//       return newTask;
//     } catch (err) {
//       // Rollback optimistic update
//       setTasks(prev => prev.filter(task => task.id !== tempId));
//       setError('Failed to create task');
//       console.error(err);
//       throw err;
//     }
//   };

//   /**
//    * PUT /tasks/{id}
//    * Updates task fields (title, description, completed)
//    */
//   const updateTaskById = async (
//     taskId: number,
//     taskData: { title?: string; description?: string; completed?: boolean }
//   ) => {
//     // Ignore temp tasks (not yet in DB)
//     if (taskId < 0) return;

//     // Optimistic UI update
//     setTasks(prev =>
//       prev.map(task =>
//         task.id === taskId ? { ...task, ...taskData } : task
//       )
//     );

//     try {
//       const response: ApiResponse<Task> = await updateTask(taskId, taskData);
//       const updatedTask = response.data;

//       if (updatedTask) {
//         setTasks(prev =>
//           prev.map(task => (task.id === taskId ? updatedTask : task))
//         );
//       }

//       return updatedTask;
//     } catch (err) {
//       setError('Failed to update task');
//       console.error(err);
//       throw err;
//     }
//   };

//   /**
//    * DELETE /tasks/{id}
//    * Removes task from DB
//    */
//   const removeTask = async (taskId: number) => {
//     const removedTask = tasks.find(task => task.id === taskId);
//     if (!removedTask) return;

//     // Optimistic removal
//     setTasks(prev => prev.filter(task => task.id !== taskId));

//     // Skip backend call for temp task
//     if (taskId < 0) return;

//     try {
//       await deleteTask(taskId);
//     } catch (err) {
//       // Rollback on failure
//       setTasks(prev => [...prev, removedTask]);
//       setError('Failed to delete task');
//       console.error(err);
//       throw err;
//     }
//   };

//   /**
//    * PATCH /tasks/{id}/complete
//    * Toggles completed status
//    */
//   const toggleCompletion = async (taskId: number) => {
//     const task = tasks.find(t => t.id === taskId);
//     if (!task) return;

//     // Optimistic toggle
//     setTasks(prev =>
//       prev.map(t =>
//         t.id === taskId ? { ...t, completed: !t.completed } : t
//       )
//     );

//     // Skip temp task
//     if (taskId < 0) return;

//     try {
//       const response: ApiResponse<Task> = await toggleTaskCompletion(
//         taskId,
//         !task.completed
//       );
//       const updatedTask = response.data;

//       if (updatedTask) {
//         setTasks(prev =>
//           prev.map(t => (t.id === taskId ? updatedTask : t))
//         );
//       }

//       return updatedTask;
//     } catch (err) {
//       // Rollback toggle
//       setTasks(prev =>
//         prev.map(t =>
//           t.id === taskId ? { ...t, completed: task.completed } : t
//         )
//       );
//       setError('Failed to toggle task completion');
//       console.error(err);
//       throw err;
//     }
//   };

//   // ------------------------------
//   // PUBLIC API OF HOOK
//   // ------------------------------
//   return {
//     tasks,
//     loading,
//     error,
//     fetchTasks,
//     addTask,
//     updateTaskById,
//     removeTask,
//     toggleCompletion,
//   };
// };





import { useState, useEffect } from 'react';
import { Task } from '../types/task';
import {
  getTasks,
  createTask,
  updateTask,
  deleteTask,
  toggleTaskCompletion,
} from '../services/task-service';
import { ApiResponse } from '../types/api';

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const toTaskArray = (arr: unknown[]): Task[] =>
    arr.filter(
      (item): item is Task =>
        typeof item === 'object' &&
        item !== null &&
        'id' in item &&
        'title' in item &&
        'completed' in item
    );

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await getTasks();
      setTasks(Array.isArray(data) ? toTaskArray(data) : []);
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (taskData: {
    title: string;
    description?: string;
    completed?: boolean;
  }) => {
    const tempId = -Date.now();

    const tempTask: Task = {
      id: tempId,
      title: taskData.title,
      description: taskData.description,
      completed: taskData.completed ?? false,
      user_id: 'temp',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    setTasks(prev => [...prev, tempTask]);

    try {
      const response: ApiResponse<Task> = await createTask(taskData);
      const newTask = response.data;

      if (newTask) {
        setTasks(prev =>
          prev.map(task => (task.id === tempId ? newTask : task))
        );
      }

      return newTask;
    } catch (err) {
      setTasks(prev => prev.filter(task => task.id !== tempId));
      setError('Failed to create task');
      console.error(err);
      throw err;
    }
  };

  const updateTaskById = async (
    taskId: number,
    taskData: { title?: string; description?: string; completed?: boolean }
  ) => {
    if (taskId < 0) return;

    setTasks(prev =>
      prev.map(task =>
        task.id === taskId ? { ...task, ...taskData } : task
      )
    );

    try {
      const response: ApiResponse<Task> = await updateTask(taskId, taskData);
      const updatedTask = response.data;

      if (updatedTask) {
        setTasks(prev =>
          prev.map(task => (task.id === taskId ? updatedTask : task))
        );
      }

      return updatedTask;
    } catch (err) {
      setError('Failed to update task');
      console.error(err);
      throw err;
    }
  };

  const removeTask = async (taskId: number) => {
    const removedTask = tasks.find(task => task.id === taskId);
    if (!removedTask) return;

    setTasks(prev => prev.filter(task => task.id !== taskId));

    if (taskId < 0) return;

    try {
      await deleteTask(taskId);
    } catch (err) {
      setTasks(prev => [...prev, removedTask]);
      setError('Failed to delete task');
      console.error(err);
      throw err;
    }
  };

  const toggleCompletion = async (taskId: number) => {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    setTasks(prev =>
      prev.map(t =>
        t.id === taskId ? { ...t, completed: !t.completed } : t
      )
    );

    if (taskId < 0) return;

    try {
      const response: ApiResponse<Task> = await toggleTaskCompletion(
        taskId,
        !task.completed
      );
      const updatedTask = response.data;

      if (updatedTask) {
        setTasks(prev =>
          prev.map(t => (t.id === taskId ? updatedTask : t))
        );
      }

      return updatedTask;
    } catch (err) {
      setTasks(prev =>
        prev.map(t =>
          t.id === taskId ? { ...t, completed: task.completed } : t
        )
      );
      setError('Failed to toggle task completion');
      console.error(err);
      throw err;
    }
  };

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    addTask,
    updateTaskById,
    removeTask,
    toggleCompletion,
  };
};
