## Сервис бронирования билетов

- [*] - задание со звездочкой
- [?] - что-то не понятно

## Легенда

Хочется посмотреть фильм/сериал, но не хочется тупить в одного или ты в новом городе и здесь нет знакомых...
Заходишь на PRACTIX, выбираешь фильм, жмешь кнопку "Кино в компании".
Есть возможность пойти на просмотр гостем, ищи события с учетом даты, локации, приватности, дополнительным условиям и [*]рейтингу организаторов.
Или создать свой фест с блекджеком и куртизанками! Назначай дату, зови друзей или весь мир, ограничивай число гостей, принимай заявки от гостей и выбирай кто достоин сидеть на твоем диване

### 1. Сценарий организатор

- для конкретного фильна создается объявдение (Announcement):

  - название Announcement
  - описание Announcement
  - дата Announcement
  - место Announcement
  - приватность Announcement
  - цена Announcement (можно bool)
  - [*] указать гостей (отправить им инвайты)

- для Announcement создаются Booking (one_to_many):

  - автору приходит заявка на участие в Announcement от гостя (в Booking {'author' : None, 'guest' : True})
  - автор может посмотреть статус всех записей в Booking для своего Announcement и редактировать их (отклонить уже принятую заявку)
  - как только запись в Booking {'author' : True, 'guest' : True}, в Announcement можно посмотреть список участников
  - [*] автор отправляет инвайт гостю на участие в Announcement ( в Booking {'author' : True, 'guest' : None} )

### 2. Сценарий гость

- для конкретного фильма есть несколько Announcement:

  - посмотреть список всех доступных Announcements
  - посмотреть информацию по конкретному Announcements
  - отправить заявку на участие (нужна проверка на уникальность, гость не может быть на нескольких событиях одновременно)
  - [*] пришел инвайт гостю на участие в Announcement ( в Booking {'author' : True, 'guest' : None} )

- для Announcement создается Booking:
  - гость отправляет заявку на участие в Announcement (в Booking {'author' : None, 'guest' : True})
  - как только запись в Booking {'author' : True, 'guest' : True}, в Announcement можно посмотреть список участников
  - [*] от автора пришел инвайт гостю на участие в Announcement ( в Booking {'author' : True, 'guest' : None} )

### 3. Сценарий Notifications

- Если организатор изменит объявление - все участники события получают уведомление и короткую ссылку на новое объявление
- Изменения в Booking (запросы, инвайты, подтверждения заявок, отклонения заявок) - организатор и гость получают уведомление и короткую ссылку на новое объявление
- За день до события всем участникам приходит уведомление и короткая ссылка на объявление
- В день события (за час) всем участникам приходит уведомление и короткая ссылка на объявление

### [\*][?] 4. Сценарий Rating

- после проведения события, всем участникам приходит сообщение "оцените событие" - продумать
- [1] у каждого пользователя есть оценка "организатор" - продумать
- [1] у каждого пользователя есть оценка "гость" - продумать
- [2] у каждого пользователя есть общая оценка - продумать
- Где хранить информацию о рейтинге пользователя? - продумать, может хранить в UGC (будет ли дублироваться БД)
- Какуб БД выбрать? mongoDB|PG (надо ли проводить иследование как в спринте UGC, какой показатель проверять? не пользовался mongo до курса... есть ли пунктик- показать все чему научили)
- Где хранить информацию о рейтинге Announcement (будет ли оно оцениваться) - продумать

надо выбрать [1] или [2]

### [*] 5. Сценарий Chat

- если ты участник события, появляется возможность общаться в чате

### [*] 6. Сценарий соц.сети

- при регистрации события есть возможность опубликовать пост в своих соц.сетях

## Требования

### Announcement

Использовать access_token для определения user_id и прав доступа к информации

