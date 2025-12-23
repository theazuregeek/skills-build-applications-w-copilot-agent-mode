from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):

        # Drop collections directly using Djongo's connection
        from django.db import connection
        db = connection.cursor().db_conn.client['octofit_db']
        db['octofit_tracker_user'].drop()
        db['octofit_tracker_team'].drop()
        db['octofit_tracker_activity'].drop()
        db['octofit_tracker_workout'].drop()
        db['octofit_tracker_leaderboard'].drop()

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create users
        spiderman = User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel)
        ironman = User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel)
        wonderwoman = User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc)
        batman = User.objects.create(name='Batman', email='batman@dc.com', team=dc)
        users = [spiderman, ironman, wonderwoman, batman]

        # Create workouts
        pushups = Workout.objects.create(name='Pushups', description='Do 20 pushups')
        running = Workout.objects.create(name='Running', description='Run 5km')
        pushups.suggested_for.set(users)
        running.suggested_for.set(users)

        # Create activities
        Activity.objects.create(user=spiderman, type='Pushups', duration=10, date=timezone.now().date())
        Activity.objects.create(user=ironman, type='Running', duration=30, date=timezone.now().date())
        Activity.objects.create(user=wonderwoman, type='Pushups', duration=15, date=timezone.now().date())
        Activity.objects.create(user=batman, type='Running', duration=25, date=timezone.now().date())

        # Create leaderboard
        Leaderboard.objects.create(team=marvel, score=100)
        Leaderboard.objects.create(team=dc, score=90)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
