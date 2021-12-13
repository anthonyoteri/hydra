export interface Category {
  id: number;
  name: string;
  description: string;
  created?: Date;
  updated?: Date;
}

export interface CategoryDraft
  extends Omit<Category, "id" | "created" | "updated"> {}

export interface Project {
  id: number;
  name: string;
  description: string;
  category: number;
  created?: Date;
  updated?: Date;
}

export interface ProjectDraft
  extends Omit<Project, "id" | "created" | "updated"> {}

export interface TimeRecord {
  id: number;
  project: number;
  start_time: Date;
  stop_time: Date;
  total_seconds?: number;
}

export interface TimeRecordDraft
  extends Omit<
    TimeRecord,
    "id" | "start_time" | "stop_time" | "total_seconds"
  > {
  start_time?: Date;
  stop_time?: Date;
}
