export interface BaseCursorResponse<T> {
  items: T[];
  next_cursor: string | null;
  previous_cursor: string | null;
  limit: number;
}

export interface BaseProgramResponse {
  id: string;
  name: string;
  degree_type: string;
  application_deadline: string;
}

export interface DetailedProgramResponse {
  id: string;
  name: string;
  degree_type: string;
  application_deadline: string;
  requirements: Array<{
    id: string;
    title: string;
    type: string;
    description: string;
    evidence_type: string;
    due_offset_days: number;
    required: boolean;
  }>;
}

export interface BaseApplicationResponse {
  id: string;
  created_at: string;
  program: {
    id: string;
    name: string;
    application_deadline: string;
  };
}

export interface DetailedApplicationResponse {
  id: string;
  created_at: string;
  program: {
    id: string;
    name: string;
    degree_type: string;
    application_deadline: string;
  };
  checklist_items: Array<{
    id: string;
    requirement_id: string;
    requirement_title: string;
    requirement_type: string;
    required: boolean;
    status: string;
    due_date: string;
    notes: string;
  }>;
}

export interface TimelineResponse {
  id: string;
  title: string;
  date: string;
  status: string;
  checklist_item: {
    id: string;
    requirement_id: string;
    requirement_title: string;
    requirement_type: string;
    required: boolean;
    status: string;
    due_date: string;
    notes: string;
  };
}

export interface ReadinessResponse {
  readiness_score: number;
  missing_requirements: Array<{
    requirement_id: string;
    title: string;
    type: string;
    due_date: string;
  }>;
  next_milestones: Array<{
    title: string;
    date: string;
    status: string;
  }>;
  checklist_items: Array<{
    id: string;
    requirement_id: string;
    requirement_title: string;
    requirement_type: string;
    required: boolean;
    status: string;
    due_date: string;
    notes: string;
  }>;
}

export interface ProfileOut {
  id: string;
  name: string;
  family_name: string;
  email: string;
  gpa: number;
  target_term: string;
}

export interface ApplicationPreview {
  id: string;
  created_at: string;
  program: {
    id: string;
    name: string;
    degree_type: string;
    application_deadline: string;
  };
  readiness_score: number;
  next_milestone: {
    title: string;
    date: string;
    status: string;
  };
}
