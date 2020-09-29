from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse  # Used to generate urls by reversing the URL patterns
from django.db.models.signals import post_save
from twilio.rest import Client

#relation containg all genre of books
class Genre(models.Model):
    genre = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    class Meta:
        ordering = ('-genre',)

    def __str__(self):
        return self.name
##  __str__ method is used to override default string returnd by an object


##relation containing language of books
class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.name


#book relation that has 2 foreign key author language
#book relation can contain multiple genre so we have used manytomanyfield
class Book(models.Model):
    #objects = None
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField('author', max_length=100, null=True, blank=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    total_copies = models.IntegerField(null=True, blank=True)
    available_copies = models.IntegerField(null=True, blank=True)
    pic = models.ImageField(blank=True, null=True, upload_to='book_image')

    # return canonical url for an object
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    ##  _str_ method is used to override default string returnd by an object
    def _str_(self):
        return self.title

class sms(models.Model):
    result= models.PositiveIntegerField()

    def _str_(self):
        return str(self.result)

    def save(self,*args, **kwargs):
        if self.result < 70:
            account_sid = 'AC1711a06bbde293f359ef995639a8202a'
            auth_token = 'dab191dcd7ce8d11b19015cb214f0973'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f'The Number of books borrowed - {self.result}',
                from_='+19092595003',
                to='+918446896642'
            )

            print(message.sid)
        return super(sms, self).save(*args,*kwargs)


def create_user(sender, *args, **kwargs):
    if kwargs['created']:
        user = User.objects.create(username=kwargs['instance'], password="dummypass")



#relation containing info about students
#roll_no is used for identifing students uniquely
class Student(models.Model):
    roll_no = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=10)
    branch = models.CharField(max_length=3)
    contact_no = models.CharField(max_length=10)
    total_books_due=models.IntegerField(default=0)
    email=models.EmailField(unique=True)
    pic=models.ImageField(blank=True, upload_to='profile_image')
    def __str__(self):
        return str(self.roll_no)


post_save.connect(create_user, sender=Student)
#relation containing info about Borrowed books
#it has  foriegn key book and student for refrencing book nad student
#roll_no is used for identifing students
#if a book is returned than corresponding tuple is deleted from database
class Borrower(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    issue_date = models.DateTimeField(null=True,blank=True)
    return_date = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.student.name+" borrowed "+self.book.title




class Reviews(models.Model):
    review=models.CharField(max_length=100,default="none")
    book=models.ForeignKey('Book',on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    CHOICES = (
        ('0', '0'),
        ('.5', '.5'),
        ('1', '1'),
        ('1.5', '1.5'),
        ('2', '2'),
        ('2.5', '2.5'),
        ('3', '3'),
        ('3.5', '3.5'),
        ('4', '4'),
        ('4.5', '4.5'),
        ('5', '5'),
    )

    rating=models.CharField(max_length=3, choices=CHOICES, default='2')
