from sqlalchemy import MetaData, Table, Column, UniqueConstraint, CheckConstraint, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, DECIMAL, TINYINT, TEXT, TIME, DATE, ENUM, VARCHAR, NCHAR, BOOLEAN

metadata = MetaData()

Recipe = Table(
    'Recipe',
    metadata,
    Column("recipe_ID", INTEGER(unsigned=True), primary_key=True),
    Column("name", VARCHAR(length=100), nullable=False),
    Column("photo", VARCHAR(length=50), nullable=False),
    Column("servings_cout", TINYINT(unsigned=True), nullable=False),
    Column("cook_time", TIME(), nullable=False),
    Column("rating", INTEGER(unsigned=False), nullable=False),
    Column("recommend", TEXT(), nullable=True),
    Column("author", INTEGER(unsigned=True), ForeignKey("user.id", ondelete="SET DEFAULT"), nullable=False),
    UniqueConstraint("name"),
    UniqueConstraint("photo"),
    CheckConstraint('servings_cout>0'), )

Ingredient = Table(
    'Ingredient',
    metadata,
    Column("ingredient_ID", INTEGER(unsigned=True), primary_key=True),
    Column("name", VARCHAR(length=50), nullable=False),
    Column("unit_ID", INTEGER(unsigned=True), ForeignKey("Unit.unit_ID", ondelete="RESTRICT"), nullable=False),
    Column("kkal", DECIMAL(precision=6, scale=2), nullable=False),
    Column("belki", DECIMAL(precision=6, scale=2), nullable=False),
    Column("zhiry", DECIMAL(precision=6, scale=2), nullable=False),
    Column("uglevody", DECIMAL(precision=6, scale=2), nullable=False),
    UniqueConstraint("name"), )

Step = Table(
    'Step',
    metadata,
    Column("step_ID", INTEGER(unsigned=True), primary_key=True),
    Column("description", TEXT(), nullable=False),
    Column("timer", TIME(), nullable=True, default=None),
    Column("media", VARCHAR(length=20), nullable=True),
    Column("recipe_ID", INTEGER(unsigned=True), ForeignKey("Recipe.recipe_ID", ondelete="CASCADE"), nullable=False),
    UniqueConstraint("media"), )

Tag = Table(
    'Tag',
    metadata,
    Column("tag_ID", INTEGER(unsigned=True), primary_key=True),
    Column("name", VARCHAR(length=20), nullable=False),
    UniqueConstraint("name"),
)

User = Table(
    'user',
    metadata,
    Column("id", INTEGER(unsigned=True), primary_key=True),
    Column("login", VARCHAR(length=50), nullable=False, unique=True),
    Column("hashed_password", TEXT(), nullable=False),
    Column("photo", VARCHAR(length=20)),
    Column("name", VARCHAR(length=40)),
    Column("s_name", VARCHAR(length=40)),
    Column("b_day", DATE()),
    Column("gender", ENUM("М", "Ж")),
    Column("is_active", BOOLEAN(), default=True, nullable=False),
    Column("is_superuser", BOOLEAN(), default=False, nullable=False),
    Column("is_verified", BOOLEAN(), default=False, nullable=False),
)

Unit = Table(
    'Unit',
    metadata,
    Column("unit_ID", INTEGER(unsigned=True), primary_key=True),
    Column("name", VARCHAR(length=20), nullable=False),
    UniqueConstraint("name"),
)
Recipe_ingredient = Table(
    'Recipe_ingredient',
    metadata,
    Column("recipe_ID_ingredient", INTEGER(unsigned=True), primary_key=True),
    Column("recipe_ID", INTEGER(unsigned=True), ForeignKey("Recipe.recipe_ID", ondelete="CASCADE"), nullable=False),
    Column("ingredient_ID", INTEGER(unsigned=True), ForeignKey("Ingredient.ingredient_ID", ondelete="CASCADE"),
           nullable=False),
    Column("count", DECIMAL(precision=5, scale=2), nullable=False),
    CheckConstraint("count>0"),
)
Recipe_tag = Table(
    'Recipe_tag',
    metadata,
    Column("recipe_ID_tag", INTEGER(unsigned=True), primary_key=True),
    Column("recipe_ID", INTEGER(unsigned=True), ForeignKey("Recipe.recipe_ID", ondelete="CASCADE"), nullable=False),
    Column("tag_ID", INTEGER(unsigned=True), ForeignKey("Tag.tag_ID", ondelete="CASCADE"), nullable=False),
)

Favourite_recipe = Table(
    'Favourite_recipe',
    metadata,
    Column("favourite_ID", INTEGER(unsigned=True), primary_key=True),
    Column("recipe_ID", INTEGER(unsigned=True), ForeignKey("Recipe.recipe_ID", ondelete="CASCADE"), nullable=False),
    Column("user_ID", INTEGER(unsigned=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
)
Score_recipe = Table(
    'Score_recipe',
    metadata,
    Column("Score_ID", INTEGER(unsigned=True), primary_key=True),
    Column("recipe_ID", INTEGER(unsigned=True), ForeignKey("Recipe.recipe_ID", ondelete="CASCADE"), nullable=False),
    Column("user_ID", INTEGER(unsigned=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("score", TINYINT(), nullable=False, ),
)
