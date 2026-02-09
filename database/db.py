"""
Database Operations
Barcha database operatsiyalari - Modular struktura
"""
import config
from .operations.user_ops import UserOperations
from .operations.transaction_ops import TransactionOperations
from .operations.goal_ops import GoalOperations
from .operations.diary_ops import DiaryOperations
from .operations.admin_ops import AdminOperations


class Database(
    UserOperations,
    TransactionOperations,
    GoalOperations,
    DiaryOperations,
    AdminOperations
):
    """Barcha database operatsiyalari - Bir joyda"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.DATABASE_PATH
