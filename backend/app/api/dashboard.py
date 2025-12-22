from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.dashboard import DashboardData, ProjectStats, TaskStats, FeedbackStats, TeamWorkload, AISuggestion

router = APIRouter()

# Dummy users for role-based testing
class User:
    def __init__(self, username: str, role: str):
        self.username = username
        self.role = role

# Simulate user auth (replace with JWT/session in real app)
def get_current_user():
    # Example: return PM
    return User(username="pm_john", role="Admin")
    # To test other roles, change role to "Admin", "Contributor", "Reviewer"

# Dummy dashboard data
full_dashboard = DashboardData(
    project_stats=ProjectStats(total_projects=12, ongoing_projects=8, completed_projects=3, overdue_projects=1),
    task_stats=TaskStats(total=50, completed=30, in_progress=15, pending=5),
    feedback_stats=FeedbackStats(total_feedback=20, processed=12, unprocessed=8),
    team_workloads=[
        TeamWorkload(team_name="Backend Team", assigned_tasks=20, completed_tasks=15),
        TeamWorkload(team_name="Frontend Team", assigned_tasks=15, completed_tasks=10),
    ],
    ai_suggestions=[
        AISuggestion(message="Redistribute 2 tasks from Backend Team to Frontend Team"),
        AISuggestion(message="Create new sprint for overdue tasks")
    ]
)

# Role-based filtering function
def filter_dashboard_for_role(user: User) -> DashboardData:
    if user.role == "Admin":
        return full_dashboard
    elif user.role == "PM":
        # PM sees all project/task stats + team workloads + AI suggestions
        return full_dashboard
    elif user.role == "Contributor":
        # Contributor sees only tasks assigned to them + AI suggestions (optional)
        contributor_dashboard = DashboardData(
            project_stats=full_dashboard.project_stats,
            task_stats=TaskStats(
                total=full_dashboard.task_stats.total,
                completed=10,  # only tasks assigned to this contributor
                in_progress=5,
                pending=2
            ),
            feedback_stats=FeedbackStats(
                total_feedback=0,
                processed=0,
                unprocessed=0
            ),
            team_workloads=[],
            ai_suggestions=[]
        )
        return contributor_dashboard
    elif user.role == "Reviewer":
        # Reviewer sees feedback stats only
        reviewer_dashboard = DashboardData(
            project_stats=ProjectStats(total_projects=0, ongoing_projects=0, completed_projects=0, overdue_projects=0),
            task_stats=TaskStats(total=0, completed=0, in_progress=0, pending=0),
            feedback_stats=full_dashboard.feedback_stats,
            team_workloads=[],
            ai_suggestions=[]
        )
        return reviewer_dashboard
    else:
        raise HTTPException(status_code=403, detail="Role not allowed")

# Endpoint
@router.get("/", response_model=DashboardData)
def get_dashboard(current_user: User = Depends(get_current_user)):
    """
    Get Dashboard data based on user role
    """
    return filter_dashboard_for_role(current_user)
