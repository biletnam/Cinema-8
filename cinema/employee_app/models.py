from django.db import models

# Create your models here.

class Client(models.Model):
	name = models.CharField(max_length=20)
	surname = models.CharField(max_length=30)
	phone = models.PositiveIntegerField()
	email = models.EmailField()

	def __unicode__(self):
		return self.name + " " + self.surname

class Movie(models.Model):
	title = models.CharField(max_length=100, unique=True)
	length = models.PositiveSmallIntegerField()
	minimal_age = models.PositiveSmallIntegerField(default=0)
	genre = models.CharField(max_length=30, blank=True, null=True)

	def __unicode__(self):
		return self.title

class Room(models.Model):
	room_number = models.PositiveSmallIntegerField(primary_key=True)
	seats_number = models.PositiveSmallIntegerField()
	status = models.CharField(max_length=20, choices=(('Closed', 'Closed'), ('Open', 'Open')), default='Open')

	def __unicode__(self):
		return "room " + str(self.room_number)

class Projection(models.Model): #chack na dacie czy jest > now
	movie = models.ForeignKey(Movie)
	room = models.ForeignKey(Room)
	date_time = models.DateTimeField()
	audio_language = models.CharField(max_length=15, blank=True, null=True)
	subtitles_language = models.CharField(max_length=15, blank=True, null=True)
	ticket_price = models.PositiveSmallIntegerField()

	class Meta:
		unique_together = ("movie", "room", "date_time",)

	def __unicode__(self):
		return str(self.movie) + " - " + str(self.room) + " - " + str(self.date_time)

class Reservation(models.Model):
	seat_number = models.PositiveSmallIntegerField()
	client = models.ForeignKey(Client)
	projection = models.ForeignKey(Projection)
	received = models.BooleanField(default=False)

	class Meta:
		unique_together = ("seat_number", "projection",)

	def __unicode__(self):
		return "Name: " + str(self.client) + ", Seat: " + str(self.seat_number) + ", Projection: " + str(self.projection)

