from datetime import datetime
from typing import Optional

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase
from playhouse.postgres_ext import JSONField

from pht.bot import config, scheduler
from pht.data import SCHEDULER_FORGET_IF_MISSED_SECONDS

db = PooledPostgresqlExtDatabase(
    config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    port=config.DB_PORT,
    max_connections=8,
    stale_timeout=300,
)

ts_default = datetime.utcnow


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username: str = CharField()
    full_name: str = CharField()
    created_at: datetime = DateTimeField(default=ts_default)
    rating_privacy: str = CharField(default="private")  # 'public'
    time_to_ask: str = CharField(default="22:00")  # '22:00'
    scheduler_job_id: Optional[str] = CharField()

    def __repr__(self):
        return f"<User: {self.username} / {self.full_name}>"

    def __str__(self):
        return self.__repr__()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_up_scheduler_job()

    def _get_cron_trigger(self):
        hours, minutes = self.time_to_ask.split(":")
        # FIXME: development/debugging purposes only
        return IntervalTrigger(seconds=10)
        # every day at hh:mm
        return CronTrigger(hour=hours, minute=minutes)

    def set_up_scheduler_job(self):
        scheduler_job_id = f"user_{self.id}_scheduler"
        from pht.scheduler_jobs import ask_about_day_job

        scheduler.add_job(
            ask_about_day_job,
            trigger=self._get_cron_trigger(),
            args=(self,),
            misfire_grace_time=SCHEDULER_FORGET_IF_MISSED_SECONDS,
            id=scheduler_job_id,
            replace_existing=True,
        )
        self.scheduler_job_id = scheduler_job_id

    def reschedule_scheduler_job(self):
        """
        This method should be called when `User.time_to_ask` is changed
        """
        scheduler.reschedule_job(
            self.scheduler_job_id, trigger=self._get_cron_trigger()
        )

    def remove_scheduler_job(self):
        if self.scheduler_job_id:
            scheduler.remove_job(self.scheduler_job_id)


class Habit(BaseModel):
    owner: User = ForeignKeyField(User, backref="habits")
    name: str = CharField()
    answer_type: str = CharField()  # 'bool' or 'integer'
    regularity: str = IntegerField()  # 3 (times a week)
    created_at: datetime = DateTimeField(default=ts_default)

    def __repr__(self):
        return f"<Habit: {self.name}, {self.answer_type}, {self.regularity}, owner: {self.owner}>"

    def __str__(self):
        return self.__repr__()


class Answer(BaseModel):
    habit: Habit = ForeignKeyField(Habit, backref="answers")
    content: int = IntegerField()
    description: str = CharField()  # "valid_reason" or other explanation
    date: datetime = DateTimeField(default=ts_default)
    changed_at: datetime = DateTimeField(default=ts_default)


class Event(BaseModel):
    ts: datetime = DateTimeField(default=ts_default)
    type: str = CharField()
    data: dict = JSONField()


with db:
    db.create_tables([User, Habit, Answer, Event])