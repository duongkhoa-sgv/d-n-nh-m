from pydantic import BaseModel
from typing import List, Optional

# Task statistics
class TaskStats(BaseModel):
    total: int
    completed: int
    in_progress: int
    pending: int

# Project statistics
class ProjectStats(BaseModel):
    total_projects: int
    ongoing_projects: int
    completed_projects: int
    overdue_projects: int

# Feedback statistics
class FeedbackStats(BaseModel):
    total_feedback: int
    processed: int
    unprocessed: int

# Team workload
class TeamWorkload(BaseModel):
    team_name: str
    assigned_tasks: int
    completed_tasks: int

# AI Suggestions
class AISuggestion(BaseModel):
    message: str

# Full dashboard response
class DashboardData(BaseModel):
    project_stats: ProjectStats
    task_stats: TaskStats
    feedback_stats: FeedbackStats
    team_workloads: Optional[List[TeamWorkload]] = []
    ai_suggestions: Optional[List[AISuggestion]] = []
