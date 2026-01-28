from tortoise import fields, models

class Admin(models.Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
    username = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "bot_admins"

class BotSetting(models.Model):
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=255, unique=True)
    value = fields.TextField()

    class Meta:
        table = "bot_settings"

    @classmethod
    async def get_val(cls, key, default=None):
        setting = await cls.get_or_none(key=key)
        return setting.value if setting else default

    @classmethod
    async def set_val(cls, key, value):
        await cls.update_or_create(key=key, defaults={"value": str(value)})
