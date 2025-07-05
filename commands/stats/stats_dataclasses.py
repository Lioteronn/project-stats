from dataclasses import dataclass

from models.users import Rank, RankDivision, UserStatsInfo


@dataclass
class UserStats:
    user_steam_id: str
    user_steam_url: str
    level: int
    current_rank: Rank
    current_rank_division: RankDivision
    wins: int
    goals: int
    shots: int
    assists: int
    saves: int
    steals: int
    tackles: int
    mvps: int
    total_wins: int
    total_losses: int

    @property
    def shot_accuracy(self) -> float:
        """Calculate shot accuracy as percentage"""
        return (self.goals / self.shots * 100) if self.shots > 0 else 0.0

    @property
    def win_rate(self) -> float:
        """Calculate win rate as percentage"""
        total_games = self.total_wins + self.total_losses
        return (self.total_wins / total_games * 100) if total_games > 0 else 0.0

    @property
    def save_percentage(self) -> float:
        """Calculate save percentage based on shots faced (estimated)"""
        # Assuming shots faced = shots + goals (simplified estimation)
        shots_faced = self.shots + self.goals
        return (self.saves / shots_faced * 100) if shots_faced > 0 else 0.0

    @property
    def goals_per_game(self) -> float:
        """Calculate average goals per game"""
        total_games = self.total_wins + self.total_losses
        return self.goals / total_games if total_games > 0 else 0.0

    @property
    def assists_per_game(self) -> float:
        """Calculate average assists per game"""
        total_games = self.total_wins + self.total_losses
        return self.assists / total_games if total_games > 0 else 0.0

    @classmethod
    def from_model(cls, model: UserStatsInfo) -> "UserStats":
        """Create UserStats from UserStatsInfo model"""
        return cls(
            user_steam_id=model.user_steam_id,
            user_steam_url=model.user_steam_url,
            level=model.level,
            current_rank=Rank(model.current_rank),
            current_rank_division=RankDivision(model.current_rank_division),
            wins=model.wins,
            goals=model.goals,
            shots=model.shots,
            assists=model.assists,
            saves=model.saves,
            steals=model.steals,
            tackles=model.tackles,
            mvps=model.mvps,
            total_wins=model.total_wins,
            total_losses=model.total_losses,
        )
