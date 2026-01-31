import { useState, useEffect } from 'react';
import { CreateTaskRequest, Task } from '../../types/task';

interface TaskFormProps {
  userId: string;
  onSubmit: (taskData: CreateTaskRequest) => void;
  onCancel: () => void;
  initialData?: Task;
}

export default function TaskForm({
  userId,
  onSubmit,
  onCancel,
  initialData,
}: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');

  // 🔁 Populate form when editing
  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title);
      setDescription(initialData.description ?? '');
    }
  }, [initialData]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (title.length > 255) {
      setError('Title must be 255 characters or less');
      return;
    }

    if (description.length > 1000) {
      setError('Description must be 1000 characters or less');
      return;
    }

    setError('');
    onSubmit({
      title: title.trim(),
      description: description.trim(),
      user_id: userId,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="rounded-md bg-red-900/30 p-4 border border-red-800/50">
          <h3 className="text-sm font-medium text-red-300">{error}</h3>
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-white">Title *</label>
        <input
          value={title}
          onChange={e => setTitle(e.target.value)}
          className="mt-1 block w-full rounded-md border border-white/20 bg-black p-2 text-white"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-white">
          Description
        </label>
        <textarea
          rows={3}
          value={description}
          onChange={e => setDescription(e.target.value)}
          className="mt-1 block w-full rounded-md border border-white/20 bg-black p-2 text-white"
        />
      </div>

      <div className="flex justify-end space-x-3">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm text-[#a1a1aa] hover:bg-white/10 rounded"
        >
          Cancel
        </button>

        <button
          type="submit"
          className="px-4 py-2 text-sm bg-white text-black rounded"
        >
          {initialData ? 'Update Task' : 'Add Task'}
        </button>
      </div>
    </form>
  );
}
