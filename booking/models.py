from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

#Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None):
        #create and save a User with the given email and password
        if not email:
            raise ValueError("User must have a email address ")
        user = self.model(
            email=self.normalize_email(email),
            name = name 
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_manageruser(self, name, email, password):
        #create and save a staff user with the given email and password
        user = self.create_user(email, name=name, password=password,)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        # create and save a superuser with the given email and password
        user = self.create_user(
            email, 
            name=name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True),
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user, non super-user
    admin = models.BooleanField(default=False) # a superuser 


# notice the absence of a password field are required by default

    def get_full_name(self):
        return self.name
    def get_short_name(self):
        return self.email
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the User have a specific permission"
        return True
    def has_module_perm(self, app_label):
        "Does the user have permission to view the app 'app_label'"
        #simple posible answer is : yes Always
        return True


    @property
    def is_staff(self):
        "is the user is staff"
        return self.staff
    
    @property
    def is_admin(self):
        "is the user is a user ?"
        return self.admin
    objects =UserManager()


class Room(models.Model):
    name = models.CharField(max_length=30)
    advance_booking= models.IntegerField()
    booked = models.BooleanField(default=True)

    USERNAME_FIELD = 'name'

    class Meta:
        ordering=['name']

    def __str__(self):
        return self.room.name

class TimeSlot(models.Model):
    check_in_time = models.TimeField(max_length=4)
    check_out_time = models.TimeField(max_length=4)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booked = models.BooleanField(default=True)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    date = models.DateField()
