from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from utils.core.base_models import BaseModel
from safedelete.managers import SafeDeleteManager
from utils.core.validation import nepal_phone_number_validator


class CustomBaseUserManager(BaseUserManager, SafeDeleteManager):
    """
    Custom user manager that handles user creation and inherits SafeDeleteManager
    """

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a regular user with the given username and password.
        """
        if not username:
            raise ValueError("The Username field must be set")

        # Normalize email if provided
        if email:
            email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a superuser with the given username and password.
        """
        extra_fields.setdefault("role", self.model.Roles.SUPER)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, BaseModel):
    """
    Custom User model using AbstractBaseUser.
    Only includes essential fields and custom role-based permissions.
    """

    class Roles(models.IntegerChoices):
        SUPER = 1, "Super"
        ADMIN = 2, "Admin"
        GENERAL = 3, "General"
        WHISTLE_BLOWER = 4, "Whistle Blower"
        FACT_CHECKER = 5, "Fact Checker"

    username_validator = UnicodeUsernameValidator()

    # Core user fields
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        unique=True,
        validators=[username_validator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
    )

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    email = models.EmailField(_("email address"), blank=True)

    phone_number = models.CharField(
        max_length=15, validators=[nepal_phone_number_validator], blank=True, default=""
    )

    # Status fields (is_active and password, last_login are inherited from AbstractBaseUser, but redefined here anyway)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    password = models.CharField(_("password"), max_length=128)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    role = models.CharField(max_length=20, default=Roles.GENERAL, choices=Roles.choices)

    # Timestamps
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    # Password reset fields (optional but gives you more control)
    password_reset_token = models.CharField(max_length=255, blank=True, default="")
    password_reset_token_created_at = models.DateTimeField(null=True, blank=True)

    # Authentication configuration
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email"
    ]  # Fields required when creating superuser via createsuperuser command

    # Custom manager
    objects = CustomBaseUserManager()

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(deleted=None),
                name="user_unique_email_safedelete",
            ),
            models.UniqueConstraint(
                fields=["phone_number"],
                condition=models.Q(deleted=None),
                name="user_unique_phone_number_safedelete",
            ),
        ]

    def delete(self, force_policy=None, **kwargs):
        """
        It is overridden to add a timestamp to the username. This is done because username is a field which is used to login to the system. Django needs it to be unique using the unique=True param. But when a user is soft-deleted, it is still present in database and any new users trying to use the username of the soft-deleted user will not be able to have it because of the unique constraint, hence a timestamp is added to the username when soft-deleting.
        """
        self.username = f"{self.username}_{timezone.now()}"
        self.save()
        return super().delete(force_policy, **kwargs)

    # def delete(self, force_policy=None, **kwargs):
    #     return super().delete(force_policy, **kwargs)

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name

    def clean(self):
        super().clean()

    @property
    def is_super_user(self):
        """Check if user has super role"""
        return self.role == self.Roles.SUPER

    @property
    def is_admin_user(self):
        """Check if user has admin role"""
        return self.role == self.Roles.ADMIN

    @property
    def is_general_user(self):
        """Check if user has general role"""
        return self.role == self.Roles.GENERAL

    @property
    def is_whistle_blower_user(self):
        """Check if user has whistle blower role"""
        return self.role == self.Roles.WHISTLE_BLOWER

    @property
    def is_fact_checker_user(self):
        """Check if user has fact checker role"""
        return self.role == self.Roles.FACT_CHECKER

    # You can implement your own permission methods here
    def has_admin_access(self):
        """Check if user can access admin interface"""
        return self.is_active and self.role in [self.Roles.SUPER, self.Roles.ADMIN]

    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.is_active and self.role == self.Roles.SUPER

    # Optional: Django admin compatibility properties
    @property
    def is_staff(self):
        """Property for Django admin compatibility"""
        return self.has_admin_access()

    @property
    def is_superuser(self):
        """Property for Django admin compatibility"""
        return self.is_active and self.role == self.Roles.SUPER
