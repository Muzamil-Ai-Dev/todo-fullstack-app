export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string | null;
  completed: boolean;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}