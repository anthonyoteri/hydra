export interface Category {
  id: number;
  name: string;
  description: string;
  created: Date;
  updated: Date;
}

export interface Project {
  id: number;
  name: string;
  slug: string;
  description: string;
  category: string | number;
  created: Date;
  updated: Date;
}

export interface TimeRecord {
  id: number;
  project: string;
  start_time: Date;
  stop_time: Date;
  total_seconds: number;
}