from sqlalchemy import MetaData, Table, Column, UniqueConstraint, CheckConstraint
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
    Column("author", INTEGER(unsigned=True), nullable=False, foreign_key="User.user_ID"),
    UniqueConstraint("name"),
    UniqueConstraint("photo"),
    CheckConstraint('servings_cout>0'), )

Ingredient = Table(
    'Ingredient',
    metadata,
    Column("ingredient_ID", INTEGER(unsigned=True), primary_key=True),
    Column("name", VARCHAR(length=50), nullable=False),
    Column("kkal", DECIMAL(unsigned=True, precision=6, scale=2), nullable=False),
    Column("belki", DECIMAL(unsigned=True, precision=6, scale=2), nullable=False),
    Column("zhiry", DECIMAL(unsigned=True, precision=6, scale=2), nullable=False),
    Column("uglevody", DECIMAL(unsigned=True, precision=6, scale=2), nullable=False),
    UniqueConstraint("name"), )

Step = Table(
    'Step',
    metadata,
    Column("step_ID", INTEGER(unsigned=True), primary_key=True),
    Column("description", TEXT(), nullable=False),
    Column("timer", TIME(), nullable=True, default=None),
    Column("media", VARCHAR(length=20), nullable=True),
    Column("recipe_ID", INTEGER(unsigned=True), foreign_key="Recipe.recipe_ID", nullable=False),
    UniqueConstraint("media"), )

Tag = Table(
    'Tag',
    metadata,
    Column("tag_ID", INTEGER(unsigned=True), primary_key=True),
    Column("name", VARCHAR(length=20), nullable=False),
    UniqueConstraint("name"),
)

User = Table(
    'User',
    metadata,
    Column("user_ID", INTEGER(unsigned=True), primary_key=True),
    Column("login", VARCHAR(length=50), nullable=False),
    Column("hashed_password", NCHAR(length=1024), nullable=False),
    Column("photo", VARCHAR(length=20), nullable=False),
    Column("name", VARCHAR(length=40), nullable=False),
    Column("s_name", VARCHAR(length=40), nullable=False),
    Column("b_day", DATE(), nullable=False),
    Column("gender", ENUM("М", "Ж"), nullable=False),
    Column("email", VARCHAR(length=250), nullable=False),
    Column("is_active", BOOLEAN(), nullable=False),
    Column("is_superuser", BOOLEAN(), nullable=False),
    Column("is_verified", BOOLEAN(), nullable=False),
    UniqueConstraint("login", "email"),
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
    Column("recipe_ID", INTEGER(unsigned=True), nullable=False, foreign_key="Recipe.recipe_ID"),
    Column("ingredient_ID", INTEGER(unsigned=True), nullable=False, foreign_key="Ingredient.ingredient_ID"),
    Column("count", DECIMAL(unsigned=True), nullable=False),
    Column("unit_ID", INTEGER(unsigned=True), nullable=False, foreign_key="Unit.unit_ID"),
    CheckConstraint("count>0"),
)
Recipe_tag = Table(
    'Recipe_tag',
    metadata,
    Column("recipe_ID_tag", INTEGER(unsigned=True), primary_key=True),
    Column("recipe_ID", INTEGER(unsigned=True), nullable=False, foreign_key="Recipe.recipe_ID"),
    Column("tag_ID", INTEGER(unsigned=True), nullable=False, foreign_key="Tag.tag_ID"),
)

Favourite_recipe = Table(
    'Favourite_recipe',
    metadata,
    Column("favourite_ID", INTEGER(unsigned=True), primary_key=True),
    Column("recipe_ID", INTEGER(unsigned=True), nullable=False, foreign_key="Recipe.recipe_ID"),
    Column("user_ID", INTEGER(unsigned=True), nullable=False, foreign_key="User.user_ID"),
)
Score_recipe = Table(
    'Score_recipe',
    metadata,
    Column("Score_ID", INTEGER(unsigned=True), primary_key=True),
    Column("recipe_ID", INTEGER(unsigned=True), nullable=False, foreign_key="Recipe.recipe_ID"),
    Column("user_ID", INTEGER(unsigned=True), nullable=False, foreign_key="User.user_ID"),
    Column("score", TINYINT(), nullable=False, ),
)
