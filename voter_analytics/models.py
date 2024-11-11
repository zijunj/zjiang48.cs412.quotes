from django.db import models

# Create your models here.

class Voter(models.Model):
    '''
     Store/represent the data for a registered voter  in the town of Newton, MA.
*    Last Name
*    First Name
*    Residential Address - Street Number
*    Residential Address - Street Name
*    Residential Address - Apartment Number
*    Residential Address - Zip Code
*    Date of Birth
*    Date of Registration
*    Party Affiliation
*    Precinct Number
*    v20state
*    v21town
*    v21primary
*    v22general
*    v23town
*    voter_score
    '''
    # identification
    last_name = models.TextField()
    first_name = models.TextField()
    # Residential Address
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.IntegerField()
    # voter information
    dob = models.DateField(max_length=8)
    date_of_registration = models.DateField(max_length=8)
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.TextField()
    # recent elections participation
    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}, party affilation: {self.party_affiliation}, voter score = {self.voter_score}'
    
        
        
def load_data():
    '''Load data records from a CSV file into model instances.'''

    # delete all records: clear out the database:
    Voter.objects.all().delete()
    
    # open the file for reading:
    filename = r'C:\Users\Victor\django\django-projects\newton_voters.csv'
    f = open(filename)
    headers = f.readline() # read/discard the headers
    
    # loop to read all the lines in the file
    for line in f:
        
        # provide protection around code that might generate an exception
            fields = line.split(',') # create a list of fields
            
            # create a new instance of Result object with this record from CSV
            voter = Voter(
                            last_name = fields[1],
                            first_name = fields[2],
                            street_number = fields[3],
                            street_name = fields[4],
                            apartment_number = fields[5],
                            zip_code = fields[6],
                            dob = fields[7],
                            date_of_registration = fields[8],
                            party_affiliation = fields[9].strip(),
                            precinct_number = fields[10],
                            v20state = fields[11],
                            v21town = fields[12],
                            v21primary = fields[13],
                            v22general = fields[14],
                            v23town = fields[15],
                            voter_score = fields[16],
                        )
            voter.save() # save this instance to the database.
            
      