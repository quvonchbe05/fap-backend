from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    Attributes:
        DEBUG (bool): Flag to enable or disable debug mode. Default is True.
        POSTGRES_HOST (str): The hostname for the PostgreSQL database.
        POSTGRES_PORT (int): The port number for the PostgreSQL database.
        POSTGRES_USER (str): The username for the PostgreSQL database.
        POSTGRES_PASSWORD (str): The password for the PostgreSQL database.
        POSTGRES_DB (str): The database name for the PostgreSQL database.

    Properties:
        DATABASE_URL (str): The complete database URL for connecting to the PostgreSQL database.

    Config:
        model_config (SettingsConfigDict): Configuration for loading settings from an environment file.
    """

    DEBUG: bool = False

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self) -> str:
        """
        Construct the database URL for PostgreSQL.

        Returns:
            str: The database URL in the format "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
