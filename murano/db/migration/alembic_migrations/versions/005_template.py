# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Change type of description field in package table.

Revision ID: 004
Revises: table package

"""

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'

from alembic import op

import sqlalchemy as sa


MYSQL_ENGINE = 'InnoDB'
MYSQL_CHARSET = 'utf8'


def upgrade():
    op.create_table(
        'template',
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('updated', sa.DateTime(), nullable=False),
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('tenant_id', sa.String(length=36), nullable=False),
        sa.Column('version', sa.BigInteger(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('networking', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'name'),
        mysql_engine=MYSQL_ENGINE,
        mysql_charset=MYSQL_CHARSET
    )
    ### end Alembic commands ###


def downgrade():
    op.drop_table('environment')

    ### end Alembic commands ###
