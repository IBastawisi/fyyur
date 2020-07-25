#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import dateutil.parser
from datetime import datetime
import babel
from operator import itemgetter
from itertools import groupby
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from forms import ArtistForm, VenueForm, ShowForm
from models import *
from config import db, app
from init import insert_initial_data

#Insert some data
insert_initial_data()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    if type(value) is str:
        date = dateutil.parser.parse(value)
    else:
        date = value

    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.add_extension('jinja2.ext.do')

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

    upcoming_shows = Show.query.with_entities(Show.venue_id, db.func.count("*").label("num_upcoming_shows"))\
        .filter(Show.start_time > datetime.today()).group_by(Show.venue_id).subquery()

    venues = Venue.query.with_entities(Venue.id, Venue.name, Venue.city, Venue.state, upcoming_shows.c.num_upcoming_shows)\
        .outerjoin(upcoming_shows, upcoming_shows.c.venue_id == Venue.id).all()

    venues = [t._asdict() for t in venues]

    venues.sort(key=itemgetter('city'))

    data = []

    for area, items in groupby(venues, key=itemgetter('city', 'state')):
        result = {
            "city": area[0],
            "state": area[1],
            "venues": []
        }
        for i in items:
            result["venues"].append(i)

        data.append(result)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():

    venues = Venue.query.with_entities(Venue.id, Venue.name)\
        .filter(Venue.name.ilike(f"%{request.form.get('search_term', '')}%")).all()

    response = {'count': len(venues), 'data': venues}

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

    venue = Venue.query.get(venue_id)
    upcoming_shows = []
    past_shows = []

    for show in venue.shows:
        result = {"artist_id": show.artist_id, "artist_name": show.artist.name,
                  "artist_image_link": show.artist.image_link, "start_time": show.start_time}
        if show.start_time > datetime.today():
            upcoming_shows.append(result)
        else:
            past_shows.append(result)

    data = venue.__dict__

    data["genres"] = venue.genres.split(",")

    data['past_shows'] = past_shows
    data['past_shows_count'] = len(past_shows)

    data['upcoming_shows'] = upcoming_shows
    data['upcoming_shows_count'] = len(upcoming_shows)

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

    try:
        form = VenueForm(request.form)

        if not form.validate_on_submit():
            flash('An error occurred. ' + str(form.errors))
            return redirect(url_for('create_venue_form'))

        data = form.data
        data['genres'] = ','.join(data["genres"])
        data.pop('csrf_token')

        venue = Venue(**data)
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        abort(400)

    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

    venue = Venue.query.get(venue_id)
    try:
        db.session.delete(venue)
        db.session.commit()
        flash('Venue ' + venue.name + ' was successfully deleted!')

    except:
        db.session.rollback()
        flash('An error occurred. Venue ' +
              venue.name + ' could not be deleted.')
        abort(400)

    finally:
        db.session.close()

    return None


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):

    artist = Artist.query.get(artist_id)
    try:
        db.session.delete(artist)
        db.session.commit()
        flash('Artist ' + artist.name + ' was successfully deleted!')

    except:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              artist.name + ' could not be deleted.')
        abort(400)

    finally:
        db.session.close()

    return None

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():

    artists = Artist.query.with_entities(Artist.id, Artist.name).all()

    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():

    artists = Artist.query.with_entities(Artist.id, Artist.name).filter(Artist.name.ilike(
        f"%{request.form.get('search_term', '')}%")).all()

    response = {'count': len(artists), 'data': artists}

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

    artist = Artist.query.get(artist_id)
    upcoming_shows = []
    past_shows = []

    for show in artist.shows:
        result = {"venue_id": show.venue_id, "venue_name": show.venue.name,
                  "venue_image_link": show.venue.image_link, "start_time": show.start_time}
        if show.start_time > datetime.today():
            upcoming_shows.append(result)
        else:
            past_shows.append(result)

    data = artist.__dict__

    data["genres"] = artist.genres.split(",")

    data['past_shows'] = past_shows
    data['past_shows_count'] = len(past_shows)

    data['upcoming_shows'] = upcoming_shows
    data['upcoming_shows_count'] = len(upcoming_shows)

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
    form.genres.data = artist.genres.split(",")

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

    try:
        form = ArtistForm(request.form)

        if not form.validate_on_submit():
            flash('An error occurred. ' + str(form.errors))
            return redirect(url_for('edit_artist', artist_id=artist_id))

        data = form.data
        data['genres'] = ','.join(data["genres"])
        data.pop('csrf_token')

        artist = Artist.query.get(artist_id)
        for key, value in data.items():
            setattr(artist, key, value)

        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')

    except:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be updated.')
        abort(400)

    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue, genres=venue.genres.split(","))
    form.genres.data = venue.genres.split(",")

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

    try:
        form = VenueForm(request.form)

        if not form.validate_on_submit():
            flash('An error occurred. ' + str(form.errors))
            return redirect(url_for('edit_venue', venue_id=venue_id))

        data = form.data
        data['genres'] = ','.join(data["genres"])
        data.pop('csrf_token')

        venue = Venue.query.get(venue_id)
        for key, value in data.items():
            setattr(venue, key, value)

        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully updated!')

    except:
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be updated.')
        abort(400)

    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        form = ArtistForm(request.form)

        if not form.validate_on_submit():
            flash('An error occurred. ' + str(form.errors))
            return redirect(url_for('create_artist_form'))

        data = form.data
        data['genres'] = ','.join(data["genres"])
        data.pop('csrf_token')

        artist = Artist(**data)
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')

    except:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
        abort(400)

    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@ app.route('/shows')
def shows():
    shows = Show.query.join(Venue).join(Artist).with_entities(Show.venue_id, Show.artist_id, Show.start_time,
                                                              Venue.name.label("venue_name"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link")).all()
    return render_template('pages/shows.html', shows=shows)


@ app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        form = ShowForm(request.form)
        data = form.data
        data.pop('csrf_token')

        show = Show(**data)
        db.session.add(show)
        db.session.commit()

        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
        abort(400)

    finally:
        db.session.close()

    return render_template('pages/home.html')


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