- создать анонс (записать в базу) + оповещение
- изменить анонс (изменить запись в базе по announcement_id) + оповещение
- удалить анонс (удалить/изменить статус записи в базе по announcement_id) + оповещение
- посмотреть анонсы пользователя как организатора (получить записи из базы по user_id) (применить фильтрацию) (пагинация)
- [*] посмотреть анонсы пользователя как гостя (получить записи из базы по user_id) (применить фильтрацию) (пагинация)
- посмотреть актуальные анонсы для фильма (получить записи из базы по movie_id) (применить фильтрацию) (пагинация)
- посмотреть подробную информацию об анонсе (получить запись из базы по announcement_id)
- [?] менять статус анонса по его завершению (изменить запись в базе по announcement_id) + [*]оповещение c Rating
- проверять конфликты анонсов (уже создал свой или подтвердил чужой на это время)

### Booking

- отправить заявку на участие (записать в базу) + оповещение
- подтвердить участие в событии/подтвердить заявку на участии (изменить запись в базе по announcement_id, user_id) + оповещение
- посмотреть статус заявки (получить запись из базы по announcement_id, user_id)
- получить всех участников события (получить записи из базы по announcement_id) (применить фильтрацию) (пагинация)
- запретить отправлять несколько заявок на один анонс

### Rating [?]

- поставить оценку (записать в базу)
- получить оценку (получить записи из базы по announcement_id, user_id)
- изменить оценку (изменить запись в базе по rewiev_id)
- удалить оценку (удалить/изменить запись в базе по rewiev_id)

### [*] Chat

- написать пост
- изменить пост
- удалить пост
- получить посты

### Внешние сервисы

- Auth (user_info, access_token)
- Movie_API (информация о фильме)
- UGC (подписчики, !!хранение отзывов!!) - !ВОПРОС!
- Notification (отправлять уведомления, создавать и модерировать отложенные уведомления)
- Url_shortner (генерировать ссылки на события)

## Модели

### Announcement

#### Поля

- id - announcement_id
- status - ['Created', 'Alive', 'Closed', 'Done'] статус объявления, необходимо для сортировки + [?]нотификация (выбор шаблона для события)
- title - название объявления
- description - описание, условия, цена
- movie_id - uuid фильма
- author_id - uuid автора объявления
- sub_only - флаг приватности, если TRUE: объявление будет показываться только списку подписчиков
- is_free - флаг для фильтрации, если событие платое: FALSE
- ticket_count - количество участников
- event_time - дата события
- event_location - место события
- created - дата создания объявления
- modified - дата последнего изменения объявления

- movie_title - название фильма (для Response)
- author_name - имя автора объявления (для Response)
- guest_list - список гостей с их статусом и [*]рейтингом (для Response)
- author_rating - рейтинг автора объявления (для Response)

#### Layer DB:

- Announcement

- `id`: uuid [pk]
- `status`: AnnouncetStatus
- `title`: str
- `description`: str
- `movie_id`: uuid
- `author_id`: uuid
- `sub_only`: bool
- `is_free`: bool
- `ticket_count`: int
- `event_time`: datetime [unique]
- `event_location`: str
- `created`: datetime
- `modified`: datetime

#### Layer API:

- AnnouncementResponse

- `id`: str | UUID
- `status`: EventStatus
- `title`: str
- `author_id`: str | UUID
- `sub_only`: bool
- `is_free`: bool
- `ticket_count`: int
- `event_time`: datetime
- `event_location`: str

- DetailAnnouncementResponse

- `id`: str | uuid
- `status`: AnnouncetStatus
- `title`: str
- `description`: str
- `movie_title`: str
- `author_name`: str
- `sub_only`: bool
- `is_free`: bool
- `ticket_count`: int
- `event_time`: datetime
- `event_location`: str
- `created`: datetime
- `modified`: datetime
- `guest_list`: list[str]
- `author_rating`: float

### Booking

#### Поля

- id - booking_id
- announcement_id - uuid объявления
- author_id - uuid автора объявления
- guest_id - uuid гостя
- author_status - по дефолту None, если заявка одобрена TRUE, отклонена - FALSE
- guest_status - по дефолту TRUE, если гость передумал FALSE
- event_time - дата события [учавствует в индексе уникальности]
- created - дата создания записи
- modified - дата последнего изменения записи

