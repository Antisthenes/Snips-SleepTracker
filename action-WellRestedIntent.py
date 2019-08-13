#!/usr/bin/env python3

from hermes_python.hermes import Hermes


def action_wrapper(hermes, intent_message):
    current_session_id = intent_message.session_id

    if not intent_message.slots["NumberOfHours"]:
        response = "Oh, I don't know what happened. Tell me again. How many hours will you sleep tonight?"
        hermes.publish_end_session(current_session_id, response)
        return

    number_of_hours = int(intent_message.slots["NumberOfHours"].first().value)
    response = '{} hours slept. '.format(number_of_hours)

    if intent_message.slots["SleepQuality"]:
        sleep_quality = intent_message.slots["SleepQuality"].first().value
        response += 'Sleep Quality was {}. '.format(sleep_quality)

    if number_of_hours > 12:
        response = "I think you may sleep too much and swing back to tired."
    elif number_of_hours > 8:
        response = "You should wake up refreshed."
    elif number_of_hours > 6:
        response = "You may get by, but watch out for a mid-day crash."
    else:
        response = "You'll be dragging. Get the coffee ready!"

    hermes.publish_end_session(current_session_id, response)


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("Antisthenes:WellRestedIntent",
                           action_wrapper).start()
