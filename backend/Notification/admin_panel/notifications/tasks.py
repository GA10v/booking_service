import logging

from celery import shared_task  # type: ignore[attr-defined]

from generator.src.service.main import EventType, ProcessTask, Task  # noqa: F401

logger = logging.getLogger(__name__)


@shared_task(name='Создать задачу new_content')
def create_new_content_task(*args, task_id: str, **kwargs):
    # task = Task(event_type=EventType.new_content, context=kwargs)  # noqa: E800
    generator = ProcessTask()
    task = generator._get_task(task_id)
    generator.perform_task(task)


@shared_task(name='Создать задачу new_promo')
def create_new_promo_task(*args, task_id: str, **kwargs):
    # task = Task(event_type=EventType.promo, context=kwargs)  # noqa: E800
    generator = ProcessTask()
    task = generator._get_task(task_id)
    generator.perform_task(task)


@shared_task(name='Создать задачу new_likes')
def create_new_likes_task(*args, task_id: str, **kwargs):
    # task = Task(event_type=EventType.new_likes, context=kwargs)  # noqa: E800
    generator = ProcessTask()
    task = generator._get_task(task_id)
    generator.perform_task(task)


@shared_task(bind=True, name='Debug')
def hello_world(self):
    print('Hi ========================')  # noqa: T201
