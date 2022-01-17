export interface Category {
  id: number;
  name: string;
  description: string;
  num_records?: number;
  created?: Date;
  updated?: Date;
}

export interface CategoryDraft
  extends Omit<Category, "id" | "num_records" | "created" | "updated"> {}

export interface Project {
  id: number;
  name: string;
  description: string;
  category: number;
  num_records?: number;
  created?: Date;
  updated?: Date;
}

export interface ProjectDraft
  extends Omit<Project, "id" | "num_records" | "created" | "updated"> {}

export interface TimeRecord {
  id: number;
  project: number;
  start_time: Date;
  stop_time: Date;
  total_seconds?: number;
  approved?: boolean;
}

export interface TimeRecordDraft
  extends Omit<
    TimeRecord,
    "id" | "start_time" | "stop_time" | "total_seconds"
  > {
  start_time?: Date;
  stop_time?: Date;
}
