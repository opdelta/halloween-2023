from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
import datetime
import math
from django.conf import settings
from countdown.models import Countdown, Message
from django.db.utils import IntegrityError
from django.utils import timezone
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
        target.stopped = False
        target.last_update = ""  # Set last_update to an empty string
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
    # The real message_id is the square root of the message_id + 11. If the result is not an integer, take the floor of the result.
    try:
        real_message_id = str(math.floor(math.sqrt(int(message_id) - 11)))
        # For each <br> tag in the message, replace it with a newline character
    except ValueError:
        message = get_object_or_404(Message, id=1)
        message_text = message.message + " Votre tentative a soulevé une alarme et le compte à rebours a été réduit de 10m."
        # TODO: Remove 10 minutes...
        remove_time(request, 10, 'm')
        return render(request, 'message.html', {'message': message_text})
    print("Message ID: " + str(real_message_id))
    # This function is used to render the templates/message.html template with the specified message id from . If there is an api_param,
    # the specified function is called before the page is displayed.
    
    try:
        message = Message.objects.get(id=real_message_id)
        # for each <br> tag in the message, replace it with an actual br tag
        message_text = message.message.replace('<br>', '<br/>')
    except Message.DoesNotExist:
        message = get_object_or_404(Message, id=1)
        message_text = message.message + "Votre tentative a soulevé une alarme. Le compte à rebours a été réduit de 10m."
        remove_time(request, 10, 'm')
        return render(request, 'message.html', {'message': message_text})
    
    api_endpoint = message.api_endpoint_id
    api_param_nb = message.api_param_nb
    been_seen = message.been_seen
    print("Fetched message[" + str(real_message_id) + "] from database: " + str(message))
    # if a message has been seen, show message id 0. However, if it removes time, the time still gets removed. If it adds time, time does not get added again.
    print("Message id is " + str(real_message_id))
    
    if str(real_message_id) == "2":
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
        print("Marked message[" + str(real_message_id) + "] as seen: " + str(message))
        if api_endpoint == 1:
            add_time(request, api_param_nb, 's')
            print("Added " + str(api_param_nb) + " seconds to the target date.")
        elif api_endpoint == 2:
            remove_time(request, api_param_nb, 's')
            print("Removed " + str(api_param_nb) + " seconds from the target date.")
        elif api_endpoint == 3:
            reset_target_date(request)
            print("Reset the target date.")
        return render(request, 'message.html', {'message': message_text})

def stop(request):
    try:
        # Get the existing target date record or create a new one if it doesn't exist
        target, created = Countdown.objects.get_or_create(id=2)

        # Set the stopped flag to True
        target.stopped = True

        # Calculate the remaining time
        target_date = target.target_date
        current_time = timezone.now()
        remaining_time = target_date - current_time

        # Format the remaining time as a string
        days, seconds = divmod(remaining_time.total_seconds(), 60 * 60 * 24)
        hours, seconds = divmod(seconds, 60 * 60)
        minutes, seconds = divmod(seconds, 60)
        formatted_time = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

        # Set the last update time to the remaining time
        target.last_update = formatted_time

        # Save the updated target date
        target.save()

        return JsonResponse({'message': f'Stopped the countdown'})
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=400)

def start(request):
    try:
        # Get the existing target date record or create a new one if it doesn't exist
        target, created = Countdown.objects.get_or_create(id=2)

        # Set the stopped flag to False
        target.stopped = False

        # Save the updated target date
        target.save()

        return JsonResponse({'message': f'Started the countdown'})
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=400)

def is_stopped(request):
    try:
        # Get the existing target date record or create a new one if it doesn't exist
        target, created = Countdown.objects.get_or_create(id=2)

        # Return whether the countdown is stopped
        return JsonResponse({'stopped': target.stopped})
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=400)

def get_last_countdown(request):
    try:
        # Get the existing target date record or create a new one if it doesn't exist
        target, created = Countdown.objects.get_or_create(id=2)

        # Return the last countdown
        return JsonResponse({'last_update': target.last_update})
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=400)