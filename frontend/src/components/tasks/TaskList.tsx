'use client';

import { useState } from 'react';
import TaskCard from './TaskCard';
import TaskForm from './TaskForm';
import { useTasks } from '../../hooks/useTasks';
import { Task } from '../../types/task';

interface TaskListProps {
  userId: string;
}

export default function TaskList({ userId }: TaskListProps) {
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  const {
    tasks,
    loading,
    error,
    addTask,
    updateTaskById,
    toggleCompletion,
    removeTask,
  } = useTasks();

  if (loading) {
    return (
      <div className="flex justify-center items-center py-10">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-white/30"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900/30 border border-red-800/50 text-red-300 px-4 py-3 rounded">
        <strong>Error:</strong> {error}
      </div>
    );
  }

  return (
    <div className="bg-black border border-white/10 rounded-md overflow-hidden">
      {/* Header */}
      <div className="px-4 py-5 border-b border-white/10 flex justify-between items-center">
        <h3 className="text-lg font-medium text-white">Your Tasks</h3>

        <button
          onClick={() => {
            setShowForm(prev => !prev);
            setEditingTask(null);
          }}
          className="px-4 py-2 border border-white/20 bg-white/10 hover:bg-white/20 text-white text-sm rounded"
        >
          {showForm ? 'Cancel' : 'Add Task'}
        </button>
      </div>

      {/* Form */}
      {(showForm || editingTask) && (
        <div className="px-4 py-5 border-b border-white/10">
          <TaskForm
            userId={userId}
            initialData={editingTask ?? undefined}
            onSubmit={async data => {
              if (editingTask) {
                await updateTaskById(editingTask.id, data);
                setEditingTask(null);
              } else {
                await addTask(data);
                setShowForm(false);
              }
            }}
            onCancel={() => {
              setShowForm(false);
              setEditingTask(null);
            }}
          />
        </div>
      )}

      {/* Empty state */}
      {tasks.length === 0 ? (
        <div className="text-center py-10 text-[#a1a1aa]">
          No tasks yet. Add one!
        </div>
      ) : (
        <ul className="divide-y divide-white/10">
          {tasks.map(task => (
            <TaskCard
              key={task.id}
              task={task}
              onToggle={toggleCompletion}
              onDelete={() => removeTask(task.id)}
              onEdit={() => {
                setEditingTask(task);
                setShowForm(false);
              }}
            />
          ))}
        </ul>
      )}
    </div>
  );
}