- movie_title - название фильма (для Response)
- author_name - имя автора объявления (для Response)
- guest_name - имя гостя (для Response)
- author_rating - рейтинг автора объявления (для Response)
- guest_rating - рейтинг гостя (для Response)

#### Layer DB:
\n
- Booking
\n
- `id`: uuid [pk]
- `announcement_id`: uuid [fk Announcement.id]
- `author_id`: uuid [_unique]
- `guest_id`: uuid
- `author_status`: bool
- `guest_status`: bool
- `event_time`: datetime [_unique]
- `created`: datetime
- `modified`: datetime

#### Layer API:

- BookingResponse

- `booking_id`: str | uuid
- `guest_name`: str
- `author_status`: bool
- `guest_status`: bool
- `guest_rating`: float

- DetailBookingResponse

- `booking_id`: str | UUID
- `announcement_id`: str | UUID
- `movie_title`: str
- `author_name`: str
- `guest_name`: str
- `author_status`: bool | None
- `guest_status`: bool
- `guest_rating`: float
- `author_rating`: float
- `event_time`: datetime

## API

### Announcement

- POST /api/v1/announcement/{movie_id} - создание объявления [Response: DetailAnnouncementResponse]
- PUT /api/v1/announcement/{announcement_id} - изменение объявления [Response: DetailAnnouncementResponse]
- GET /api/v1/announcement/{announcement_id} - получить подробную информацию из объявления [Response: DetailAnnouncementResponse]
- GET /api/v1/announcements - получить весь список объявлений по условию [Response: list[AnnouncementResponse]]
- DELETE /api/v1/announcement/{announcement_id} [Response: HTTPStatus.OK]

### Booking

...

## Я.Практика

Не всем нравится сидеть дома и смотреть фильмы в одиночку: иногда хочется их посмотреть с компанией единомышленников.
Для добавления такой возможности реализуйте кнопку покупки билета в кино для определенной группы фильмов. Система должна дать пользователю возможность составлять свои расписания, выбирать фильмы и место сбора. Также она должна показывать возможное количество зрителей и позволять пользователю выбирать дату и время просмотра и хоста — того, кто предлагает фильм и место.
Для данной задачи реализовывать оплату не нужно: достаточно бронировать билеты и не давать забронировать их больше, чем есть мест у конкретного человека.
В качестве задания «со звёздочкой» придумайте систему оценки пользователя-хоста и пользователя-гостя.

## задачи на [22.03.2023 ]

backward

- [Notific] Fix (или писать мок)
- [Notific] Тянуть в проект или docker (если кто-то из нас умеет)
- [Notific] Добавить функционал Event.booking (не в приоритете)
  doc
- [DOC] Требования к Announcement
- [DOC] Требования к Booking
- [DOC] Требования к Rewievs
- [DOC] Требования к сервисам из прошлых спринтов
- [DOC] Модели
- [DOC] Диограма последовательностей
  api
- [MVP] FastAPI показать /api/openapi (Announcement)
  <!-- - [MVP+] FastAPI middleware Logging -->
  <!-- - [MVP+] FastAPI middleware Auth -->
  <!-- - [MVP+] FastAPI docker -->
  <!-- - [MVP+] FastAPI test -->
  db
- [MVP] PG написать StorageProtocol(async)
- [MVP+] PG написать PGStorage(async)
  <!-- - [MVP+] PG написать инициализацию BD(sqlalchemy) -->
  <!-- - [MVP+] PG написать модель Announcement(sqlalchemy) -->
  <!-- - [MVP+] PG написать модель Announcement(pydantic) -->
- [MVP+] PG docker
  reviews
- [Rewievs] Прочитать спринт UGC
- [Rewievs] Написать требования к сервису
- [Rewievs] Выбрать технологию (Mongo/PG)
- [Rewievs] Модели
- [Rewievs] Требования к стороним сервисам
- [Rewievs][mvp] DB написать StorageProtocol(async)
- [Rewievs][mvp] DB написать DBStorage(async)
