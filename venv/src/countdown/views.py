from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
import datetime
from django.conf import settings
from countdown.models import Countdown, Message
from django.db.utils import IntegrityError
# Create your views here.
def countdown_view(request):
    return render(request, 'countdown.html')

def get_target_date(request):
    # Retrieve the target date from the database
    target = get_object_or_404(Countdown, id=2)

    # Return the target date as a JSON response
    return JsonResponse({'target_date': target.target_date})

def add_time(request, number, time_indicator, target_id=None):
    # Convert the number to an integer
    try:
        number = int(number)
    except ValueError:
        return JsonResponse({'error': 'Invalid number'}, status=400)

    # Define a dictionary to map time indicators to seconds
    time_mapping = {
        's': 1,  # seconds
        'm': 60,  # minutes
        'h': 3600,  # hours
    }

    # Check if the time indicator is valid
    if time_indicator not in time_mapping:
        return JsonResponse({'error': 'Invalid time indicator'}, status=400)

    # Calculate the added time in seconds
    added_time_seconds = number * time_mapping[time_indicator]

    try:
        # Retrieve the target date for id=2
        target = Countdown.objects.get(id=2)

        # Update the target date by adding the specified time
        target.target_date += datetime.timedelta(seconds=added_time_seconds)

        # Save the updated target date
        target.save()

        return JsonResponse({'message': f'Added {number}{time_indicator} to the time'})
    except Countdown.DoesNotExist:
        return JsonResponse({'error': 'Target with id=2 not found'}, status=404)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def remove_time(request, number, time_indicator, target_id=None):
    # Convert the number to an integer
    try:
        number = int(number)
    except ValueError:
        return JsonResponse({'error': 'Invalid number'}, status=400)

    # Define a dictionary to map time indicators to seconds
    time_mapping = {
        's': 1,  # seconds
        'm': 60,  # minutes
        'h': 3600,  # hours
    }

    # Check if the time indicator is valid
    if time_indicator not in time_mapping:
        return JsonResponse({'error': 'Invalid time indicator'}, status=400)

    # Calculate the removed time in seconds
    removed_time_seconds = number * time_mapping[time_indicator]

    try:
        # Retrieve the target date for id=2
        target = Countdown.objects.get(id=2)

        # Update the target date by subtracting the specified time
        target.target_date -= datetime.timedelta(seconds=removed_time_seconds)

        # Save the updated target date
        target.save()

        return JsonResponse({'message': f'Removed {number}{time_indicator} from the time'})
    except Countdown.DoesNotExist:
        return JsonResponse({'error': 'Target with id=2 not found'}, status=404)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=400)
def reset_target_date(request):
    try:
        # Get the existing target date record or create a new one if it doesn't exist
        target, created = Countdown.objects.get_or_create(id=2)

        # Update the target date for October 28th 2023 at 23:00:00
        target.target_date = datetime.datetime(2023, 10, 28, 23, 0, 0)
        target.save()

        return JsonResponse({'message': f'Reset target date to {target.target_date}'})
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=400)

def show_message(request, message_id):
    # api endpoint meaning
    # 0 = nothing
    # 1 = add_time
    # 2 = remove_time
    # 3 = reset_target_date
    
    # This function is used to render the templates/message.html template with the specified message id from . If there is an api_param,
    # the specified function is called before the page is displayed.
    # Retrieve the message from the database
    message = get_object_or_404(Message, id=message_id)
    api_endpoint = message.api_endpoint_id
    api_param_nb = message.api_param_nb
    been_seen = message.been_seen
    print("Fetched message[" + str(message_id) + "] from database: " + str(message))
    # if a message has been seen, show message id 0. However, if it removes time, the time still gets removed. If it adds time, time does not get added again.
    print("Message id is " + str(message_id))
    if str(message_id) == "2":
        print("Message id 2 detected.")
        return render(request, 'message.html', {'message': message.message})
    if been_seen == True:
        message = get_object_or_404(Message, id=1)
        if api_endpoint == 2:
            remove_time(request, api_param_nb, 's')
        return render(request, 'message.html', {'message': message.message})
    else:
        # Mark the message as seen
        message.been_seen = True
        message.save()
        print("Marked message[" + str(message_id) + "] as seen: " + str(message))
        if api_endpoint == 1:
            add_time(request, api_param_nb, 's')
            print("Added " + str(api_param_nb) + " seconds to the target date.")
        elif api_endpoint == 2:
            remove_time(request, api_param_nb, 's')
            print("Removed " + str(api_param_nb) + " seconds from the target date.")
        elif api_endpoint == 3:
            reset_target_date(request)
            print("Reset the target date.")
        return render(request, 'message.html', {'message': message.message})


