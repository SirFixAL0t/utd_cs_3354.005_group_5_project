from pydantic import BaseModel, ConfigDict

class SettingsBase(BaseModel):
    theme: str
    timezone: str

class SettingsCreate(SettingsBase):
    pass

class Settings(SettingsBase):
    settings_id: str
    user_id: str
    model_config = ConfigDict(from_attributes=True)
