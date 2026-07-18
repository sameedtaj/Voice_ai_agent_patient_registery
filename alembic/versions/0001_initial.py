"""Initial patient and call-session tables."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "patients",
        sa.Column("patient_id", sa.Uuid(), nullable=False),
        sa.Column("first_name", sa.String(50), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("sex", sa.Enum("male", "female", "other", "decline", name="sex", native_enum=False), nullable=False),
        sa.Column("phone_number", sa.String(10), nullable=False),
        sa.Column("email", sa.String(254)),
        sa.Column("address_line_1", sa.String(200), nullable=False),
        sa.Column("address_line_2", sa.String(100)),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("state", sa.String(2), nullable=False),
        sa.Column("zip_code", sa.String(10), nullable=False),
        sa.Column("insurance_provider", sa.String(100)),
        sa.Column("insurance_member_id", sa.String(100)),
        sa.Column("preferred_language", sa.String(50), nullable=False),
        sa.Column("emergency_contact_name", sa.String(100)),
        sa.Column("emergency_contact_phone", sa.String(10)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint("patient_id"),
    )
    op.create_index("ix_patients_last_name", "patients", ["last_name"])
    op.create_index("ix_patients_date_of_birth", "patients", ["date_of_birth"])
    op.create_index("ix_patients_phone_number", "patients", ["phone_number"])
    op.create_index("ix_patients_phone_active", "patients", ["phone_number", "deleted_at"])
    op.create_table(
        "call_sessions",
        sa.Column("call_id", sa.String(100), nullable=False),
        sa.Column("patient_id", sa.Uuid()),
        sa.Column("caller_phone", sa.String(30)),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("transcript", sa.Text()),
        sa.Column("collected_payload", sa.Text()),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True)),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.patient_id"]),
        sa.PrimaryKeyConstraint("call_id"),
    )


def downgrade() -> None:
    op.drop_table("call_sessions")
    op.drop_index("ix_patients_phone_active", table_name="patients")
    op.drop_index("ix_patients_phone_number", table_name="patients")
    op.drop_index("ix_patients_date_of_birth", table_name="patients")
    op.drop_index("ix_patients_last_name", table_name="patients")
    op.drop_table("patients")
