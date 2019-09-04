from twilio.rest import Client
import requests
from time import sleep

#start of program for one plant
def plant_program():
    from shamrock import Shamrock
    api = Shamrock('R09xeis2ZEROWFpvcFo5VVhNV0NSUT09')

    # input plant identifier
    identifier=input('How would you like to identify this plant?')
    type=input('Do you know the species? (y/n)')
    if type == 'y':
        species=input('What is the common name of your plant?')
        species_data = api.species(common_name=species)
        for i in range(len(species_data)):
            x = species_data[i]
            if x['is_main_species'] == True:
                SD_URL = x['link'] + '?token=R09xeis2ZEROWFpvcFo5VVhNV0NSUT09'
                data = requests.get(SD_URL)
                SD = data.json()
                life = SD['main_species']['specifications']['lifespan']
                if life == "Short":
                    lifespan = 100 * 12 * 4 * 7 * 24 * 60 * 60
                elif life == "Moderate":
                    lifespan = 250 * 12 * 4 * 7 * 24 * 60 * 60
                else:
                    timeline = int(input('The lifespan information either does not exist, or is longer than 250 years. '
                                         'How long do you want to receive reminders for? (Please convert to months)'))
                    lifespan = timeline * 4 * 7 * 24 * 60 * 60

                precip_min = str(SD['main_species']['growth']['precipitation_minimum']['inches'])
                precip_max = str(SD['main_species']['growth']['precipitation_maximum']['inches'])

                if precip_min == 'None' or precip_max == 'None':
                    size = input('There is no watering data so lets add some. Is your plant a large or small? (l/s)')
                    if size == 's':
                        repeat = int(input('How frequently do you want to receive a reminder to water your plant 2oz of water? (Please convert to days)'))
                        _message = 'This is a reminder to water your plant ' + identifier + ' with 2oz of water'
                    else:
                        repeat = int(input('How frequently do you want to receive a reminder to water your plant 8oz of water? (Please convert to days)'))
                        _message = 'This is a reminder to water your plant ' + identifier + ' with 8oz of water'
                else:
                    av_Inrain_perday = ((float(precip_max) + float(precip_min)) / 2) / 365
                    density_max = SD['main_species']['growth']['planting_density_maximum']['sqm']
                    density_min = SD['main_species']['growth']['planting_density_minimum']['sqm']
                    av_plants_per_sqrIn = ((density_max + density_min) / 2) / 43560 / 144
                    water_vol_per_day = av_Inrain_perday / av_plants_per_sqrIn
                    days_oz = int(8 / (water_vol_per_day / 14.4375))  # days per oz of water
                    if days_oz >= 3:
                        _message = 'This is a reminder to water your plant ' + identifier + ' with 2oz of water'
                        repeat = days_oz * 2
                    else:
                        _message = 'This is a reminder to water your plant ' + identifier + ' with 8oz of water'
                        repeat = days_oz * 8
            else:
                print('')
        repeating_alerts(lifespan, repeat, _message)

    elif type == 'n':
        size = input('Let us input some requirements then. Is your plant a large or small? (l/s)')
        if size == 's':
            repeat = int(input('How frequently do you want to receive a reminder to water your plant 2oz of water? (Please convert to days)'))
            _message = 'This is a reminder to water your plant ' + identifier + ' with 2oz of water'
        else:
            repeat = int(input('How frequently do you want to receive a reminder to water your plant 8oz of water? (Please convert to days)'))
            _message = 'This is a reminder to water your plant ' + identifier + ' with 8oz of water'
        timeline = int(input('How long do you want to receive reminders for? (Please convert to months)'))
        lifespan = timeline * 4 * 7 * 24 * 60 * 60
        repeating_alerts(lifespan, repeat, _message)
    return

def repeating_alerts(lifespan, repeat, _message):
    print('Your first reminder will be sent in ' + str(repeat) + ' days')
    for num in range(lifespan):
        Val = num % repeat
        while Val == 0:
            # seconds in a day
            sleep_length = repeat * 24 * 60 * 60
            sleep(sleep_length)
            Val = 1
            message = twilio_client.messages.create(
                to=number,
                from_="+15307231680",
                body=_message)
            print('Your Reminder has been sent')
    return

start = input('Would you like a plant care reminder? (y/n)')
if start == 'y':
    #input twilio data
    account_sid = 'ACdb128d27412d67933700c209a5fcef63'
    auth_token = 'ca5c28abd9d263ee112b079f9b39e19c'
    number = input('What phone number do you want to receive reminders on? (Format: +1XXXXXXXXXX)')
    twilio_client = Client(account_sid, auth_token)
    plant_program()

else:
    print('Thank you and come again!')










