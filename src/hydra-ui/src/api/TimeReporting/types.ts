export interface Category {
  id: number;
  name: string;
  description: string;
  created: datetime;
  updated: datetime;
}

export interface Project {
  id: number;
  name: string;
  slug: string;
  description: string;
  category: string | number;
  created: datetime;
  updated: datetime;
}

export interface TimeRecord {
  id: number;
  project: string;
  start_time: datetime;
  stop_time: datetime;
  total_seconds: number;
}
