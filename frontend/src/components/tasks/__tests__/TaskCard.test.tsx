import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TaskCard from '../TaskCard';
import { Task } from '../../../types/task';

describe('TaskCard', () => {
  const mockTask: Task = {
    id: 1,
    title: 'Test Task',
    description: 'Test Description',
    completed: false,
    user_id: 'user123',
    created_at: '2023-01-01T00:00:00Z',
    updated_at: '2023-01-01T00:00:00Z',
  };

  const mockOnToggle = jest.fn();
  const mockOnDelete = jest.fn();

  it('renders task title and description', () => {
    render(
      <TaskCard
        task={mockTask}
        onToggle={mockOnToggle}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  it('renders checkbox with correct state', () => {
    render(
      <TaskCard
        task={{ ...mockTask, completed: false }}
        onToggle={mockOnToggle}
        onDelete={mockOnDelete}
      />
    );

    const checkbox = screen.getByRole('checkbox');
    expect(checkbox).not.toBeChecked();

    render(
      <TaskCard
        task={{ ...mockTask, completed: true }}
        onToggle={mockOnToggle}
        onDelete={mockOnDelete}
      />
    );

    const checkedCheckbox = screen.getByRole('checkbox');
    expect(checkedCheckbox).toBeChecked();
  });

  it('calls onToggle when checkbox is clicked', () => {
    render(
      <TaskCard
        task={mockTask}
        onToggle={mockOnToggle}
        onDelete={mockOnDelete}
      />
    );

    fireEvent.click(screen.getByRole('checkbox'));
    expect(mockOnToggle).toHaveBeenCalled();
  });

  it('calls onDelete when delete button is clicked', () => {
    render(
      <TaskCard
        task={mockTask}
        onToggle={mockOnToggle}
        onDelete={mockOnDelete}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /delete/i }));
    expect(mockOnDelete).toHaveBeenCalled();
  });

  it('applies strikethrough to title and description when completed', () => {
    render(
      <TaskCard
        task={{ ...mockTask, completed: true }}
        onToggle={mockOnToggle}
        onDelete={mockOnDelete}
      />
    );

    const titleElement = screen.getByText('Test Task');
    expect(titleElement).toHaveClass('line-through');
  });
});