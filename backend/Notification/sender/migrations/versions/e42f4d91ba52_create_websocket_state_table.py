"""create websocket state table

Revision ID: e42f4d91ba52
Revises:
Create Date: 2023-03-16 11:14:21.897178

"""
import sqlalchemy as sa
from alembic import op

TEXT_FIELD_LEN = 255

# revision identifiers, used by Alembic.
revision = 'e42f4d91ba52'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'websocket_notifications',
        sa.Column('id', sa.String(TEXT_FIELD_LEN), primary_key=True),
        sa.Column('user_id', sa.String(TEXT_FIELD_LEN)),
        sa.Column('ws_body', sa.String(TEXT_FIELD_LEN)),
        sa.Column('subject', sa.String(TEXT_FIELD_LEN)),
    )


def downgrade() -> None:
    op.drop_table('websocket_notifications')
