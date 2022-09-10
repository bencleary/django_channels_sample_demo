Overview
simple project to show how you can use channels groups to create isolated groups for a single user or other requirement.

Get Started

- Install requirements (Either using Pip or Poetry)
    - Both formats are provided
- run `python manage.py migrate`
- Create two users using `python manage.py createsuperuser`
    - Two accounts are used to test isolation
- Setup a Redis host, to be used by channels as a channels_layer
- Run `python manage.py runserver`
- In a new terminal run `python manage.py send_promotion_to_user` with the ID of the user
    - For example `python manage.py send_promotion_to_user 2``


This gives you a rough idea of how it all works. All of the logic is really in the `notify` application. THere are no tests!