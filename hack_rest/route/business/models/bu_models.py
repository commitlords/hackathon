from flask_restx import Model, fields

BU_INTEREST_MODEL = Model(
    "Business",
    {
        "name": fields.String(
            "name",
            description="business interest name",
            example="some business",
            required=True,
        )
    },
)
