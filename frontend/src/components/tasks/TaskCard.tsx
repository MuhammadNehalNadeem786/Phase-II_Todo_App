import { Task } from '../../types/task';

interface TaskCardProps {
  task: Task;
  onToggle: (taskId: number) => void;
  onDelete: () => void;
  onEdit: () => void;
}

export default function TaskCard({
  task,
  onToggle,
  onDelete,
  onEdit,
}: TaskCardProps) {
  return (
    <li className={`px-4 py-4 ${task.completed ? 'bg-white/5' : 'bg-black'}`}>
      <div className="flex justify-between items-center">
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => onToggle(task.id)}
            className="h-4 w-4"
          />
          <div className="ml-3">
            <p className={task.completed ? 'line-through text-[#a1a1aa]' : 'text-white'}>
              {task.title}
            </p>
            {task.description && (
              <p className="text-sm text-[#a1a1aa]">
                {task.description}
              </p>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={onEdit}
            className="px-2 py-1 text-xs rounded border border-blue-500/30 text-blue-400 hover:bg-blue-900/30"
          >
            Edit
          </button>

          <button
            onClick={onDelete}
            className="px-2 py-1 text-xs rounded border border-red-500/30 text-red-400 hover:bg-red-900/30"
          >
            Delete
          </button>
        </div>
      </div>
    </li>
  );
}
